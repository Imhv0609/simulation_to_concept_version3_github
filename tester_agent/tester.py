"""
Tester Agent - Simulated Student
=================================
Uses an LLM to role-play as a student persona and interact with the
educational teaching agent. Supports responding to both regular teaching
messages and simulation-context-enriched messages.

Uses the API tracker for automatic key rotation, just like the main agent.
"""

import os
import sys
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from tester_agent.personas import Persona

# Add parent directory to path so we can import config
sys.path.insert(0, str(Path(__file__).parent.parent))


def _get_llm_for_tester():
    """
    Create an LLM instance for the tester agent.
    Uses the API tracker if available, otherwise falls back to a single key.
    
    Uses a different model (gemma-3-27b-it) to avoid the tester using the
    same model/key as the teaching agent being tested.
    """
    try:
        from config import USE_API_TRACKER, get_best_api_key_for_model
        
        if USE_API_TRACKER:
            api_key = get_best_api_key_for_model("gemini-2.5-flash")
            return ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                api_key=api_key,
                temperature=0.7,
            ), api_key
    except ImportError:
        pass
    
    # Fallback: use direct env key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY_1")
    if not api_key:
        raise RuntimeError("No API key found for tester agent. Set GOOGLE_API_KEY or GOOGLE_API_KEY_1 in .env")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=0.7,
    ), api_key


class TesterAgent:
    """
    Simulated student that interacts with the educational teaching agent.
    
    Maintains a conversation history and responds in-character according to
    the assigned persona. Can handle both regular messages and messages
    that come with simulation context (what the student would "see" on screen).
    """
    
    def __init__(self, persona: Persona):
        self.persona = persona
        self.llm, self._api_key = _get_llm_for_tester()
        
        # Build system prompt for the persona
        base_prompt = (
            f"You are a student with the persona of a '{self.persona.name}'. "
            f"Your characteristics are: {self.persona.description}. "
            f"You must consistently act according to this persona throughout the entire conversation. "
            f"Keep your responses natural, concise (1-3 sentences), and realistic for a student. "
            f"Do NOT break character. Do NOT be overly verbose."
        )
        
        self.history = [
            SystemMessage(content=base_prompt)
        ]
    
    def respond(self, agent_msg: str) -> str:
        """
        Generate a student response to the educational agent's message.
        
        Args:
            agent_msg: The teaching agent's latest message.
            
        Returns:
            The simulated student's response string.
        """
        # Add the educational agent's latest message to history
        self.history.append(AIMessage(content=agent_msg))
        
        prompt = f"""{self.history}

Your task is to provide the next response as the "User" (student), staying true to your persona.
Your response should be on a single line, 1-3 sentences maximum.

User: """
        
        # Track the call if tracker is available
        try:
            from config import USE_API_TRACKER, track_model_call
            response = self.llm.invoke(prompt)
            if USE_API_TRACKER:
                track_model_call("gemini-2.5-flash", self._api_key)
        except ImportError:
            response = self.llm.invoke(prompt)
        
        user_response = response.content.strip()
        
        # Add response to history
        self.history.append(HumanMessage(content=user_response))
        
        return user_response
    
    def respond_with_simulation_context(self, agent_msg: str, simulation_description: str) -> str:
        """
        Respond to the agent with additional context about what's visible in the simulation.
        
        The tester agent can't actually "see" the simulation, so we provide a textual
        description of what the student would observe. This lets the tester respond
        as if they're watching the simulation.
        
        Args:
            agent_msg: The teaching agent's latest message.
            simulation_description: Text description of what's happening in the simulation.
            
        Returns:
            The simulated student's response string.
        """
        # Add the educational agent's latest message to history
        self.history.append(AIMessage(content=agent_msg))
        
        prompt = f"""{self.history}

{simulation_description}

Your task is to provide the next response as the "User" (student), staying true to your persona.
Based on the simulation description provided above, respond as if you can see and observe what's happening in the simulation.
Your response should acknowledge or comment on the simulation if relevant.
Keep it to 1-3 sentences maximum.

User: """
        
        try:
            from config import USE_API_TRACKER, track_model_call
            response = self.llm.invoke(prompt)
            if USE_API_TRACKER:
                track_model_call("gemini-2.5-flash", self._api_key)
        except ImportError:
            response = self.llm.invoke(prompt)
        
        user_response = response.content.strip()
        
        # Add response to history
        self.history.append(HumanMessage(content=user_response))
        
        return user_response
