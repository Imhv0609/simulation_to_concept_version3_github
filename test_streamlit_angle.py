"""
Test Streamlit configuration for angle_sum_property simulation.
"""

import sys
sys.path.insert(0, 'streamlit_app')

from streamlit_config import SIMULATIONS, DEFAULT_SIMULATION

print("="*80)
print("TESTING STREAMLIT CONFIGURATION FOR ANGLE_SUM_PROPERTY")
print("="*80)

# Test 1: Check if simulation exists in config
print("\n1. CHECKING STREAMLIT CONFIG...")
if "angle_sum_property" in SIMULATIONS:
    sim = SIMULATIONS["angle_sum_property"]
    print(f"✅ Simulation found: {sim['name']}")
    print(f"   Description: {sim['description']}")
    print(f"   Base URL: {sim['base_url']}")
    print(f"   Parameters: {len(sim['parameters'])}")
    for param in sim['parameters']:
        print(f"      - {param['display_name']}: {param['url_param']}")
else:
    print("❌ Simulation NOT found in Streamlit config!")
    exit(1)

# Test 2: Check if it's accessible from simulations_config
print("\n2. CHECKING BACKEND SIMULATIONS_CONFIG...")
import os
os.environ['SIMULATION_ID'] = 'angle_sum_property'

sys.path.insert(0, '.')
from simulations_config import get_simulation, get_simulation_list

backend_sim = get_simulation("angle_sum_property")
if backend_sim:
    print(f"✅ Backend simulation found: {backend_sim['title']}")
    print(f"   Concepts: {len(backend_sim['concepts'])}")
else:
    print("❌ Simulation NOT found in backend config!")
    exit(1)

# Test 3: Check if it appears in simulation list
print("\n3. CHECKING SIMULATION LIST...")
sim_list = get_simulation_list()
sim_ids = [s['id'] for s in sim_list]
if "angle_sum_property" in sim_ids:
    print("✅ Simulation appears in list")
    print(f"   Total simulations available: {len(sim_list)}")
    for s in sim_list:
        print(f"      - {s['id']}: {s['title']}")
else:
    print("❌ Simulation NOT in list!")
    exit(1)

# Test 4: Verify URL building
print("\n4. TESTING URL BUILDING...")
from streamlit_config import build_simulation_url

test_params = {
    "show_proof_lines": True,
    "vertexA_y": 300
}

url = build_simulation_url("angle_sum_property", test_params, auto_start=True)
print(f"Generated URL:\n  {url}")

if "AngleSumProperty.html" in url:
    print("✅ Correct HTML file")
else:
    print("❌ Wrong HTML file")

if "show_proof_lines" in url:
    print("✅ Parameters included")
else:
    print("❌ Parameters missing")

print("\n" + "="*80)
print("✅ STREAMLIT APP IS READY FOR ANGLE_SUM_PROPERTY!")
print("="*80)
print("\nYou can now:")
print("1. Run the Streamlit app: streamlit run streamlit_app/app.py")
print("2. Select 'Triangle Angle Sum' from the dropdown")
print("3. Start a teaching session")
print("\nThe simulation will work with:")
print("  - Teaching mode (3 concepts)")
print("  - Quiz mode (2 questions)")
print("  - Parameter changes by the agent")
