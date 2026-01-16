"""
Direct test: Exactly simulates what API returns for earth_rotation_revolution.
This shows the raw response the Android app should receive.
"""

import os
import json

# Set environment before any imports
os.environ['SIMULATION_ID'] = 'simple_pendulum'

from api_integration import create_teaching_session

print("="*80)
print("TESTING: What does API return for earth_rotation_revolution?")
print("="*80)

# This is exactly what happens when Android calls:
# POST /api/session/start {"simulation_id": "earth_rotation_revolution"}

thread_id, response = create_teaching_session(
    simulation_id="earth_rotation_revolution",  # <-- Android sends this
    student_id="android_user_123"
)

print("\n" + "="*80)
print("RESPONSE THAT API RETURNS TO ANDROID:")
print("="*80)

# Extract just the simulation part
sim = response['simulation']
print(f"\nsimulation.id: {sim['id']}")
print(f"simulation.title: {sim['title']}")
print(f"simulation.html_url: {sim['html_url']}")
print(f"simulation.current_params: {sim['current_params']}")

# Check concepts
concepts = response['concepts']
print(f"\nconcepts.total: {concepts['total']}")
print(f"concepts.current_concept.title: {concepts['current_concept']['title']}")

print("\n" + "="*80)
print("VERIFICATION:")
print("="*80)

# Verify correctness
errors = []

if "rotAndRev.html" not in sim['html_url']:
    errors.append(f"❌ WRONG URL: Expected 'rotAndRev.html', got: {sim['html_url']}")
else:
    print("✅ URL contains 'rotAndRev.html'")

if sim['id'] != 'earth_rotation_revolution':
    errors.append(f"❌ WRONG ID: Expected 'earth_rotation_revolution', got: {sim['id']}")
else:
    print("✅ ID is 'earth_rotation_revolution'")

if 'rotationSpeed' not in sim['current_params']:
    errors.append(f"❌ WRONG PARAMS: Expected 'rotationSpeed', got: {list(sim['current_params'].keys())}")
else:
    print("✅ Params include 'rotationSpeed'")

if "Rotation" not in concepts['current_concept']['title']:
    errors.append(f"❌ WRONG CONCEPT: Expected Earth concept, got: {concepts['current_concept']['title']}")
else:
    print("✅ First concept is about Earth rotation")

print("\n" + "="*80)
if errors:
    print("❌ STILL BROKEN:")
    for e in errors:
        print(f"  {e}")
else:
    print("✅ ALL CORRECT! API returns proper earth_rotation_revolution data.")
print("="*80)

# Print full JSON for debugging
print("\n\nFULL SIMULATION JSON (for developer):")
print(json.dumps(sim, indent=2))
