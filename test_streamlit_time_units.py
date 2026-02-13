"""
Test Streamlit Integration for Time Units
==========================================
Verify that time_units simulation is properly configured in Streamlit.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "streamlit_app"))

from streamlit_config import SIMULATIONS, build_simulation_url


def test_streamlit_time_units():
    """Test time_units simulation in Streamlit config"""
    
    print("\n" + "="*70)
    print("Testing Time Units Streamlit Integration")
    print("="*70)
    
    # 1. Check if simulation exists
    if "time_units" not in SIMULATIONS:
        print("❌ ERROR: time_units not found in SIMULATIONS!")
        return False
    
    config = SIMULATIONS["time_units"]
    print(f"\n✅ Simulation Found: {config['name']}")
    print(f"   Description: {config['description']}")
    print(f"   Base URL: {config['base_url']}")
    print(f"   Topic: {config['topic']}")
    
    # 2. Check parameters
    params = config.get("parameters", [])
    print(f"\n📊 Parameters ({len(params)}):")
    
    for param in params:
        print(f"\n   • {param['name']} ({param['display_name']})")
        print(f"     Default: {param['default']}")
        
        if "options" in param:
            print(f"     Options: {param['options']}")
            if "option_labels" in param:
                print(f"     Labels: {param['option_labels']}")
        else:
            print(f"     Min: {param.get('min')}, Max: {param.get('max')}")
        
        print(f"     URL Param: {param['url_param']}")
    
    # 3. Test URL building
    print("\n🔗 URL Building Test:")
    test_params = {
        "timeValue": 5,
        "timeUnit": "min"
    }
    
    try:
        url = build_simulation_url("time_units", test_params, auto_start=True)
        print(f"   ✅ URL Generated Successfully:")
        print(f"   {url}")
        
        # Check if parameters are in URL
        if "timeValue=5" in url and "timeUnit=min" in url:
            print(f"   ✅ Parameters correctly encoded in URL")
        else:
            print(f"   ❌ Parameters missing from URL")
            return False
            
    except Exception as e:
        print(f"   ❌ URL Building Failed: {e}")
        return False
    
    # 4. Validation checks
    print("\n🔍 Validation Checks:")
    
    checks = [
        ("name" in config, "Has name"),
        ("description" in config, "Has description"),
        ("base_url" in config, "Has base_url"),
        ("parameters" in config, "Has parameters"),
        (len(params) == 2, "Has 2 parameters"),
        (params[0]["name"] == "timeValue", "First param is timeValue"),
        (params[1]["name"] == "timeUnit", "Second param is timeUnit"),
        ("options" in params[1], "timeUnit has options"),
        (len(params[1]["options"]) == 4, "timeUnit has 4 options (h, min, s, ms)"),
        (params[0]["min"] == 0.1, "timeValue min is 0.1"),
        (params[0]["max"] == 100, "timeValue max is 100"),
        (config.get("topic") == "Time Units & SI Standards", "Has correct topic"),
    ]
    
    all_passed = True
    for passed, check_name in checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {check_name}")
        if not passed:
            all_passed = False
    
    # 5. Test all simulation keys
    print(f"\n📋 All Available Simulations ({len(SIMULATIONS)}):")
    for sim_key in SIMULATIONS.keys():
        print(f"   • {sim_key}")
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ All checks passed! Time Units is ready in Streamlit.")
        print("\nTo use in Streamlit:")
        print("1. Run: streamlit run streamlit_app/app.py")
        print("2. Select 'Time Units Converter' from simulation dropdown")
        print("3. Use sliders and dropdown to adjust parameters")
        print("="*70)
        return True
    else:
        print("❌ Some checks failed. Please review the configuration.")
        print("="*70)
        return False


if __name__ == "__main__":
    success = test_streamlit_time_units()
    sys.exit(0 if success else 1)
