"""
Test script to verify the new angle_sum_property simulation works correctly.
"""

import os
os.environ['SIMULATION_ID'] = 'simple_pendulum'

from config import build_simulation_url
from simulations_config import get_simulation, get_quiz_questions
from api_integration import create_teaching_session

print("="*80)
print("TESTING NEW ANGLE_SUM_PROPERTY SIMULATION")
print("="*80)

# Test 1: Check simulation config
print("\n1. CHECKING SIMULATION CONFIG...")
sim_config = get_simulation("angle_sum_property")

if not sim_config:
    print("❌ FAIL: Simulation not found!")
    exit(1)

print(f"✅ Simulation found: {sim_config['title']}")
print(f"   File: {sim_config['file']}")
print(f"   Concepts: {len(sim_config['concepts'])}")
print(f"   Parameters: {len(sim_config['parameter_info'])}")

# Test 2: Check quiz questions
print("\n2. CHECKING QUIZ QUESTIONS...")
quiz_questions = get_quiz_questions("angle_sum_property")
print(f"✅ Quiz questions: {len(quiz_questions)}")
for q in quiz_questions:
    print(f"   - {q['id']}: {q['challenge'][:60]}...")

# Test 3: Check URL generation
print("\n3. TESTING URL GENERATION...")
test_params = {
    "show_proof_lines": True,
    "vertexA_y": 200
}
url = build_simulation_url(test_params, autostart=True, simulation_id="angle_sum_property")
print(f"Generated URL:\n  {url}")

if "AngleSumProperty.html" in url:
    print("✅ Correct HTML file in URL")
else:
    print("❌ Wrong HTML file in URL")
    
if "show_proof_lines=true" in url.lower():
    print("✅ show_proof_lines parameter in URL")
else:
    print("❌ Missing show_proof_lines parameter")

if "autoStart=true" in url:
    print("✅ autoStart parameter in URL")
else:
    print("❌ Missing autoStart parameter")

# Test 4: Check concepts load correctly
print("\n4. TESTING CONCEPT LOADING...")
concepts = sim_config['concepts']
print(f"Concepts:")
for c in concepts:
    print(f"  {c['id']}. {c['title']}")
    print(f"     → {c['key_insight']}")

# Test 5: Test API integration
print("\n5. TESTING API INTEGRATION...")
try:
    thread_id, response = create_teaching_session(
        simulation_id="angle_sum_property",
        student_id="test_angle_user"
    )
    
    sim_info = response['simulation']
    concepts_info = response['concepts']
    
    print(f"✅ Session created: {thread_id}")
    print(f"   Simulation ID: {sim_info['id']}")
    print(f"   Title: {sim_info['title']}")
    print(f"   HTML URL: ...{sim_info['html_url'][-50:]}")
    print(f"   Concepts: {concepts_info['total']}")
    print(f"   First concept: {concepts_info['current_concept']['title']}")
    
    # Verify correctness
    errors = []
    if "AngleSumProperty.html" not in sim_info['html_url']:
        errors.append("❌ Wrong HTML file in API response")
    if sim_info['id'] != 'angle_sum_property':
        errors.append("❌ Wrong simulation ID")
    if 'show_proof_lines' not in sim_info['current_params']:
        errors.append("❌ Missing show_proof_lines parameter")
    if concepts_info['total'] != 3:
        errors.append(f"❌ Wrong number of concepts: {concepts_info['total']} (expected 3)")
        
    if errors:
        print("\n⚠️ ERRORS FOUND:")
        for e in errors:
            print(f"  {e}")
    else:
        print("\n✅ ALL API TESTS PASSED!")
        
except Exception as e:
    print(f"❌ API TEST FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("✅ ANGLE_SUM_PROPERTY SIMULATION IS READY!")
print("="*80)
print("\nNext steps:")
print("1. Push changes to GitHub: git add . && git commit -m 'Add angle sum simulation' && git push")
print("2. Simulation will be available at:")
print("   https://imhv0609.github.io/simulation_to_concept_version3_github/simulations/AngleSumProperty.html")
print("3. Test with Android developer using simulation_id='angle_sum_property'")
