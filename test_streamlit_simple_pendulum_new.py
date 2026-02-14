"""
Test Script for Simple Pendulum New - Streamlit Configuration
==============================================================
Tests Streamlit integration of simple_pendulum_new simulation.

This verifies:
1. Simulation exists in streamlit_config.py
2. All parameters are configured with correct UI types
3. URL building works correctly
4. Parameter ranges match backend configuration
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "streamlit_app"))

from streamlit_app.streamlit_config import SIMULATIONS as STREAMLIT_SIMS


def test_streamlit_integration():
    """Test Streamlit configuration for simple_pendulum_new"""
    
    print("\n" + "="*70)
    print("TEST 2: Streamlit Integration for Simple Pendulum New")
    print("="*70)
    
    # Check if simulation exists
    if "simple_pendulum_new" not in STREAMLIT_SIMS:
        print("❌ FAIL: Simulation 'simple_pendulum_new' not found in Streamlit config")
        return False
    
    sim_config = STREAMLIT_SIMS["simple_pendulum_new"]
    
    print(f"✅ Simulation found: {sim_config['name']}")
    print(f"   Description: {sim_config['description'][:80]}...")
    print(f"   Base URL: {sim_config['base_url']}")
    print(f"   Topic: {sim_config.get('topic', 'N/A')}")
    
    # Check parameters
    params = sim_config.get("parameters", [])
    print(f"\n✅ Parameters ({len(params)} total):")
    
    for param in params:
        print(f"   - {param['name']}: {param['type']}")
        print(f"      Display: {param['display_name']}")
        print(f"      Range: {param.get('min', 'N/A')} - {param.get('max', 'N/A')} {param.get('unit', '')}")
        print(f"      Default: {param.get('default', 'N/A')}")
        print(f"      URL param: {param['url_param']}")
    
    # Test URL building
    print("\n✅ Testing URL building:")
    
    # Simulate parameter values
    test_values = {
        "length": 150,
        "mass": 120
    }
    
    # Build URL query string
    url_parts = []
    for param in params:
        param_name = param['name']
        if param_name in test_values:
            url_key = param['url_param']
            value = test_values[param_name]
            url_parts.append(f"{url_key}={value}")
    
    url_query = "&".join(url_parts)
    full_url = f"{sim_config['base_url']}?{url_query}"
    
    print(f"   Test values: {test_values}")
    print(f"   Generated URL: {full_url}")
    
    if "length=150" in url_query and "mass=120" in url_query:
        print("   ✅ URL building successful")
    else:
        print("   ❌ URL building failed")
        return False
    
    return True


def test_all_validations():
    """Run all validation checks for Streamlit config"""
    
    print("\n" + "="*70)
    print("STREAMLIT VALIDATION CHECKS FOR SIMPLE_PENDULUM_NEW")
    print("="*70)
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Simulation exists
    total_checks += 1
    if "simple_pendulum_new" in STREAMLIT_SIMS:
        print("✅ Check 1: Simulation exists in Streamlit config")
        checks_passed += 1
    else:
        print("❌ Check 1: Simulation NOT found in Streamlit config")
        return checks_passed, total_checks
    
    sim_config = STREAMLIT_SIMS["simple_pendulum_new"]
    
    # Check 2: Has name
    total_checks += 1
    if sim_config.get("name"):
        print("✅ Check 2: Name present")
        checks_passed += 1
    else:
        print("❌ Check 2: Name missing")
    
    # Check 3: Has description
    total_checks += 1
    if sim_config.get("description"):
        print("✅ Check 3: Description present")
        checks_passed += 1
    else:
        print("❌ Check 3: Description missing")
    
    # Check 4: Has base_url
    total_checks += 1
    if sim_config.get("base_url") == "simulations/simulation_3_pendulum.html":
        print("✅ Check 4: Base URL correct")
        checks_passed += 1
    else:
        print("❌ Check 4: Base URL incorrect or missing")
    
    # Check 5: Has parameters
    total_checks += 1
    params = sim_config.get("parameters", [])
    if len(params) == 2:
        print("✅ Check 5: Has 2 parameters")
        checks_passed += 1
    else:
        print(f"❌ Check 5: Expected 2 parameters, found {len(params)}")
    
    # Check 6: Length parameter exists
    total_checks += 1
    length_param = next((p for p in params if p['name'] == 'length'), None)
    if length_param:
        print("✅ Check 6: Length parameter exists")
        checks_passed += 1
    else:
        print("❌ Check 6: Length parameter missing")
    
    # Check 7: Mass parameter exists
    total_checks += 1
    mass_param = next((p for p in params if p['name'] == 'mass'), None)
    if mass_param:
        print("✅ Check 7: Mass parameter exists")
        checks_passed += 1
    else:
        print("❌ Check 7: Mass parameter missing")
    
    # Check 8: Length is slider type
    total_checks += 1
    if length_param and length_param.get('type') == 'slider':
        print("✅ Check 8: Length is slider type")
        checks_passed += 1
    else:
        print("❌ Check 8: Length should be slider type")
    
    # Check 9: Mass is slider type
    total_checks += 1
    if mass_param and mass_param.get('type') == 'slider':
        print("✅ Check 9: Mass is slider type")
        checks_passed += 1
    else:
        print("❌ Check 9: Mass should be slider type")
    
    # Check 10: Length range correct
    total_checks += 1
    if length_param and length_param.get('min') == 50 and length_param.get('max') == 200:
        print("✅ Check 10: Length range correct (50-200)")
        checks_passed += 1
    else:
        print("❌ Check 10: Length range incorrect")
    
    # Check 11: Mass range correct
    total_checks += 1
    if mass_param and mass_param.get('min') == 50 and mass_param.get('max') == 200:
        print("✅ Check 11: Mass range correct (50-200)")
        checks_passed += 1
    else:
        print("❌ Check 11: Mass range incorrect")
    
    # Check 12: Length default correct
    total_checks += 1
    if length_param and length_param.get('default') == 100:
        print("✅ Check 12: Length default correct (100)")
        checks_passed += 1
    else:
        print("❌ Check 12: Length default incorrect")
    
    # Check 13: Mass default correct
    total_checks += 1
    if mass_param and mass_param.get('default') == 100:
        print("✅ Check 13: Mass default correct (100)")
        checks_passed += 1
    else:
        print("❌ Check 13: Mass default incorrect")
    
    # Check 14: URL param keys correct
    total_checks += 1
    if (length_param and length_param.get('url_param') == 'length' and
        mass_param and mass_param.get('url_param') == 'mass'):
        print("✅ Check 14: URL parameter keys correct")
        checks_passed += 1
    else:
        print("❌ Check 14: URL parameter keys incorrect")
    
    # Check 15: Has topic
    total_checks += 1
    if sim_config.get("topic"):
        print("✅ Check 15: Topic present")
        checks_passed += 1
    else:
        print("❌ Check 15: Topic missing")
    
    return checks_passed, total_checks


def list_available_simulations():
    """List all available simulations in Streamlit config"""
    
    print("\n" + "="*70)
    print("AVAILABLE SIMULATIONS IN STREAMLIT")
    print("="*70)
    
    for idx, (sim_id, sim_config) in enumerate(STREAMLIT_SIMS.items(), 1):
        print(f"{idx}. {sim_id}")
        print(f"   Name: {sim_config.get('name', 'N/A')}")
        print(f"   Params: {len(sim_config.get('parameters', []))}")
        print(f"   Topic: {sim_config.get('topic', 'N/A')}")
    
    print(f"\n✅ Total simulations: {len(STREAMLIT_SIMS)}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("SIMPLE PENDULUM NEW - STREAMLIT CONFIGURATION TEST")
    print("="*70)
    
    # Run main test
    streamlit_success = test_streamlit_integration()
    
    # Run all validations
    checks_passed, total_checks = test_all_validations()
    
    # List all simulations
    list_available_simulations()
    
    # Final result
    print("\n" + "="*70)
    print("FINAL RESULT")
    print("="*70)
    print(f"Validation: {checks_passed}/{total_checks} checks passed")
    
    if streamlit_success and checks_passed == total_checks:
        print("✅ ALL TESTS PASSED")
        print("✅ Simple Pendulum New is fully configured in Streamlit")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)
