"""
Content Loader Node
===================
Parses the topic description and extracts teachable concepts using LLM.

This node runs ONCE at the start of a session to:
1. Analyze the topic description
2. Extract 2-4 key concepts that can be taught
3. Identify which parameters best illustrate each concept
4. Create a teaching plan
"""

import json
import re
from typing import Dict, Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from config import GOOGLE_API_KEY, GEMINI_MODEL, TEMPERATURE


def get_llm():
    """Get configured LLM instance."""
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=TEMPERATURE
    )


def parse_json_safe(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown code blocks."""
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract from markdown code block
    code_block_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
    if code_block_match:
        try:
            return json.loads(code_block_match.group(1).strip())
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON object
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    raise ValueError(f"Could not parse JSON from: {text[:200]}...")


def content_loader_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract teachable concepts from the topic description.
    
    Input State:
        - topic_description: The source material
        
    Output State:
        - concepts: List of Concept objects with teaching plan
        
    Example Output:
        concepts = [
            {
                "id": 1,
                "title": "Length affects time period",
                "description": "Longer pendulums swing slower...",
                "key_insight": "T = 2π√(L/g) shows direct relationship",
                "related_params": ["length"]
            },
            ...
        ]
    """
    print("\n" + "="*60)
    print("📚 CONTENT LOADER: Extracting concepts from topic")
    print("="*60)
    
    topic = state.get("topic_description", "")
    
    if not topic:
        raise ValueError("No topic_description provided in state")
    
    # Create extraction prompt
    extraction_prompt = f"""
You are an expert physics teacher. Analyze this topic description and extract 
2-4 KEY CONCEPTS that should be taught to a student.

TOPIC DESCRIPTION:
{topic}

For each concept, provide:
1. A short title (5-7 words)
2. A clear description of what to teach (2-3 sentences)
3. The key insight or "aha moment" the student should reach
4. Which simulation parameters best illustrate this concept

IMPORTANT:
- Order concepts from foundational to advanced
- Each concept should build on the previous
- Focus on concepts that can be demonstrated through parameter changes

Return ONLY valid JSON in this exact format:
{{
    "concepts": [
        {{
            "id": 1,
            "title": "Short concept title",
            "description": "What this concept is about and why it matters...",
            "key_insight": "The main takeaway the student should understand",
            "related_params": ["param1", "param2"]
        }}
    ]
}}
"""
    
    llm = get_llm()
    response = llm.invoke([HumanMessage(content=extraction_prompt)])
    
    try:
        result = parse_json_safe(response.content)
        concepts = result.get("concepts", [])
        
        print(f"\n✅ Extracted {len(concepts)} concepts:")
        for c in concepts:
            print(f"   {c['id']}. {c['title']}")
            print(f"      Params: {c['related_params']}")
        
        return {
            "concepts": concepts,
            "current_concept_index": 0
        }
        
    except Exception as e:
        print(f"❌ Error parsing concepts: {e}")
        print(f"   Raw response: {response.content[:200]}...")
        
        # Fallback: Create a single default concept
        fallback_concepts = [{
            "id": 1,
            "title": "Understanding the Simple Pendulum",
            "description": "Learn how a pendulum's motion is affected by its physical properties.",
            "key_insight": "The time period depends mainly on length, not mass or angle.",
            "related_params": ["length", "mass", "angle"]
        }]
        
        return {
            "concepts": fallback_concepts,
            "current_concept_index": 0
        }
