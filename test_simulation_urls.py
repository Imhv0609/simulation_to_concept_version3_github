"""
Test script to verify simulation URLs AND concepts are generated correctly.
Run this to check if the bugs are fixed before deploying to production.
"""

import os
os.environ['SIMULATION_ID'] = 'simple_pendulum'  # Set default

from config import build_simulation_url
from simulations_config import SIMULATIONS, get_simulation

print("\n" + "="*80)
print("TESTING SIMULATION URL GENERATION AND CONCEPTS")
print("="*80 + "\n")

# Test parameters for each simulation type
test_cases = {
    "simple_pendulum": {
        "params": {"length": 5, "number_of_oscillations": 10},
        "expected_file": "simple_pendulum.html",
        "expected_concept_keywords": ["pendulum", "length", "time period"]
    },
    "earth_rotation_revolution": {
        "params": {"rotation_angle": 0, "revolution_angle": 90},
        "expected_file": "rotAndRev.html",
        "expected_concept_keywords": ["rotation", "revolution", "earth", "day", "year"]
    },
    "light_shadows": {
        "params": {"light_source_distance": 50, "object_position": 25},
        "expected_file": "lightsShadows.html",
        "expected_concept_keywords": ["light", "shadow", "distance"]
    }
}

all_passed = True

for sim_id, test_data in test_cases.items():
    if sim_id not in SIMULATIONS:
        print(f"⚠️  {sim_id}: Not configured in simulations_config.py")
        continue
    
    print(f"\n{'─'*80}")
    print(f"Testing: {sim_id}")
    print(f"{'─'*80}")
    
    # Get simulation config dynamically
    sim_config = get_simulation(sim_id)
    
    # ============ TEST 1: URL Generation ============
    url = build_simulation_url(
        params=test_data["params"],
        autostart=True,
        simulation_id=sim_id
    )
    
    print(f"Generated URL:\n  {url}\n")
    
    # Check if correct file is in the URL
    expected_file = test_data["expected_file"]
    if expected_file in url:
        print(f"✅ PASS: Contains correct file '{expected_file}'")
    else:
        print(f"❌ FAIL: Expected '{expected_file}' in URL")
        all_passed = False
    
    # Check if simulation_id specific params are in URL
    param_info = sim_config.get("parameter_info", {})
    
    print(f"\nParameter mapping check:")
    for param_name, param_value in test_data["params"].items():
        if param_name in param_info:
            url_key = param_info[param_name].get("url_key", param_name)
            expected_param = f"{url_key}={param_value}"
            if expected_param in url:
                print(f"  ✓ {param_name} → {url_key}={param_value}")
            else:
                print(f"  ✗ Missing: {expected_param}")
                all_passed = False
    
    # ============ TEST 2: Concepts Check ============
    concepts = sim_config.get("concepts", [])
    print(f"\nConcepts check ({len(concepts)} concepts):")
    
    # Combine all concept text for keyword search
    all_concept_text = " ".join([
        f"{c['title']} {c['description']} {c['key_insight']}" 
        for c in concepts
    ]).lower()
    
    expected_keywords = test_data.get("expected_concept_keywords", [])
    for keyword in expected_keywords:
        if keyword.lower() in all_concept_text:
            print(f"  ✓ Found keyword: '{keyword}'")
        else:
            print(f"  ✗ Missing keyword: '{keyword}'")
            all_passed = False
    
    # Show first concept as sanity check
    if concepts:
        print(f"\n  First concept: \"{concepts[0]['title']}\"")
        print(f"    → {concepts[0]['key_insight']}")
    
    # ============ TEST 3: Initial params check ============
    initial_params = sim_config.get("initial_params", {})
    print(f"\nInitial params from config: {initial_params}")

print("\n" + "="*80)
if all_passed:
    print("🎉 ALL TESTS PASSED! URLs and concepts are correct for each simulation.")
else:
    print("❌ SOME TESTS FAILED! Check the output above.")
print("="*80 + "\n")
