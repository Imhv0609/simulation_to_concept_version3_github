"""
Test script to verify simulation URLs are generated correctly for each simulation.
Run this to check if the bug is fixed before deploying to production.
"""

import os
os.environ['SIMULATION_ID'] = 'simple_pendulum'  # Set default

from config import build_simulation_url
from simulations_config import SIMULATIONS

print("\n" + "="*80)
print("TESTING SIMULATION URL GENERATION")
print("="*80 + "\n")

# Test parameters for each simulation type
test_cases = {
    "simple_pendulum": {
        "params": {"length": 5, "number_of_oscillations": 10},
        "expected_file": "simple_pendulum.html"
    },
    "earth_rotation_revolution": {
        "params": {"rotation_angle": 0, "revolution_angle": 90},
        "expected_file": "rotAndRev.html"
    },
    "light_shadows": {
        "params": {"light_source_distance": 50, "object_position": 25},
        "expected_file": "lightsShadows.html"
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
    
    # Build URL with simulation_id parameter
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
    sim_config = SIMULATIONS[sim_id]
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

print("\n" + "="*80)
if all_passed:
    print("🎉 ALL TESTS PASSED! URLs are generated correctly for each simulation.")
else:
    print("❌ SOME TESTS FAILED! Check the output above.")
print("="*80 + "\n")
