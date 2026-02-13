"""
Quick test to debug session start issue
"""

import os
os.environ['SIMULATION_ID'] = 'speed_race'

from api_integration import create_teaching_session

try:
    print("Testing session creation...")
    session_id, response = create_teaching_session(
        simulation_id="speed_race",
        student_id="test_student"
    )
    print(f"✅ Success! Session ID: {session_id}")
    print(f"Teacher message: {response['teacher_message']['text'][:100]}...")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
