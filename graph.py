"""
LangGraph Definition for Version 3 Teaching Agent
=================================================
Defines the graph structure, routing logic, and execution helpers.

Graph Flow:
    ┌─────────────────┐
    │ content_loader  │ (Start - extracts concepts)
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │    teacher      │◄────────────────────────────┐
    └────────┬────────┘                             │
             │                                      │
             ▼                                      │
    ┌─────────────────┐                             │
    │   [INTERRUPT]   │ (Wait for student input)   │
    └────────┬────────┘                             │
             │                                      │
             ▼                                      │
    ┌─────────────────┐                             │
    │   evaluator     │                             │
    └────────┬────────┘                             │
             │                                      │
             ▼                                      │
    ┌─────────────────┐                             │
    │   trajectory    │                             │
    └────────┬────────┘                             │
             │                                      │
             ▼                                      │
    ┌─────────────────┐                             │
    │    strategy     │─────────────────────────────┘
    └────────┬────────┘          (if not complete)
             │
             ▼ (if session_complete)
    ┌─────────────────┐
    │      END        │
    └─────────────────┘
"""

from typing import Dict, Any

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from state import TeachingState
from nodes import (
    content_loader_node,
    teacher_node,
    understanding_evaluator_node,
    trajectory_analyzer_node,
    strategy_selector_node
)


# ═══════════════════════════════════════════════════════════════════════════
# GLOBAL CHECKPOINTER
# ═══════════════════════════════════════════════════════════════════════════

_checkpointer = MemorySaver()
_compiled_graph = None


# ═══════════════════════════════════════════════════════════════════════════
# ROUTING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def route_after_strategy(state: TeachingState) -> str:
    """
    Route after strategy selector.
    
    If session is complete → END
    Otherwise → back to teacher
    """
    session_complete = state.get("session_complete", False)
    
    if session_complete:
        print("\n🔀 [ROUTING] Session complete → END")
        return END
    else:
        print("\n🔀 [ROUTING] Continue teaching → teacher")
        return "teacher"


# ═══════════════════════════════════════════════════════════════════════════
# GRAPH CREATION
# ═══════════════════════════════════════════════════════════════════════════

def create_teaching_graph() -> StateGraph:
    """Create the adaptive teaching workflow graph."""
    
    workflow = StateGraph(TeachingState)
    
    # Add all nodes
    workflow.add_node("content_loader", content_loader_node)
    workflow.add_node("teacher", teacher_node)
    workflow.add_node("evaluator", understanding_evaluator_node)
    workflow.add_node("trajectory", trajectory_analyzer_node)
    workflow.add_node("strategy", strategy_selector_node)
    
    # Set entry point
    workflow.set_entry_point("content_loader")
    
    # Define edges
    workflow.add_edge("content_loader", "teacher")
    # Teacher → [INTERRUPT] → Evaluator (interrupt handled in compile)
    workflow.add_edge("teacher", "evaluator")
    workflow.add_edge("evaluator", "trajectory")
    workflow.add_edge("trajectory", "strategy")
    
    # Conditional routing after strategy
    workflow.add_conditional_edges(
        "strategy",
        route_after_strategy,
        {
            "teacher": "teacher",
            END: END
        }
    )
    
    return workflow


def compile_graph(force_recompile: bool = False):
    """Compile graph with checkpointer and interrupt points (singleton)."""
    global _compiled_graph, _checkpointer
    
    if _compiled_graph is None or force_recompile:
        # Reset checkpointer when recompiling to avoid session conflicts
        if force_recompile:
            _checkpointer = MemorySaver()
        
        print("\n" + "="*60)
        print("🔧 COMPILING TEACHING GRAPH")
        print("="*60)
        
        workflow = create_teaching_graph()
        _compiled_graph = workflow.compile(
            checkpointer=_checkpointer,
            interrupt_before=["evaluator"]  # Pause before evaluation to get student input
        )
        
        print("✅ Graph compiled with:")
        print("   • MemorySaver checkpointer")
        print("   • Interrupt before evaluator (for student input)")
        print("   • Flow: content_loader → teacher → [WAIT] → evaluator → trajectory → strategy → [loop/END]")
    
    return _compiled_graph


def reset_graph():
    """Force reset the compiled graph. Call this when simulation changes."""
    global _compiled_graph, _checkpointer
    _compiled_graph = None
    _checkpointer = MemorySaver()
    print("🔄 Graph reset - will recompile on next use")


# ═══════════════════════════════════════════════════════════════════════════
# EXECUTION HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def start_session(initial_state: Dict[str, Any], thread_id: str) -> Dict[str, Any]:
    """
    Start a new teaching session.
    
    Runs the graph until it hits the interrupt point (waiting for student input).
    
    Args:
        initial_state: Starting state with topic_description and initial_params
        thread_id: Unique ID for this session
        
    Returns:
        Current state after teacher's first message
    """
    graph = compile_graph()
    config = {"configurable": {"thread_id": thread_id}}
    
    print("\n" + "="*60)
    print(f"🚀 STARTING SESSION: {thread_id}")
    print("="*60)
    
    # Run until interrupt
    for event in graph.stream(initial_state, config=config):
        for node_name in event.keys():
            print(f"   ✓ Completed: {node_name}")
    
    # Get full state
    snapshot = graph.get_state(config)
    return dict(snapshot.values)


def continue_session(student_response: str, thread_id: str) -> Dict[str, Any]:
    """
    Continue session with student's response.
    
    Updates state with student response and continues graph execution.
    
    Args:
        student_response: What the student said
        thread_id: Session ID
        
    Returns:
        Updated state after processing and teacher's next message
    """
    graph = compile_graph()
    config = {"configurable": {"thread_id": thread_id}}
    
    print("\n" + "="*60)
    print("📥 PROCESSING STUDENT RESPONSE")
    print("="*60)
    print(f"   Response: \"{student_response[:100]}...\"" if len(student_response) > 100 else f"   Response: \"{student_response}\"")
    
    # Update state with student response
    graph.update_state(config, {"student_response": student_response})
    
    # Continue execution
    for event in graph.stream(None, config=config):
        for node_name in event.keys():
            print(f"   ✓ Completed: {node_name}")
    
    # Get full state
    snapshot = graph.get_state(config)
    return dict(snapshot.values)


def get_session_state(thread_id: str) -> Dict[str, Any]:
    """Get current state of a session."""
    graph = compile_graph()
    config = {"configurable": {"thread_id": thread_id}}
    snapshot = graph.get_state(config)
    return dict(snapshot.values) if snapshot.values else {}
