"""
End-to-end test: Verify API returns correct concepts for each simulation.
This simulates what the Android app will receive.
"""

import os
os.environ['SIMULATION_ID'] = 'simple_pendulum'  # Set default

from api_integration import create_teaching_session
from simulations_config import get_simulation

def test_api_concepts():
    """Test that API returns correct concepts for each simulation."""
    
    print("\n" + "="*80)
    print("TESTING API CONCEPT LOADING FOR EACH SIMULATION")
    print("="*80 + "\n")
    
    simulations_to_test = [
        "simple_pendulum",
        "earth_rotation_revolution", 
        "light_shadows"
    ]
    
    all_passed = True
    
    for sim_id in simulations_to_test:
        print(f"\n{'─'*80}")
        print(f"Testing API for: {sim_id}")
        print(f"{'─'*80}\n")
        
        # Get expected config
        expected_config = get_simulation(sim_id)
        expected_title = expected_config['title']
        expected_concepts = expected_config['concepts']
        expected_file = expected_config['file']
        
        print(f"Expected simulation: {expected_title}")
        print(f"Expected HTML file: {expected_file}")
        print(f"Expected {len(expected_concepts)} concepts")
        
        # Call API (this is what Android app will call)
        try:
            thread_id, response = create_teaching_session(
                simulation_id=sim_id,
                student_id=f"test_student_{sim_id}"
            )
            
            print(f"\n✅ Session created: {thread_id}")
            
            # Verify response
            sim_info = response['simulation']
            concepts_info = response['concepts']
            
            # Check 1: Correct simulation ID
            if sim_info['id'] == sim_id:
                print(f"  ✓ Simulation ID: {sim_info['id']}")
            else:
                print(f"  ✗ Wrong ID: got {sim_info['id']}, expected {sim_id}")
                all_passed = False
            
            # Check 2: Correct title
            if sim_info['title'] == expected_title:
                print(f"  ✓ Title: {sim_info['title']}")
            else:
                print(f"  ✗ Wrong title: got '{sim_info['title']}', expected '{expected_title}'")
                all_passed = False
            
            # Check 3: Correct HTML file in URL
            if expected_file in sim_info['html_url']:
                print(f"  ✓ HTML file: {expected_file} in URL")
            else:
                print(f"  ✗ Wrong file: expected '{expected_file}' in URL")
                print(f"    Got: {sim_info['html_url']}")
                all_passed = False
            
            # Check 4: Correct number of concepts
            total_concepts = concepts_info['total']
            if total_concepts == len(expected_concepts):
                print(f"  ✓ Concept count: {total_concepts}")
            else:
                print(f"  ✗ Wrong count: got {total_concepts}, expected {len(expected_concepts)}")
                all_passed = False
            
            # Check 5: First concept matches
            current_concept = concepts_info['current_concept']
            if current_concept:
                expected_first = expected_concepts[0]['title']
                actual_first = current_concept['title']
                if actual_first == expected_first:
                    print(f"  ✓ First concept: \"{actual_first}\"")
                else:
                    print(f"  ✗ Wrong concept: got \"{actual_first}\", expected \"{expected_first}\"")
                    all_passed = False
            
            # Check 6: Current params match simulation's initial params
            current_params = sim_info['current_params']
            expected_params = expected_config['initial_params']
            if set(current_params.keys()) == set(expected_params.keys()):
                print(f"  ✓ Parameters: {list(current_params.keys())}")
            else:
                print(f"  ✗ Wrong params: got {list(current_params.keys())}, expected {list(expected_params.keys())}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("🎉 ALL API TESTS PASSED! Ready for Android integration.".center(80))
        print("Each simulation returns correct concepts, URLs, and parameters.".center(80))
    else:
        print("❌ SOME TESTS FAILED".center(80))
    print("="*80 + "\n")
    
    return all_passed

if __name__ == "__main__":
    import sys
    success = test_api_concepts()
    sys.exit(0 if success else 1)
