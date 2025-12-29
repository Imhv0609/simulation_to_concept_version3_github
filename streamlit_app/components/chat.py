"""
Chat Component
==============
Handles the chat interface - displaying messages and input.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from streamlit_config import UI_CONFIG


def render_chat_message(role: str, content: str, timestamp: str = None):
    """
    Render a single chat message.
    
    Args:
        role: "teacher", "student", or "system"
        content: Message content
        timestamp: Optional timestamp to display
    """
    if role == "teacher":
        with st.chat_message("assistant", avatar="🎓"):
            st.markdown(content)
            if timestamp:
                st.caption(f"_{timestamp}_")
    
    elif role == "student":
        with st.chat_message("user", avatar="👩‍🎓"):
            st.markdown(content)
            if timestamp:
                st.caption(f"_{timestamp}_")
    
    else:  # system
        st.info(content)


def render_chat_history(messages: list):
    """
    Render the chat history.
    
    Args:
        messages: List of message dicts with 'role', 'content', and optional 'timestamp'
    """
    for msg in messages:
        render_chat_message(
            role=msg.get("role", "system"),
            content=msg.get("content", ""),
            timestamp=msg.get("timestamp")
        )


def render_concept_divider(concept_name: str, concept_number: int, total_concepts: int):
    """
    Render a divider when moving to a new concept.
    
    Args:
        concept_name: Name of the new concept
        concept_number: Current concept number (1-indexed)
        total_concepts: Total number of concepts
    """
    st.markdown("---")
    st.markdown(
        f"""
        <div style="
            background-color: #e8f5e9; 
            padding: 15px; 
            border-radius: 10px;
            text-align: center;
            margin: 10px 0;
        ">
            <h3>📚 Concept {concept_number} of {total_concepts}</h3>
            <h4>{concept_name}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")


def render_progress_bar(current_concept: int, total_concepts: int, understanding: str):
    """
    Render learning progress indicator.
    
    Args:
        current_concept: Current concept index (0-based)
        total_concepts: Total number of concepts
        understanding: Current understanding level
    """
    # Progress bar
    progress = (current_concept) / total_concepts if total_concepts > 0 else 0
    st.progress(progress)
    
    # Understanding indicator
    understanding_colors = {
        "none": "🔴",
        "partial": "🟠",
        "mostly": "🟡",
        "complete": "🟢"
    }
    indicator = understanding_colors.get(understanding, "⚪")
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"📊 Concepts: {current_concept}/{total_concepts}")
    with col2:
        st.caption(f"{indicator} Understanding: {understanding.title()}")


def render_chat_input():
    """
    Render the chat input box.
    
    Returns:
        User input string or None
    """
    return st.chat_input("Type your response here...")


def format_teacher_message(content: str) -> str:
    """
    Format teacher message for display.
    Makes certain keywords stand out.
    
    Args:
        content: Raw message content
        
    Returns:
        Formatted message
    """
    # Highlight action words
    formatted = content
    
    # Make OBSERVE, PREDICT, EXPLAIN stand out
    for keyword in ["OBSERVE:", "PREDICT:", "EXPLAIN:"]:
        if keyword in formatted:
            formatted = formatted.replace(
                keyword, 
                f"**{keyword}**"
            )
    
    return formatted


def initialize_chat_state():
    """Initialize chat-related session state variables."""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    if "current_concept_displayed" not in st.session_state:
        st.session_state.current_concept_displayed = -1


def add_message_to_chat(role: str, content: str, simulation_data: dict = None):
    """
    Add a message to the chat history.
    
    Args:
        role: "teacher", "student", or "system"
        content: Message content
        simulation_data: Optional dict with simulation info for before/after display
                        {"before_params": {...}, "after_params": {...}}
    """
    from datetime import datetime
    
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M")
    }
    
    # Add simulation data if present (for parameter changes)
    if simulation_data:
        message["simulation_data"] = simulation_data
    
    st.session_state.chat_messages.append(message)
    
    # Trim if too long
    max_messages = UI_CONFIG.get("max_chat_history", 50)
    if len(st.session_state.chat_messages) > max_messages:
        st.session_state.chat_messages = st.session_state.chat_messages[-max_messages:]


def clear_chat():
    """Clear the chat history."""
    st.session_state.chat_messages = []
    st.session_state.current_concept_displayed = -1


def add_concept_change_marker(concept_name: str, concept_number: int, total_concepts: int):
    """
    Add a marker in chat when concept changes.
    
    Args:
        concept_name: Name of new concept
        concept_number: Concept number (1-indexed)
        total_concepts: Total concepts
    """
    st.session_state.chat_messages.append({
        "role": "system",
        "content": f"📚 **Concept {concept_number}/{total_concepts}:** {concept_name}",
        "timestamp": None,
        "is_divider": True
    })
