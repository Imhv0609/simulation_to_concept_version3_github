"""
Backend Integration Module
==========================
Provides a clean interface between the Streamlit app and the LangGraph backend.
Handles session management, state synchronization, and response processing.
"""

import sys
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Add parent directory to path for backend imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import backend modules
try:
    from config import (
        validate_config,
        TOPIC_DESCRIPTION,
        INITIAL_PARAMS,
        MAX_EXCHANGES,
        CANNOT_DEMONSTRATE,
        PRE_DEFINED_CONCEPTS,
        build_simulation_url
    )
    from state import create_initial_state, TeachingState
    from graph import start_session, continue_session, get_session_state
    
    BACKEND_AVAILABLE = True
    
except Exception as e:
    print(f"Backend import error: {e}")
    import traceback
    traceback.print_exc()
    BACKEND_AVAILABLE = False
    # Set defaults
    INITIAL_PARAMS = {"length": 5, "number_of_oscillations": 10}
    MAX_EXCHANGES = 6


def is_backend_available() -> bool:
    """Check if the backend is available."""
    return BACKEND_AVAILABLE


def create_new_session() -> Tuple[str, Dict[str, Any]]:
    """
    Create a new teaching session.
    
    Returns:
        Tuple of (thread_id, initial_state_from_backend)
    """
    if not BACKEND_AVAILABLE:
        raise RuntimeError("Backend not available")
    
    # Validate config
    validate_config()
    
    # Create unique session ID
    thread_id = f"streamlit_session_{uuid.uuid4().hex[:8]}"
    
    # Create initial state
    initial_state = create_initial_state(
        topic_description=TOPIC_DESCRIPTION,
        initial_params=INITIAL_PARAMS.copy()
    )
    
    # Start the session - runs until first interrupt (waiting for student input)
    state = start_session(initial_state, thread_id)
    
    return thread_id, state


def send_student_response(thread_id: str, response: str) -> Dict[str, Any]:
    """
    Send a student response and get the updated state.
    
    Args:
        thread_id: The session thread ID
        response: Student's response text
        
    Returns:
        Updated state dict
    """
    if not BACKEND_AVAILABLE:
        raise RuntimeError("Backend not available")
    
    state = continue_session(response, thread_id)
    return state


def get_current_state(thread_id: str) -> Dict[str, Any]:
    """
    Get the current state of a session.
    
    Args:
        thread_id: The session thread ID
        
    Returns:
        Current state dict
    """
    if not BACKEND_AVAILABLE:
        return {}
    
    return get_session_state(thread_id)


def extract_display_data(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract data from backend state for UI display.
    
    Args:
        state: Full backend state
        
    Returns:
        Dict with UI-friendly data
    """
    concepts = state.get("concepts", [])
    current_idx = state.get("current_concept_index", 0)
    
    # Get current concept info
    current_concept = None
    if current_idx < len(concepts):
        current_concept = concepts[current_idx]
    
    # Get parameter changes for comparison
    param_history = state.get("parameter_history", [])
    has_param_change = False
    previous_params = None
    current_params = state.get("current_params", INITIAL_PARAMS.copy())
    
    # Check if there was a recent parameter change (within the last response)
    if param_history:
        last_change = param_history[-1]
        # Only show comparison if the student hasn't reacted yet (empty reaction)
        if last_change.get("student_reaction", "") == "":
            has_param_change = True
            # Reconstruct previous params
            previous_params = current_params.copy()
            previous_params[last_change["parameter"]] = last_change["old_value"]
    
    return {
        # Teacher message
        "teacher_message": state.get("last_teacher_message", ""),
        
        # Progress info
        "current_concept_index": current_idx,
        "total_concepts": len(concepts),
        "current_concept": current_concept,
        "concepts": concepts,
        
        # Understanding
        "understanding_level": state.get("understanding_level", "none"),
        "understanding_reasoning": state.get("understanding_reasoning", ""),
        "trajectory_status": state.get("trajectory_status", "improving"),
        
        # Exchange info
        "exchange_count": state.get("exchange_count", 0),
        "max_exchanges": MAX_EXCHANGES,
        
        # Simulation params
        "current_params": current_params,
        "previous_params": previous_params,
        "has_param_change": has_param_change,
        "param_history": param_history,
        
        # Session status
        "session_complete": state.get("session_complete", False),
        "concept_complete": state.get("concept_complete", False),
        
        # Teaching context
        "strategy": state.get("strategy", "continue"),
        "teacher_mode": state.get("teacher_mode", "encouraging"),
        
        # Conversation history
        "conversation_history": state.get("conversation_history", [])
    }


def get_initial_params() -> Dict[str, Any]:
    """Get the initial simulation parameters."""
    if BACKEND_AVAILABLE:
        return INITIAL_PARAMS.copy()
    return {"length": 5, "number_of_oscillations": 10}


def get_concepts() -> list:
    """Get the pre-defined concepts."""
    if BACKEND_AVAILABLE:
        return PRE_DEFINED_CONCEPTS
    return []


def get_topic_description() -> str:
    """Get the topic description."""
    if BACKEND_AVAILABLE:
        return TOPIC_DESCRIPTION
    return "Time & Pendulums"


def build_sim_url(params: Dict[str, Any], autostart: bool = True) -> str:
    """Build simulation URL with parameters."""
    if BACKEND_AVAILABLE:
        return build_simulation_url(params, autostart)
    
    # Fallback URL building
    base_url = "https://imhv0609.github.io/simulation_to_concept_github/SimulationsNCERT-main/simple_pendulum.html"
    url = f"{base_url}?length={params.get('length', 5)}&oscillations={params.get('number_of_oscillations', 10)}"
    if autostart:
        url += "&autoStart=true"
    return url
