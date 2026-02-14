"""
Test Streamlit Integration for Speed Calculator
================================================
Verify that speed_calculator simulation is properly configured in Streamlit.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "streamlit_app"))

from streamlit_config import SIMULATIONS, build_simulation_url


def test_streamlit_speed_calculator():
    """Test speed_calculator simulation in Streamlit config"""
    
    print("\n" + "="*70)
    print("Testing Speed Calculator Streamlit Integration")
    print("="*70)
    
    # 1. Check if simulation exists
    if "speed_calculator" not in SIMULATIONS:
        print("❌ ERROR: speed_calculator not found in SIMULATIONS!")
        return False
    
    config = SIMULATIONS["speed_calculator"]
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
        "calculationMode": "distance",
        "speed": 80,
        "time": 4,
        "distance": 100
    }
    
    try:
        url = build_simulation_url("speed_calculator", test_params, auto_start=True)
        print(f"   ✅ URL Generated Successfully:")
        print(f"   {url}")
        
        # Check if parameters are in URL
        if "calculationMode=distance" in url and "speed=80" in url and "time=4" in url:
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
        (len(params) == 4, "Has 4 parameters"),
        (params[0]["name"] == "calculationMode", "First param is calculationMode"),
        (params[1]["name"] == "distance", "Second param is distance"),
        (params[2]["name"] == "time", "Third param is time"),
        (params[3]["name"] == "speed", "Fourth param is speed"),
        ("options" in params[0], "calculationMode has options"),
        (len(params[0]["options"]) == 3, "calculationMode has 3 options"),
        (params[1]["min"] == 1, "distance min is 1"),
        (params[1]["max"] == 1000, "distance max is 1000"),
        (params[2]["min"] == 0.1, "time min is 0.1"),
        (params[3]["max"] == 1000, "speed max is 1000"),
        (config.get("topic") == "Speed, Distance & Time Relationships", "Has correct topic"),
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
        print("✅ All checks passed! Speed Calculator is ready in Streamlit.")
        print("\nTo use in Streamlit:")
        print("1. Run: streamlit run streamlit_app/app.py")
        print("2. Select 'Speed Calculator' from simulation dropdown")
        print("3. Use dropdown to select calculation mode (speed/distance/time)")
        print("4. Use sliders to adjust distance, time, and speed values")
        print("="*70)
        return True
    else:
        print("❌ Some checks failed. Please review the configuration.")
        print("="*70)
        return False


if __name__ == "__main__":
    success = test_streamlit_speed_calculator()
    sys.exit(0 if success else 1)
