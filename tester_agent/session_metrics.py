"""
Session Metrics Computer
=========================
Computes quantitative metrics for a teaching session using LLM analysis.
Analyzes conversation history to produce engagement scores, clarity ratings,
user classification, and other measurable outcomes.

Saves metrics locally to JSON files (no external services like Langfuse).
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Literal

from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser

sys.path.insert(0, str(Path(__file__).parent.parent))


# ═══════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════

class LLMAnalyzedMetrics(BaseModel):
    """Metrics extracted by LLM analysis of the conversation."""
    
    concepts_covered: List[str] = Field(
        description="List of educational concepts taught during the session"
    )
    clarity_conciseness_score: float = Field(
        description="Score 1-5 for how clear and concise the agent's explanations were",
        ge=1, le=5
    )
    user_type: Literal["Dull", "Medium", "High"] = Field(
        description="Learner classification based on comprehension speed and curiosity"
    )
    user_interest_rating: float = Field(
        description="Score 1-5 based on enthusiasm, questions asked, and voluntary engagement",
        ge=1, le=5
    )
    user_engagement_rating: float = Field(
        description="Score 1-5 based on response quality, participation, and willingness to explore",
        ge=1, le=5
    )
    enjoyment_probability: float = Field(
        description="Probability 0-1 that the user enjoyed and benefited from the session",
        ge=0, le=1
    )
    error_handling_count: int = Field(
        description="Count of times the agent had to clarify, correct, or re-explain something",
        ge=0
    )
    adaptability: bool = Field(
        description="Whether the agent adapted its teaching approach based on user responses"
    )


class SessionMetrics(BaseModel):
    """Complete session-level metrics for educational agent interactions."""
    
    # LLM-analyzed metrics
    concepts_covered: List[str] = Field(description="List of concepts taught during the session")
    num_concepts_covered: int = Field(description="Total number of concepts touched")
    clarity_conciseness_score: float = Field(description="Based on LLM evaluation (1-5)", ge=1, le=5)
    user_type: str = Field(description="Categorized as Dull, Medium, or High learner")
    user_interest_rating: float = Field(description="Score (1-5) based on engagement indicators", ge=1, le=5)
    user_engagement_rating: float = Field(description="Score (1-5) using response patterns", ge=1, le=5)
    enjoyment_probability: float = Field(description="Likelihood (0-1) that user enjoyed and benefited", ge=0, le=1)
    
    # Computed metrics
    quiz_score: float = Field(description="Score from formative assessments (0-100)", ge=0, le=100)
    error_handling_count: int = Field(description="Count of corrections/re-prompts", ge=0)
    adaptability: bool = Field(description="Whether flow was adjusted dynamically to user performance")
    
    # Session metadata
    session_id: str = Field(description="Unique session identifier")
    simulation_id: str = Field(description="Which simulation was taught", default="unknown")
    total_interactions: int = Field(description="Total number of user-agent exchanges", ge=0)
    persona_name: Optional[str] = Field(description="User persona if known", default=None)


# ═══════════════════════════════════════════════════════════════════════
# METRICS COMPUTER
# ═══════════════════════════════════════════════════════════════════════

def _get_metrics_llm():
    """Create LLM for metrics computation."""
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


class MetricsComputer:
    """Computes session metrics from conversation history and state."""
    
    def __init__(self):
        self.llm, self._api_key = _get_metrics_llm()
        self.llm_parser = PydanticOutputParser(pydantic_object=LLMAnalyzedMetrics)
    
    def compute_metrics(
        self,
        session_id: str,
        history: List[Dict[str, Any]],
        session_state: Dict[str, Any],
        simulation_id: str = "unknown",
        persona_name: Optional[str] = None
    ) -> SessionMetrics:
        """
        Compute all session metrics from conversation history and agent state.
        
        Args:
            session_id: Unique identifier for this session.
            history: Conversation history (list of {role, content} dicts).
            session_state: Final agent state dict.
            simulation_id: Which simulation was being taught.
            persona_name: Name of the persona used (if testing).
            
        Returns:
            SessionMetrics object with all computed metrics.
        """
        # Count interactions
        user_interactions = [h for h in history if h.get("role") in ("user", "student")]
        total_interactions = len(user_interactions)
        
        # Get LLM-analyzed metrics
        llm_metrics = self._analyze_conversation_with_llm(history, persona_name)
        
        # Extract quiz score from state
        quiz_score = self._extract_quiz_score(history, session_state)
        
        return SessionMetrics(
            concepts_covered=llm_metrics.concepts_covered,
            num_concepts_covered=len(llm_metrics.concepts_covered),
            clarity_conciseness_score=llm_metrics.clarity_conciseness_score,
            user_type=llm_metrics.user_type,
            user_interest_rating=llm_metrics.user_interest_rating,
            user_engagement_rating=llm_metrics.user_engagement_rating,
            enjoyment_probability=llm_metrics.enjoyment_probability,
            error_handling_count=llm_metrics.error_handling_count,
            adaptability=llm_metrics.adaptability,
            quiz_score=quiz_score,
            session_id=session_id,
            simulation_id=simulation_id,
            total_interactions=total_interactions,
            persona_name=persona_name,
        )
    
    def _analyze_conversation_with_llm(
        self,
        history: List[Dict[str, Any]],
        persona_name: Optional[str] = None
    ) -> LLMAnalyzedMetrics:
        """Use LLM to extract structured metrics from conversation."""
        
        conversation_text = self._format_conversation(history)
        persona_context = f"\nThe user was acting with the persona: {persona_name}\n" if persona_name else ""
        
        prompt = f"""You are an expert educational analyst. Analyze this educational conversation and provide structured metrics.

{persona_context}
**Conversation History:**
{conversation_text}

**Analysis Instructions:**
1. **Concepts Covered**: List the main educational concepts that were taught
2. **Clarity & Conciseness**: Rate 1-5 how clear and concise the agent's explanations were
3. **User Type**: Classify as "Dull", "Medium", or "High" based on comprehension speed and curiosity
4. **Interest Rating**: Rate 1-5 the user's interest level
5. **Engagement Rating**: Rate 1-5 the user's engagement level
6. **Enjoyment Probability**: Estimate 0-1 likelihood that user enjoyed and benefited
7. **Error Handling Count**: Count how many times the agent had to clarify, correct, or re-explain
8. **Adaptability**: Did the agent adapt its teaching approach based on user responses?

{self.llm_parser.get_format_instructions()}
"""
        
        response = self.llm.invoke(prompt)
        
        # Track the call
        try:
            from config import USE_API_TRACKER, track_model_call
            if USE_API_TRACKER:
                track_model_call("gemini-2.5-flash", self._api_key)
        except ImportError:
            pass
        
        return self.llm_parser.parse(response.content)
    
    def _format_conversation(self, history: List[Dict[str, Any]]) -> str:
        """Format conversation history for LLM analysis."""
        formatted_lines = []
        for interaction in history:
            role = interaction.get("role", "unknown")
            content = interaction.get("content", "")
            if isinstance(content, str):
                formatted_lines.append(f"{role.title()}: {content}")
            else:
                formatted_lines.append(f"{role.title()}: [Non-text content]")
        return "\n".join(formatted_lines)
    
    def _extract_quiz_score(self, history: List[Dict], state: Dict) -> float:
        """Extract quiz score from session state."""
        quiz_score = state.get("quiz_score")
        if quiz_score is not None:
            return float(quiz_score)
        
        # Try to compute from quiz_scores dict
        quiz_scores = state.get("quiz_scores", {})
        if quiz_scores:
            scores = list(quiz_scores.values())
            return (sum(scores) / len(scores)) * 100
        
        return 0.0


# ═══════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTION
# ═══════════════════════════════════════════════════════════════════════

def compute_session_metrics(
    session_id: str,
    history: List[Dict[str, Any]],
    session_state: Dict[str, Any],
    simulation_id: str = "unknown",
    persona_name: Optional[str] = None
) -> SessionMetrics:
    """
    Convenience function to compute session metrics.
    
    Args:
        session_id: Unique session identifier.
        history: Conversation history.
        session_state: Agent's final state.
        simulation_id: Which simulation was taught.
        persona_name: Optional persona name.
    
    Returns:
        SessionMetrics object with all computed metrics.
    """
    computer = MetricsComputer()
    metrics = computer.compute_metrics(
        session_id, history, session_state, simulation_id, persona_name
    )
    
    print(f"📊 Session metrics computed successfully!")
    print(f"   - Concepts covered: {metrics.num_concepts_covered}")
    print(f"   - User type: {metrics.user_type}")
    print(f"   - Quiz score: {metrics.quiz_score:.1f}%")
    print(f"   - Engagement rating: {metrics.user_engagement_rating:.1f}/5")
    print(f"   - Enjoyment probability: {metrics.enjoyment_probability:.2f}")
    
    return metrics
