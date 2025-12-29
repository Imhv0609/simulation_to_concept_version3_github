"""
Streamlit Teaching Agent App
============================
Main application integrating simulation display with chat interface.
Shows before/after simulation comparison when parameters change.

FULLY INTEGRATED with the LangGraph backend.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for backend imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import simulations config
from simulations_config import get_all_simulations, get_simulation_list

# Import components
from components.simulation import (
    render_simulation_comparison,
    render_simulation_single
)
from components.chat import (
    render_chat_history,
    render_chat_input,
    render_progress_bar,
    initialize_chat_state,
    add_message_to_chat,
    clear_chat,
    add_concept_change_marker,
    format_teacher_message
)
from streamlit_config import get_default_params, UI_CONFIG

# Import backend integration
from backend_integration import (
    is_backend_available,
    create_new_session,
    send_student_response,
    get_current_state,
    extract_display_data,
    get_initial_params
)

# Page config
st.set_page_config(
    page_title="Adaptive Physics Tutor",
    page_icon="🔬",
    layout="wide"
)


def initialize_session_state():
    """Initialize all session state variables."""
    # Chat state
    initialize_chat_state()
    
    # Backend session
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None
    
    if "backend_state" not in st.session_state:
        st.session_state.backend_state = None
    
    # Simulation state
    if "current_simulation" not in st.session_state:
        st.session_state.current_simulation = "simple_pendulum"
    
    if "simulation_params" not in st.session_state:
        st.session_state.simulation_params = get_initial_params()
    
    if "previous_params" not in st.session_state:
        st.session_state.previous_params = None
    
    # Display control
    if "show_simulation_comparison" not in st.session_state:
        st.session_state.show_simulation_comparison = False
    
    if "session_started" not in st.session_state:
        st.session_state.session_started = False
    
    if "last_concept_shown" not in st.session_state:
        st.session_state.last_concept_shown = -1


def start_new_teaching_session():
    """Start a new teaching session with the backend."""
    if not is_backend_available():
        st.error("❌ Backend is not available. Please check configuration.")
        return False
    
    try:
        # Create new session
        thread_id, state = create_new_session()
        
        # Store in session state
        st.session_state.thread_id = thread_id
        st.session_state.backend_state = state
        st.session_state.session_started = True
        
        # Extract display data
        display_data = extract_display_data(state)
        
        # Update simulation params
        st.session_state.simulation_params = display_data["current_params"]
        
        # Add initial teacher message to chat
        teacher_msg = display_data["teacher_message"]
        if teacher_msg:
            formatted_msg = format_teacher_message(teacher_msg)
            add_message_to_chat("teacher", formatted_msg)
        
        # Show concept marker if applicable
        if display_data["current_concept"]:
            concept = display_data["current_concept"]
            add_concept_change_marker(
                concept["title"],
                display_data["current_concept_index"] + 1,
                display_data["total_concepts"]
            )
            st.session_state.last_concept_shown = display_data["current_concept_index"]
        
        return True
        
    except Exception as e:
        st.error(f"❌ Failed to start session: {e}")
        import traceback
        st.error(traceback.format_exc())
        return False


def process_student_response(user_input: str):
    """Process a student response through the backend."""
    if not st.session_state.thread_id:
        st.error("No active session. Please start a new session.")
        return
    
    try:
        # Send response to backend
        state = send_student_response(st.session_state.thread_id, user_input)
        st.session_state.backend_state = state
        
        # Extract display data
        display_data = extract_display_data(state)
        
        # Check for parameter changes (before/after comparison)
        simulation_data = None
        if display_data["has_param_change"]:
            st.session_state.previous_params = display_data["previous_params"]
            st.session_state.simulation_params = display_data["current_params"]
            st.session_state.show_simulation_comparison = True
            # Store simulation data for inline display
            simulation_data = {
                "before_params": display_data["previous_params"],
                "after_params": display_data["current_params"]
            }
        else:
            st.session_state.simulation_params = display_data["current_params"]
            st.session_state.show_simulation_comparison = False
        
        # Check for concept change
        current_idx = display_data["current_concept_index"]
        if current_idx > st.session_state.last_concept_shown and display_data["current_concept"]:
            concept = display_data["current_concept"]
            add_concept_change_marker(
                concept["title"],
                current_idx + 1,
                display_data["total_concepts"]
            )
            st.session_state.last_concept_shown = current_idx
        
        # Add teacher message to chat (with simulation data if params changed)
        teacher_msg = display_data["teacher_message"]
        if teacher_msg:
            formatted_msg = format_teacher_message(teacher_msg)
            add_message_to_chat("teacher", formatted_msg, simulation_data=simulation_data)
        
        return display_data
        
    except Exception as e:
        st.error(f"❌ Error processing response: {e}")
        import traceback
        st.error(traceback.format_exc())
        return None


def render_header():
    """Render the app header."""
    st.markdown("""
    # 🔬 Adaptive Physics Tutor
    *Learn through observation and guided discovery*
    """)


def render_sidebar():
    """Render the sidebar with controls and info."""
    with st.sidebar:
        st.markdown("## � Simulation Selection")
        
        # Get available simulations
        simulations = get_simulation_list()
        sim_options = {sim["title"]: sim["id"] for sim in simulations}
        
        # Only allow changing if session hasn't started
        if not st.session_state.session_started:
            selected_title = st.selectbox(
                "Choose a simulation:",
                options=list(sim_options.keys()),
                help="Select which simulation to use for this learning session"
            )
            
            # Update current simulation if changed
            selected_id = sim_options[selected_title]
            if selected_id != st.session_state.current_simulation:
                st.session_state.current_simulation = selected_id
                # Update environment variable for backend
                import os
                os.environ["SIMULATION_ID"] = selected_id
                st.info(f"📌 Selected: {selected_title}")
        else:
            # Show current simulation (read-only during session)
            current_sim = get_all_simulations()[st.session_state.current_simulation]
            st.info(f"🔒 **Current:** {current_sim['title']}")
            st.caption("(Cannot change during active session)")
        
        st.markdown("---")
        st.markdown("## �📊 Learning Progress")
        
        # Show progress if session is active
        if st.session_state.backend_state:
            display_data = extract_display_data(st.session_state.backend_state)
            
            render_progress_bar(
                display_data["current_concept_index"],
                display_data["total_concepts"],
                display_data["understanding_level"]
            )
            
            st.markdown("---")
            
            # Current concept info
            if display_data["current_concept"]:
                st.markdown("### 📚 Current Concept")
                concept = display_data["current_concept"]
                st.info(f"**{concept['title']}**\n\n{concept.get('description', '')}")
            
            st.markdown("---")
            
            # Understanding details
            st.markdown("### 🎯 Understanding")
            understanding = display_data["understanding_level"]
            trajectory = display_data["trajectory_status"]
            
            understanding_colors = {
                "none": "🔴",
                "partial": "🟠", 
                "mostly": "🟡",
                "complete": "🟢"
            }
            trajectory_icons = {
                "improving": "📈",
                "stagnating": "📊",
                "regressing": "📉"
            }
            
            st.markdown(f"{understanding_colors.get(understanding, '⚪')} Level: **{understanding.title()}**")
            st.markdown(f"{trajectory_icons.get(trajectory, '📊')} Trend: **{trajectory.title()}**")
            st.markdown(f"💬 Exchange: **{display_data['exchange_count']}/{display_data['max_exchanges']}**")
            
            st.markdown("---")
            
            # Current simulation params
            st.markdown("### ⚙️ Simulation Parameters")
            params = display_data["current_params"]
            for key, value in params.items():
                label = key.replace("_", " ").title()
                st.text(f"{label}: {value}")
            
            st.markdown("---")
            
            # Session complete celebration
            if display_data["session_complete"]:
                st.success("🎉 **Session Complete!**")
                st.balloons()
        
        # Action buttons
        st.markdown("### 🔄 Actions")
        
        if st.button("🆕 Start New Session", use_container_width=True):
            clear_chat()
            st.session_state.thread_id = None
            st.session_state.backend_state = None
            st.session_state.session_started = False
            st.session_state.previous_params = None
            st.session_state.show_simulation_comparison = False
            st.session_state.last_concept_shown = -1
            st.session_state.simulation_params = get_initial_params()
            st.rerun()
        
        # Backend status
        st.markdown("---")
        if is_backend_available():
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Unavailable")


def render_chat_with_simulations():
    """
    Render the chat history with inline simulations when parameters change.
    Simulations appear as part of the conversation flow.
    """
    messages = st.session_state.chat_messages
    
    if not messages:
        st.info("Waiting for teacher to start...")
        return
    
    for msg in messages:
        role = msg.get("role", "system")
        content = msg.get("content", "")
        timestamp = msg.get("timestamp")
        simulation_data = msg.get("simulation_data")
        
        # Render the message
        if role == "teacher":
            with st.chat_message("assistant", avatar="🎓"):
                st.markdown(content)
                if timestamp:
                    st.caption(f"_{timestamp}_")
                
                # If this message has simulation data, show before/after comparison
                if simulation_data:
                    st.markdown("---")
                    st.markdown("### 🔬 Observe the Simulation")
                    
                    before_params = simulation_data.get("before_params", {})
                    after_params = simulation_data.get("after_params", {})
                    
                    # Show what changed
                    changes = []
                    for key in after_params:
                        if before_params.get(key) != after_params.get(key):
                            label = key.replace("_", " ").title()
                            changes.append(f"**{label}**: {before_params.get(key)} → {after_params.get(key)}")
                    
                    if changes:
                        st.info("📊 **Parameter Change:** " + " | ".join(changes))
                    
                    # Side by side simulations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### ⬅️ Before")
                        render_simulation_single(
                            sim_key="simple_pendulum",
                            params=before_params,
                            title=""
                        )
                    
                    with col2:
                        st.markdown("#### ➡️ After")
                        render_simulation_single(
                            sim_key="simple_pendulum",
                            params=after_params,
                            title=""
                        )
                    
                    st.markdown("---")
        
        elif role == "student":
            with st.chat_message("user", avatar="👩‍🎓"):
                st.markdown(content)
                if timestamp:
                    st.caption(f"_{timestamp}_")
        
        else:  # system message (concept markers, etc.)
            if msg.get("is_divider"):
                st.markdown("---")
            st.info(content)


def render_demo_mode_controls():
    """Render controls for demo mode (when backend isn't available)."""
    st.warning("🎮 **Demo Mode** - Backend not connected. Limited functionality.")
    
    # Demo controls in sidebar
    with st.sidebar:
        st.markdown("### Demo Controls")
        
        # Param controls
        new_length = st.slider("Pendulum Length", 1, 10, 
                               st.session_state.simulation_params.get("length", 5))
        new_osc = st.slider("Oscillations", 5, 50,
                            st.session_state.simulation_params.get("number_of_oscillations", 10))
        
        if st.button("Update Simulation"):
            st.session_state.previous_params = st.session_state.simulation_params.copy()
            st.session_state.simulation_params = {
                "length": new_length,
                "number_of_oscillations": new_osc
            }
            st.session_state.show_simulation_comparison = True
            st.rerun()
        
        # Demo messages
        if st.button("Add Demo Teacher Message"):
            add_message_to_chat("teacher", 
                "👋 Hello! Let's explore the pendulum together.\n\n**OBSERVE:** What do you notice about how fast the pendulum swings?")
            st.rerun()
        
        if st.button("Reset Demo"):
            clear_chat()
            st.session_state.simulation_params = get_initial_params()
            st.session_state.previous_params = None
            st.session_state.show_simulation_comparison = False
            st.rerun()


def main():
    """Main app function."""
    # Initialize
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Check backend availability
    backend_available = is_backend_available()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area - single column chat interface
    # Simulation will be shown inline when parameters change
    
    st.markdown("### 💬 Learning Conversation")
    
    # Start session button if not started
    if not st.session_state.session_started:
        st.info("👋 Welcome! Click below to start your learning session.")
        
        if backend_available:
            if st.button("🚀 Start Learning Session", use_container_width=True, type="primary"):
                with st.spinner("Initializing teaching session..."):
                    if start_new_teaching_session():
                        st.rerun()
        else:
            render_demo_mode_controls()
    
    else:
        # Render chat messages with inline simulations
        render_chat_with_simulations()
        
        # Check if session is complete
        if st.session_state.backend_state:
            display_data = extract_display_data(st.session_state.backend_state)
            if display_data["session_complete"]:
                st.success("🎉 **Congratulations!** You've completed the lesson!")
                
                # Show summary
                with st.expander("📊 Session Summary"):
                    st.markdown(f"**Concepts Covered:** {display_data['total_concepts']}")
                    for i, concept in enumerate(display_data["concepts"], 1):
                        st.markdown(f"  {i}. {concept['title']}")
                    
                    param_history = display_data["param_history"]
                    if param_history:
                        st.markdown(f"**Parameter Explorations:** {len(param_history)}")
                        effective = sum(1 for p in param_history if p.get("was_effective", False))
                        st.markdown(f"**Effective Changes:** {effective}")
                
                # Don't show input for completed sessions
                return
        
        # Chat input (only if backend available and session not complete)
        if backend_available:
            user_input = render_chat_input()
            
            if user_input:
                # Add student message to chat
                add_message_to_chat("student", user_input)
                
                # Process through backend
                with st.spinner("Teacher is thinking... 🤔"):
                    process_student_response(user_input)
                
                st.rerun()
        else:
            render_demo_mode_controls()
    
    # Footer
    st.markdown("---")
    st.caption("🎓 Adaptive Physics Tutor v3 | Powered by LangGraph + Gemini")


if __name__ == "__main__":
    main()
