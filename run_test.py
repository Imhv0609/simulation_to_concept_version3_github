"""
Run Test - Direct Mode (No API)
================================
Tests the educational teaching agent directly by importing the graph functions.
No FastAPI server needed - talks to the LangGraph agent directly.

Usage:
    python run_test.py

Flow:
    1. Select a persona (Eager, Confused, Distracted, Dull)
    2. Select a simulation (pendulum, earth, light_shadows, etc.)
    3. Agent starts teaching, tester agent role-plays as student
    4. Conversation runs until session completes (END state)
    5. Session metrics are computed (LLM-based analysis)
    6. Educational quality is evaluated (pedagogical assessment)
    7. All reports saved to test_reports/ folder
"""

import os
import sys
import json
import time
import uuid
from datetime import datetime
from pprint import pprint
from pathlib import Path

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=True)

from tester_agent.tester import TesterAgent
from tester_agent.evaluator import Evaluator
from tester_agent.personas import personas
from tester_agent.session_metrics import compute_session_metrics
from tester_agent.simulation_descriptor import format_simulation_context_for_tester

# Import our agent's core functions
from config import validate_config
from state import create_initial_state
from graph import start_session, continue_session, get_session_state
from simulations_config import get_simulation, get_simulation_list


# ═══════════════════════════════════════════════════════════════════════
# DELAY BETWEEN TURNS (seconds) - to respect API rate limits
# ═══════════════════════════════════════════════════════════════════════
TURN_DELAY = 15  # seconds between each turn


def select_persona():
    """Let user select a student persona."""
    print("\n" + "="*60)
    print("👤 Select a persona to test:")
    print("="*60)
    for i, p in enumerate(personas):
        print(f"  {i+1}. {p.name} - {p.description[:60]}...")
    
    while True:
        try:
            choice = int(input("\nEnter persona number: ")) - 1
            if 0 <= choice < len(personas):
                return personas[choice]
            print("Invalid choice, try again.")
        except (ValueError, EOFError):
            print("Please enter a number.")


def select_simulation():
    """Let user select a simulation to test."""
    print("\n" + "="*60)
    print("📚 Select a simulation to test:")
    print("="*60)
    
    sim_list = get_simulation_list()
    for i, sim in enumerate(sim_list):
        print(f"  {i+1}. {sim['id']} - {sim['title']}")
    
    while True:
        try:
            choice = int(input("\nEnter simulation number: ")) - 1
            if 0 <= choice < len(sim_list):
                return sim_list[choice]["id"]
            print("Invalid choice, try again.")
        except (ValueError, EOFError):
            print("Please enter a number.")


def convert_state_to_history(state: dict) -> list:
    """
    Convert the agent's conversation_history from internal format to
    simple {role, content} format for evaluation and metrics.
    """
    history = []
    conversation = state.get("conversation_history", [])
    for msg in conversation:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        # Normalize role names
        if role == "teacher":
            role = "assistant"
        elif role == "student":
            role = "user"
        history.append({"role": role, "content": content})
    return history


def save_intermediate_report(thread_id, simulation_id, sim_config, persona, 
                            turn_count, state, timestamp, 
                            session_metrics=None, evaluation=None, completed=False):
    """Save intermediate report after each turn to preserve progress."""
    os.makedirs("test_reports", exist_ok=True)
    
    history_for_reports = convert_state_to_history(state)
    
    report = {
        "test_metadata": {
            "timestamp": datetime.now().isoformat(),
            "mode": "direct (no API)",
            "thread_id": thread_id,
            "simulation_id": simulation_id,
            "simulation_title": sim_config["title"],
            "total_turns": turn_count,
            "completed": completed,  # Flag to indicate if test finished normally
        },
        "persona": persona.model_dump(),
        "conversation_history": history_for_reports,
    }
    
    if session_metrics:
        report["session_metrics"] = session_metrics.model_dump()
    
    if evaluation:
        report["educational_evaluation"] = evaluation
    
    report_filename = f"test_report_{simulation_id}_{persona.name.lower().replace(' ', '_')}_{timestamp}.json"
    report_path = os.path.join("test_reports", report_filename)
    
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    return report_path


def run_test():
    """Main test execution function."""
    
    print("\n" + "="*70)
    print("  🧪 EDUCATIONAL AGENT TESTER - Direct Mode (No API)")
    print("="*70)
    
    # Validate configuration
    try:
        validate_config()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)
    
    # 1. Select Persona
    persona = select_persona()
    print(f"\n✅ Selected persona: {persona.name}")
    
    # 2. Select Simulation
    simulation_id = select_simulation()
    sim_config = get_simulation(simulation_id)
    print(f"✅ Selected simulation: {sim_config['title']} ({simulation_id})")
    
    # 3. Set environment for the simulation and reload config
    os.environ['SIMULATION_ID'] = simulation_id
    
    # Force reload of config module to pick up new simulation
    import importlib
    import config
    importlib.reload(config)
    
    # Force graph recompilation with new simulation
    from graph import reset_graph
    reset_graph()
    
    # 4. Initialize agents
    print("\n⏳ Initializing agents...")
    tester = TesterAgent(persona)
    
    # Create session
    thread_id = f"test_{simulation_id}_{persona.name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    initial_state = create_initial_state(
        topic_description=sim_config["description"],
        initial_params=sim_config["initial_params"].copy(),
        simulation_id=simulation_id
    )
    
    print(f"\n🚀 Starting session: {thread_id}")
    print(f"   Simulation: {sim_config['title']}")
    print(f"   Persona: {persona.name}")
    
    # Variables for finally block
    state = None
    turn_count = 0
    session_metrics = None
    evaluation = None
    
    try:
        # 5. Start the teaching session
        state = start_session(initial_state, thread_id)
        agent_msg = state.get("last_teacher_message", "")
        
        print(f"\n🤖 Teacher: {agent_msg[:200]}...")
        
        # 6. Conversation Loop
        print("\n" + "="*70)
        print("💬 CONVERSATION LOOP")
        print("="*70)
        
        while not state.get("session_complete", False):
            turn_count += 1
            print(f"\n{'─'*50}")
            print(f"--- Turn {turn_count} ---")
            
            # Check if simulation context is available for the tester
            param_history = state.get("parameter_history", [])
            simulation_description = format_simulation_context_for_tester(state)
            
            # Get tester response
            if simulation_description and param_history:
                # There's been a parameter change - give tester simulation context
                print("\n🔬 [Simulation context provided to tester agent]")
                user_msg = tester.respond_with_simulation_context(agent_msg, simulation_description)
            else:
                user_msg = tester.respond(agent_msg)
            
            print(f"👤 {persona.name}: {user_msg}")
            
            # Delay to respect rate limits
            print(f"   ⏳ Waiting {TURN_DELAY}s for rate limits...")
            time.sleep(TURN_DELAY)
            
            # Send response to agent
            state = continue_session(user_msg, thread_id)
            agent_msg = state.get("last_teacher_message", "")
            
            print(f"🤖 Teacher: {agent_msg[:200]}...")
            
            # Print progress
            current_idx = state.get("current_concept_index", 0)
            total_concepts = len(state.get("concepts", []))
            understanding = state.get("understanding_level", "none")
            quiz_mode = state.get("quiz_mode", False)
            
            print(f"   📊 Concept: {current_idx}/{total_concepts} | "
                  f"Understanding: {understanding} | "
                  f"Quiz Mode: {'✅' if quiz_mode else '❌'}")
            
            # Save intermediate report after each turn
            print(f"   💾 Saving progress...")
            report_path = save_intermediate_report(
                thread_id, simulation_id, sim_config, persona,
                turn_count, state, timestamp, completed=False
            )
            print(f"   ✅ Saved to {os.path.basename(report_path)}")
    
    print(f"\n{'='*70}")
    print(f"✅ SESSION COMPLETE after {turn_count} turns")
    print(f"{'='*70}")
    
    # 7. Get final state and convert history
    final_state = get_session_state(thread_id)
    history_for_reports = convert_state_to_history(final_state)
    
    print(f"\n📜 Conversation length: {len(history_for_reports)} messages")
    
    # 8. Compute Session Metrics
    print("\n" + "="*60)
    print("📊 Computing Session Metrics...")
    print("="*60)
    
    session_metrics = None
    try:
        print(f"   ⏳ Waiting {TURN_DELAY}s before metrics computation...")
        time.sleep(TURN_DELAY)
        
        session_metrics = compute_session_metrics(
            session_id=thread_id,
            history=history_for_reports,
            session_state=final_state,
            simulation_id=simulation_id,
            persona_name=persona.name,
        )
        
        print("\n--- Quantitative Metrics ---")
        print(f"  Concepts Covered:    {session_metrics.num_concepts_covered}")
        print(f"  Clarity Score:       {session_metrics.clarity_conciseness_score}/5")
        print(f"  User Type:           {session_metrics.user_type}")
        print(f"  Engagement:          {session_metrics.user_engagement_rating}/5")
        print(f"  Enjoyment:           {session_metrics.enjoyment_probability:.2f}")
        print(f"  Error Handling:      {session_metrics.error_handling_count}")
        print(f"  Adaptability:        {session_metrics.adaptability}")
        print(f"  Quiz Score:          {session_metrics.quiz_score:.1f}%")
    except Exception as e:
        print(f"❌ Error computing metrics: {e}")
        import traceback
        traceback.print_exc()
    
    # 9. Evaluate Educational Quality
    print("\n" + "="*60)
    print("🎓 Evaluating Educational Quality...")
    print("="*60)
    
    evaluation = None
    try:
        print(f"   ⏳ Waiting {TURN_DELAY}s before evaluation...")
        time.sleep(TURN_DELAY)
        
        evaluator = Evaluator()
        evaluation = evaluator.evaluate_parsed(persona, history_for_reports, simulation_id)
        
        print("\n--- Educational Quality Evaluation ---")
        pprint(evaluation)
    except Exception as e:
        print(f"❌ Error evaluating: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 10. Save Final Report (always runs, even on error)
        print("\n" + "="*60)
        print("💾 Saving Final Report...")
        print("="*60)
        
        if state is not None:
            # Save final comprehensive report with completed=True
            final_state = get_session_state(thread_id)
            completed = state.get("session_complete", False)
            
            report_path = save_intermediate_report(
                thread_id, simulation_id, sim_config, persona,
                turn_count, final_state, timestamp,
                session_metrics, evaluation, completed=completed
            )
            print(f"✅ Final report saved to {report_path}")
            
            # Save just the session summary
            session_summary = final_state.get("session_summary", {})
            if session_summary:
                summary_path = os.path.join("test_reports", f"session_summary_{thread_id}.json")
                with open(summary_path, "w") as f:
                    json.dump(session_summary, f, indent=2)
                print(f"✅ Session summary saved to {summary_path}")
        else:
            print("⚠️  No state to save (session never started)")
    
        # 11. Print Final Summary
        print("\n" + "="*70)
        print("📋 FINAL TEST SUMMARY")
        print("="*70)
        print(f"  Session ID:    {thread_id}")
        print(f"  Simulation:    {sim_config['title']} ({simulation_id})")
        print(f"  Persona:       {persona.name}")
        print(f"  Total Turns:   {turn_count}")
        
        if state:
            history_for_reports = convert_state_to_history(state)
            print(f"  Messages:      {len(history_for_reports)}")
        
        if session_metrics:
            print(f"  Concepts:      {session_metrics.num_concepts_covered}")
            print(f"  User Type:     {session_metrics.user_type}")
            print(f"  Engagement:    {session_metrics.user_engagement_rating}/5")
            print(f"  Quiz Score:    {session_metrics.quiz_score:.1f}%")
        
        if evaluation and "scores" in evaluation:
            scores = evaluation["scores"]
            avg = evaluation.get("average_score", 0)
            print(f"  Pedagogy Avg:  {avg}/5")
            for key, val in scores.items():
                print(f"    - {key}: {val}/5")
        
        if state:
            print(f"\n  📁 Report: {report_path}")
        print("="*70)


if __name__ == "__main__":
    run_test()
