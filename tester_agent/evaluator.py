"""
Educational Quality Evaluator
==============================
Uses an LLM to evaluate the pedagogical effectiveness of a conversation
between the teaching agent and a student (persona).

Assesses:
- Pedagogical flow and structure
- Learning objective achievement
- Scaffolding effectiveness
- Misconception handling
- Simulation utilization
- Persona adaptation
"""

import os
import json
import sys
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI

from tester_agent.personas import Persona

sys.path.insert(0, str(Path(__file__).parent.parent))


def _get_evaluator_llm():
    """Create an LLM for evaluation. Uses API tracker if available."""
    try:
        from config import USE_API_TRACKER, get_best_api_key_for_model
        if USE_API_TRACKER:
            api_key = get_best_api_key_for_model("gemini-2.5-flash")
            return ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                api_key=api_key,
                temperature=0.2,
            ), api_key
    except ImportError:
        pass
    
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY_1")
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=0.2,
    ), api_key


class Evaluator:
    """
    Educational Quality Evaluator.
    
    Focuses on pedagogical effectiveness and qualitative assessment.
    Complements the quantitative session metrics by providing:
    - Educational quality scores (pedagogical flow, scaffolding, etc.)
    - Qualitative feedback for improvement
    - Technical issue identification
    """
    
    def __init__(self):
        self.llm, self._api_key = _get_evaluator_llm()
    
    def evaluate(self, persona: Persona, history: list, simulation_id: str = None) -> str:
        """
        Evaluate the educational quality and pedagogical effectiveness of the conversation.
        
        Args:
            persona: The student persona used in the test.
            history: Conversation history as a list of dicts with 'role' and 'content'.
            simulation_id: Optional simulation ID for context.
            
        Returns:
            JSON string with evaluation results.
        """
        simulation_context = ""
        if simulation_id:
            simulation_context = f"\n**Simulation Being Taught:** {simulation_id}\n"
        
        prompt = f"""You are an expert in evaluating educational conversations for pedagogical effectiveness.
Your task is to analyze the following conversation between an educational agent and a student with the persona of a "{persona.name}".

**Persona Description:** {persona.description}
{simulation_context}
**Conversation History:**
{json.dumps(history, indent=2)}

**Educational Quality Metrics (rate each 1-5):**
- **Pedagogical Flow:** Did the conversation follow a logical and effective teaching structure? Did it progress from simple to complex concepts appropriately?
- **Learning Objective Achievement:** How well did the agent help the student achieve the learning objectives? Were concepts properly introduced and reinforced?
- **Scaffolding Effectiveness:** Did the agent provide appropriate support and gradually reduce guidance as the student progressed?
- **Misconception Handling:** How effectively did the agent identify and address student misconceptions?
- **Simulation Utilization:** How well did the agent use the simulation to demonstrate concepts? Did it reference what the student could observe?
- **Quiz Quality:** If quiz mode was reached, how well did the quiz assess understanding? Were hints helpful?

**Qualitative Feedback:**
- **Pedagogical Strengths:** What educational strategies did the agent use effectively?
- **Areas for Educational Improvement:** What pedagogical approaches could be enhanced?
- **Technical Issues:** Were there any bugs, technical problems, or system errors?
- **Persona Alignment:** How well did the agent adapt its teaching style to this specific persona?
- **Overall Assessment:** A brief summary paragraph of the teaching quality.

**Output Format:**
Please provide your evaluation as a JSON object directly. Do NOT wrap in ```json``` markers.
I need to run json.loads() on your output directly.

Example structure:
{{
    "scores": {{
        "pedagogical_flow": 4,
        "learning_objective_achievement": 3,
        "scaffolding_effectiveness": 4,
        "misconception_handling": 3,
        "simulation_utilization": 4,
        "quiz_quality": 3
    }},
    "average_score": 3.5,
    "qualitative_feedback": {{
        "pedagogical_strengths": ["..."],
        "areas_for_improvement": ["..."],
        "technical_issues": ["..."],
        "persona_alignment": "...",
        "overall_assessment": "..."
    }}
}}
"""
        response = self.llm.invoke(prompt)
        
        # Track the call
        try:
            from config import USE_API_TRACKER, track_model_call
            if USE_API_TRACKER:
                track_model_call("gemini-2.5-flash", self._api_key)
        except ImportError:
            pass
        
        return response.content
    
    def evaluate_parsed(self, persona: Persona, history: list, simulation_id: str = None) -> dict:
        """
        Same as evaluate() but returns a parsed dict instead of raw string.
        
        Returns:
            Parsed evaluation dictionary.
        """
        raw = self.evaluate(persona, history, simulation_id)
        
        # Clean up common LLM formatting issues
        clean_str = raw.strip()
        if clean_str.startswith("```json"):
            clean_str = clean_str[7:]
        if clean_str.startswith("```"):
            clean_str = clean_str[3:]
        if clean_str.endswith("```"):
            clean_str = clean_str[:-3]
        clean_str = clean_str.strip()
        
        try:
            return json.loads(clean_str)
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse evaluation: {e}",
                "raw_response": raw
            }
