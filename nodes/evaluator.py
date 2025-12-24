"""
Understanding Evaluator Node
============================
Analyzes student responses to determine their understanding level.

This node uses the LLM to:
1. Assess what the student understood from their response
2. Identify misconceptions or gaps
3. Assign an understanding level (none/partial/mostly/complete)
4. Provide reasoning for the assessment

The evaluation is nuanced - it's not just right/wrong, but a spectrum.
"""

import json
import re
from typing import Dict, Any
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from config import GOOGLE_API_KEY, GEMINI_MODEL, TEMPERATURE
from state import add_message_to_history


def get_llm():
    """Get configured LLM instance."""
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3  # Lower temperature for more consistent evaluation
    )


def parse_json_safe(text: str) -> dict:
    """Extract JSON from LLM response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    code_block_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if code_block_match:
        try:
            return json.loads(code_block_match.group(1).strip())
        except json.JSONDecodeError:
            pass
    
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    return {"level": "partial", "reasoning": "Could not parse evaluation"}


def understanding_evaluator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate the student's understanding from their response.
    
    Input State:
        - student_response: What the student said
        - concepts: All concepts
        - current_concept_index: Which concept
        - conversation_history: Context
        - understanding_trajectory: Past levels
        - parameter_history: What we've tried
        
    Output State:
        - understanding_level: none/partial/mostly/complete
        - understanding_reasoning: Why this level
        - understanding_trajectory: Updated history
        - conversation_history: Updated with student message
        
    Understanding Levels:
        - none: No evidence of understanding, completely off track
        - partial: Some grasp but significant gaps or misconceptions
        - mostly: Good understanding with minor gaps
        - complete: Clear, correct understanding of the concept
    """
    print("\n" + "="*60)
    print("🔍 EVALUATOR NODE: Assessing understanding")
    print("="*60)
    
    student_response = state.get("student_response", "")
    
    if not student_response:
        print("   ⚠️ No student response to evaluate")
        return {
            "understanding_level": "none",
            "understanding_reasoning": "Student hasn't responded yet"
        }
    
    # Get current concept
    concepts = state.get("concepts", [])
    current_idx = state.get("current_concept_index", 0)
    
    if current_idx >= len(concepts):
        return {
            "understanding_level": "complete",
            "understanding_reasoning": "All concepts completed"
        }
    
    current_concept = concepts[current_idx]
    
    # Get context
    conversation = state.get("conversation_history", [])
    param_history = state.get("parameter_history", [])
    last_teacher_msg = state.get("last_teacher_message", "")
    
    print(f"   Student said: \"{student_response[:100]}...\"" if len(student_response) > 100 else f"   Student said: \"{student_response}\"")
    
    # Build evaluation prompt
    eval_prompt = f"""You are evaluating a student's understanding of a physics concept.

CONCEPT BEING TAUGHT:
Title: {current_concept['title']}
Key Insight: {current_concept['key_insight']}

TEACHER'S LAST QUESTION:
"{last_teacher_msg}"

STUDENT'S RESPONSE:
"{student_response}"

═══════════════════════════════════════════════════════════════
🎯 OBSERVATION ≠ UNDERSTANDING - Require reasoning for 'complete'
═══════════════════════════════════════════════════════════════

UNDERSTANDING LEVELS:
- "complete": Student explains WHAT happens AND gives a reason WHY (even a simple one)
- "mostly": Correct observation/prediction but NO reasoning (good start, needs follow-up!)
- "partial": Wrong direction, vague, or just acknowledgment ("okay", "sure")
- "none": "I don't know", off-topic, or completely wrong

CRITICAL DISTINCTION:
- OBSERVATION ONLY = "it took longer", "swings slower" → MOSTLY (correct but no WHY)
- WITH REASONING = "longer because more distance to travel" → COMPLETE (shows understanding)

SCORING RULES:
1. **OBSERVATION WITHOUT WHY = MOSTLY**: "it took longer" is correct but doesn't explain WHY
2. **CORRECT + ANY REASONING = COMPLETE**: Be VERY generous! Even simple reasoning counts:
   - "because it's longer" = COMPLETE (simple but valid)
   - "more distance" = COMPLETE
   - "gravity pulls more" = COMPLETE (any physics reasoning)
   - "because..." followed by anything = COMPLETE
3. **WRONG DIRECTION = PARTIAL**: Tried but got it backwards
4. **ACKNOWLEDGMENTS = PARTIAL**: "okay", "sure" = not demonstrating anything
5. **"I don't know" = NONE**: Needs teaching

EXAMPLES (be generous with reasoning!):
- "it takes longer" → MOSTLY (observation only, no because/why)
- "it took longer" → MOSTLY (observation only)
- "longer because more distance" → COMPLETE ✓
- "because it's longer" → COMPLETE ✓ (simple but counts!)
- "I think because gravity" → COMPLETE ✓ (any reasoning attempt)
- "slower, more to travel" → COMPLETE ✓ (implied reasoning)
- "I think faster" → PARTIAL (wrong direction)
- "okay" / "sure" → PARTIAL
- "I don't know" → NONE

Return JSON:
{{
    "level": "complete/mostly/partial/none",
    "reasoning": "Brief explanation",
    "what_they_got_right": "What was correct",
    "needs_deeper": true/false
}}

Set needs_deeper=true if level is "mostly" (they need to explain WHY).
"""

    llm = get_llm()
    response = llm.invoke([HumanMessage(content=eval_prompt)])
    
    result = parse_json_safe(response.content)
    
    level = result.get("level", "partial")
    reasoning = result.get("reasoning", "Evaluation uncertain")
    needs_deeper = result.get("needs_deeper", False)
    
    # Validate level
    valid_levels = ["none", "partial", "mostly", "complete"]
    if level not in valid_levels:
        level = "partial"
    
    print(f"\n   📊 Understanding Level: {level.upper()}")
    print(f"   📝 Reasoning: {reasoning}")
    if needs_deeper:
        print(f"   🔄 Needs Deeper: Yes (correct observation, asking for WHY)")
    if result.get("detected_misconception"):
        print(f"   ⚠️ Misconception: {result['detected_misconception']}")
    
    # Update trajectory
    old_trajectory = state.get("understanding_trajectory", [])
    new_trajectory = old_trajectory + [level]
    
    # Add student message to history
    student_message = add_message_to_history(state, "student", student_response)
    new_conversation = state.get("conversation_history", []) + [student_message]
    
    # Update last parameter change if exists
    param_history = state.get("parameter_history", [])
    if param_history:
        # Update the most recent parameter change with student's reaction
        param_history[-1]["student_reaction"] = student_response[:200]
        param_history[-1]["understanding_after"] = level
        
        # Determine if the parameter change was effective
        before = param_history[-1].get("understanding_before", "none")
        level_order = {"none": 0, "partial": 1, "mostly": 2, "complete": 3}
        if level_order.get(level, 0) > level_order.get(before, 0):
            param_history[-1]["was_effective"] = True
    
    return {
        "understanding_level": level,
        "understanding_reasoning": reasoning,
        "understanding_trajectory": new_trajectory,
        "conversation_history": new_conversation,
        "parameter_history": param_history,
        "needs_deeper": needs_deeper,  # Flag for teacher to ask WHY
        # Store additional insights for strategy selector
        "_eval_details": {
            "what_they_got_right": result.get("what_they_got_right", ""),
            "what_needs_work": result.get("what_needs_work", ""),
            "misconception": result.get("detected_misconception")
        }
    }
