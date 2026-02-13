"""
Run Test - API Mode
====================
Tests the educational teaching agent through the FastAPI REST endpoints.
Requires the API server to be running first.

Usage:
    1. Start the API server:  uvicorn api_server:app --reload --port 8000
    2. Run this script:       python run_test_api.py

Flow:
    1. Health-check the API server
    2. Select a persona (Eager, Confused, Distracted, Dull)
    3. Select a simulation from available simulations via API
    4. Start session via POST /api/session/start
    5. Tester agent role-plays as student, sends responses via POST /api/session/{id}/respond
    6. Conversation runs until session_complete == True
    7. Session metrics computed and educational quality evaluated
    8. All reports saved to test_reports/ folder
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pprint import pprint
from pathlib import Path
from typing import Optional, Dict, Any

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=True)

from tester_agent.tester import TesterAgent
from tester_agent.evaluator import Evaluator
from tester_agent.personas import personas
from tester_agent.session_metrics import compute_session_metrics
from tester_agent.simulation_descriptor import format_simulation_from_api_metadata
from tester_agent.parameter_validator import ParameterValidator


# ═══════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

API_BASE_URL = os.getenv("TEST_API_URL", "http://localhost:8000")
TURN_DELAY = 15  # seconds between turns (rate limit protection)


# ═══════════════════════════════════════════════════════════════════════
# API CLIENT
# ═══════════════════════════════════════════════════════════════════════

class TeachingAgentAPIClient:
    """Client for interacting with the Teaching Agent REST API."""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the API server is running."""
        response = self.session.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()
    
    def list_simulations(self) -> Dict[str, Any]:
        """Get list of available simulations."""
        response = self.session.get(f"{self.base_url}/api/simulations")
        response.raise_for_status()
        return response.json()
    
    def start_session(self, simulation_id: str, student_id: str = None) -> Dict[str, Any]:
        """Start a new teaching session."""
        payload = {
            "simulation_id": simulation_id,
        }
        if student_id:
            payload["student_id"] = student_id
        
        response = self.session.post(
            f"{self.base_url}/api/session/start",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def send_response(self, session_id: str, student_response: str) -> Dict[str, Any]:
        """Send a student response and get teacher's reply."""
        payload = {
            "student_response": student_response
        }
        response = self.session.post(
            f"{self.base_url}/api/session/{session_id}/respond",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get current session state."""
        response = self.session.get(
            f"{self.base_url}/api/session/{session_id}"
        )
        response.raise_for_status()
        return response.json()
    
    def submit_quiz(self, session_id: str, question_id: str, parameters: Dict) -> Dict[str, Any]:
        """Submit a quiz answer."""
        payload = {
            "question_id": question_id,
            "submitted_parameters": parameters
        }
        response = self.session.post(
            f"{self.base_url}/api/session/{session_id}/submit-quiz",
            json=payload
        )
        response.raise_for_status()
        return response.json()


# ═══════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════

def extract_history_from_api_responses(turns: list) -> list:
    """
    Convert collected turn data into {role, content} history format
    for evaluation and metrics computation.
    """
    history = []
    for turn in turns:
        if turn.get("teacher_message"):
            history.append({"role": "assistant", "content": turn["teacher_message"]})
        if turn.get("student_message"):
            history.append({"role": "user", "content": turn["student_message"]})
    return history


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


def select_simulation(api_client: TeachingAgentAPIClient) -> tuple:
    """Let user select a simulation from API's available list."""
    print("\n" + "="*60)
    print("📚 Select a simulation to test:")
    print("="*60)
    
    try:
        sims_response = api_client.list_simulations()
        simulations = sims_response.get("simulations", [])
        
        for i, sim in enumerate(simulations):
            print(f"  {i+1}. {sim['id']} - {sim['title']} ({sim.get('concepts_count', '?')} concepts)")
        
        while True:
            try:
                choice = int(input("\nEnter simulation number: ")) - 1
                if 0 <= choice < len(simulations):
                    sim = simulations[choice]
                    return sim["id"], sim["title"]
                print("Invalid choice, try again.")
            except (ValueError, EOFError):
                print("Please enter a number.")
    except Exception as e:
        print(f"❌ Error fetching simulations: {e}")
        sim_id = input("Enter simulation ID manually: ").strip()
        return sim_id, sim_id


# ═══════════════════════════════════════════════════════════════════════
# MAIN TEST RUNNER
# ═══════════════════════════════════════════════════════════════════════

def run_test_api():
    """Main API-based test execution function."""
    
    print("\n" + "="*70)
    print("  🧪 EDUCATIONAL AGENT TESTER - API Mode")
    print("="*70)
    
    api_client = TeachingAgentAPIClient()
    
    # 1. Health Check
    print("\n🏥 Checking API Health...")
    try:
        health = api_client.health_check()
        print(f"  ✅ API Status: {health.get('status')}")
        print(f"  📦 Service: {health.get('service')}")
        print(f"  🎮 Simulations: {health.get('available_simulations')}")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Cannot connect to API at {API_BASE_URL}")
        print(f"     Make sure the API server is running:")
        print(f"     uvicorn api_server:app --reload --port 8000")
        print(f"     Error: {e}")
        return
    
    # 2. Select Persona
    persona = select_persona()
    print(f"\n✅ Selected persona: {persona.name}")
    
    # 3. Select Simulation
    simulation_id, simulation_title = select_simulation(api_client)
    print(f"✅ Selected simulation: {simulation_title} ({simulation_id})")
    
    # 4. Initialize Tester Agent and Validator
    print("\n⏳ Initializing tester agent and validator...")
    tester = TesterAgent(persona)
    validator = ParameterValidator(simulation_id)
    print("   ✅ Parameter validator initialized")
    
    # 5. Start Session via API
    print("\n" + "="*60)
    print("🚀 Starting Session via API...")
    print("="*60)
    
    try:
        start_response = api_client.start_session(
            simulation_id=simulation_id,
            student_id=f"tester_{persona.name.lower().replace(' ', '_')}"
        )
    except requests.exceptions.RequestException as e:
        print(f"❌ Error starting session: {e}")
        return
    
    session_id = start_response.get("session_id")
    agent_msg = start_response.get("teacher_message", {}).get("text", "")
    session_complete = start_response.get("learning_state", {}).get("session_complete", False)
    
    print(f"  ✅ Session started!")
    print(f"  📝 Session ID: {session_id}")
    print(f"\n🤖 Teacher: {agent_msg[:200]}...")
    
    # Track turns for history and validation
    turns = [{"teacher_message": agent_msg, "student_message": None}]
    last_response = start_response
    previous_params = None
    
    # 6. Conversation Loop
    print("\n" + "="*70)
    print("💬 CONVERSATION LOOP")
    print("="*70)
    
    turn_count = 0
    previous_params = None
    
    try:
        while not session_complete:
            turn_count += 1
            print(f"\n{'─'*50}")
            print(f"--- Turn {turn_count} ---")
            
            # Check for simulation context in the API response
            simulation_description = format_simulation_from_api_metadata(last_response)
            
            # Get tester response
            if simulation_description:
                print("🔬 [Simulation context provided to tester agent]")
                user_msg = tester.respond_with_simulation_context(agent_msg, simulation_description)
            else:
                user_msg = tester.respond(agent_msg)
            
            print(f"👤 {persona.name}: {user_msg}")
            
            # Update the last turn with student message
            turns[-1]["student_message"] = user_msg
            
            # Delay for rate limits
            print(f"   ⏳ Waiting {TURN_DELAY}s for rate limits...")
            time.sleep(TURN_DELAY)
            
            # Send response via API
            try:
                continue_response = api_client.send_response(session_id, user_msg)
            except requests.exceptions.RequestException as e:
                print(f"❌ Error sending response: {e}")
                break
            
            agent_msg = continue_response.get("teacher_message", {}).get("text", "")
            learning_state = continue_response.get("learning_state", {})
            session_complete = learning_state.get("session_complete", False)
            last_response = continue_response
            
            # Track this turn
            turns.append({"teacher_message": agent_msg, "student_message": None})
            
            print(f"🤖 Teacher: {agent_msg[:200]}...")
            
            # Validate parameters from API response
            print(f"   🔍 Validating parameters...")
            
            # Build state dict from API response for validation
            simulation_data = continue_response.get("simulation", {})
            current_params = simulation_data.get("current_params", {})
            param_history = simulation_data.get("parameter_history", [])
            simulation_url = simulation_data.get("html_url", "")  # Fixed: API uses 'html_url' not 'url'
            
            state_for_validation = {
                "current_params": current_params,
                "parameter_history": param_history,
                "simulation_url": simulation_url,
            }
            
            validation_result = validator.validate_turn(
                turn_number=turn_count,
                teacher_message=agent_msg,
                state=state_for_validation,
                previous_params=previous_params
            )
            
            if validation_result.passed:
                print(f"   ✅ Validation passed")
            else:
                print(f"   ❌ Validation failed: {len(validation_result.issues)} issues")
                for issue in validation_result.issues:
                    print(f"      • {issue}")
            
            if validation_result.warnings:
                print(f"   ⚠️  {len(validation_result.warnings)} warnings")
                for warning in validation_result.warnings[:2]:  # Show first 2
                    print(f"      • {warning}")
            
            # Update previous params for next turn
            if current_params:
                previous_params = current_params.copy()
            
            # Print progress from API response
            concepts_info = continue_response.get("concepts", {})
            print(f"   📊 Concept: {concepts_info.get('current_index', '?')}/{concepts_info.get('total', '?')} | "
                  f"Understanding: {learning_state.get('understanding_level', '?')} | "
                  f"Strategy: {learning_state.get('strategy', '?')}")
    
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Test interrupted by user (Ctrl+C)")
        print(f"   Saving results collected so far...")
    except Exception as e:
        print(f"\n\n❌ Error during test: {e}")
        print(f"   Saving results collected so far...")
        import traceback
        traceback.print_exc()
    finally:
        # Always save results, even on error
        print(f"\n{'='*70}")
        if session_complete:
            print(f"✅ SESSION COMPLETE after {turn_count} turns")
        else:
            print(f"⚠️  SESSION INCOMPLETE - Stopped after {turn_count} turns")
        print(f"{'='*70}")
    
    # Skip remaining processing if no turns collected (session never started)
    if not turns:
        print("⚠️  No turns to process - session never started properly")
        return
    
    # 7. Print Parameter Validation Summary
    validator.print_summary()
    
    # 8. Build History for Evaluation
    history_for_reports = extract_history_from_api_responses(turns)
    print(f"\n📜 Conversation length: {len(history_for_reports)} messages")
    
    # 9. Compute Session Metrics
    print("\n" + "="*60)
    print("📊 Computing Session Metrics...")
    print("="*60)
    
    session_metrics = None
    try:
        print(f"   ⏳ Waiting {TURN_DELAY}s before metrics computation...")
        time.sleep(TURN_DELAY)
        
        # Get final state from API for quiz score etc.
        try:
            final_api_state = api_client.get_session(session_id)
            session_state = final_api_state.get("learning_state", {})
        except Exception:
            session_state = {}
        
        session_metrics = compute_session_metrics(
            session_id=session_id,
            history=history_for_reports,
            session_state=session_state,
            simulation_id=simulation_id,
            persona_name=persona.name,
        )
    except Exception as e:
        print(f"❌ Error computing metrics: {e}")
        import traceback
        traceback.print_exc()
    
    # 10. Evaluate Educational Quality
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
    
    # 11. Save Reports
    print("\n" + "="*60)
    print("💾 Saving Reports...")
    print("="*60)
    
    os.makedirs("test_reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    report = {
        "test_metadata": {
            "timestamp": datetime.now().isoformat(),
            "mode": "API",
            "api_url": API_BASE_URL,
            "session_id": session_id,
            "simulation_id": simulation_id,
            "simulation_title": simulation_title,
            "total_turns": turn_count,
        },
        "persona": persona.model_dump(),
        "conversation_history": history_for_reports,
        "educational_evaluation": evaluation,
        "parameter_validation": validator.get_summary(),
    }
    
    if session_metrics:
        report["session_metrics"] = session_metrics.model_dump()
    
    report_filename = f"test_report_api_{simulation_id}_{persona.name.lower().replace(' ', '_')}_{timestamp}.json"
    report_path = os.path.join("test_reports", report_filename)
    
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"✅ Report saved to {report_path}")
    
    # 12. Print Final Summary
    print("\n" + "="*70)
    print("📋 FINAL TEST SUMMARY")
    print("="*70)
    print(f"  Session ID:    {session_id}")
    print(f"  Simulation:    {simulation_title} ({simulation_id})")
    print(f"  Persona:       {persona.name}")
    print(f"  Total Turns:   {turn_count}")
    print(f"  Messages:      {len(history_for_reports)}")
    print(f"  API Mode:      {API_BASE_URL}")
    
    # Parameter validation summary
    val_summary = validator.get_summary()
    print(f"\n  🔍 PARAMETER VALIDATION:")
    print(f"  Pass Rate:     {val_summary['pass_rate']*100:.1f}%")
    print(f"  Issues:        {val_summary['total_issues']}")
    print(f"  Warnings:      {val_summary['total_warnings']}")
    print(f"  Param Changes: {val_summary['total_actual_changes']}")
    
    if session_metrics:
        print(f"\n  📊 SESSION METRICS:")
        print(f"  Concepts:      {session_metrics.num_concepts_covered}")
        print(f"  User Type:     {session_metrics.user_type}")
        print(f"  Engagement:    {session_metrics.user_engagement_rating}/5")
        print(f"  Quiz Score:    {session_metrics.quiz_score:.1f}%")
    
    if evaluation and "scores" in evaluation:
        scores = evaluation["scores"]
        avg = evaluation.get("average_score", 0)
        print(f"\n  🎓 PEDAGOGY:")
        print(f"  Average:       {avg}/5")
        for key, val in scores.items():
            print(f"    - {key}: {val}/5")
    
    print(f"\n  📁 Report: {report_path}")
    print("="*70)


if __name__ == "__main__":
    run_test_api()
