"""
Comprehensive Integration Test for Speed Calculator
====================================================
Tests both backend and Streamlit integrations to ensure everything works together.
"""

import sys
from pathlib import Path

print("\n" + "="*80)
print("COMPREHENSIVE INTEGRATION TEST: Speed Calculator")
print("="*80)

# ============================================================================
# TEST 1: Backend Integration (simulations_config.py)
# ============================================================================
print("\n" + "="*80)
print("TEST 1: Backend Integration")
print("="*80)

try:
    from simulations_config import (
        get_simulation, 
        get_concepts, 
        get_quiz_questions, 
        get_parameter_info,
        get_initial_params
    )
    
    # Test simulation exists
    sim = get_simulation("speed_calculator")
    assert sim is not None, "Simulation not found"
    print("✅ Simulation found in backend config")
    
    # Test initial params
    initial_params = get_initial_params("speed_calculator")
    assert "calculationMode" in initial_params, "Missing calculationMode"
    assert "distance" in initial_params, "Missing distance"
    assert "time" in initial_params, "Missing time"
    assert "speed" in initial_params, "Missing speed"
    print(f"✅ Initial params: {initial_params}")
    
    # Test parameter info
    param_info = get_parameter_info("speed_calculator")
    assert len(param_info) == 4, f"Expected 4 params, got {len(param_info)}"
    print(f"✅ Parameter info: {len(param_info)} parameters")
    
    # Test concepts
    concepts = get_concepts("speed_calculator")
    assert len(concepts) == 4, f"Expected 4 concepts, got {len(concepts)}"
    print(f"✅ Concepts: {len(concepts)} concepts defined")
    
    # Test quiz questions
    quiz = get_quiz_questions("speed_calculator")
    assert len(quiz) == 4, f"Expected 4 quiz questions, got {len(quiz)}"
    print(f"✅ Quiz questions: {len(quiz)} questions defined")
    
    print("\n✅ BACKEND INTEGRATION: PASS")
    
except Exception as e:
    print(f"\n❌ BACKEND INTEGRATION: FAIL - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


# ============================================================================
# TEST 2: Streamlit Integration (streamlit_config.py)
# ============================================================================
print("\n" + "="*80)
print("TEST 2: Streamlit Integration")
print("="*80)

try:
    # Add streamlit_app to path
    sys.path.insert(0, str(Path(__file__).parent / "streamlit_app"))
    from streamlit_config import SIMULATIONS, build_simulation_url
    
    # Test simulation exists in Streamlit config
    assert "speed_calculator" in SIMULATIONS, "Simulation not in Streamlit config"
    print("✅ Simulation found in Streamlit config")
    
    config = SIMULATIONS["speed_calculator"]
    
    # Test basic config
    assert config["name"] == "Speed Calculator", "Wrong name"
    assert "base_url" in config, "Missing base_url"
    assert "parameters" in config, "Missing parameters"
    print(f"✅ Config: {config['name']}")
    
    # Test parameters
    params = config["parameters"]
    assert len(params) == 4, f"Expected 4 params, got {len(params)}"
    
    # Test calculationMode parameter (dropdown)
    calc_mode_param = params[0]
    assert calc_mode_param["name"] == "calculationMode", "First param should be calculationMode"
    assert "options" in calc_mode_param, "calculationMode missing options"
    assert len(calc_mode_param["options"]) == 3, "calculationMode should have 3 options"
    assert calc_mode_param["options"] == ["speed", "distance", "time"], "Wrong options"
    print(f"✅ calculationMode: dropdown with {len(calc_mode_param['options'])} options")
    
    # Test numeric parameters (sliders)
    for param in params[1:]:
        assert "min" in param, f"{param['name']} missing min"
        assert "max" in param, f"{param['name']} missing max"
        print(f"✅ {param['name']}: slider ({param['min']}-{param['max']})")
    
    # Test URL building
    test_params = {
        "calculationMode": "distance",
        "distance": 100,
        "time": 4,
        "speed": 80
    }
    url = build_simulation_url("speed_calculator", test_params, auto_start=True)
    assert "calculationMode=distance" in url, "calculationMode not in URL"
    assert "distance=100" in url, "distance not in URL"
    assert "time=4" in url, "time not in URL"
    assert "speed=80" in url, "speed not in URL"
    print(f"✅ URL generation works correctly")
    
    print("\n✅ STREAMLIT INTEGRATION: PASS")
    
except Exception as e:
    print(f"\n❌ STREAMLIT INTEGRATION: FAIL - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


# ============================================================================
# TEST 3: Backend-Streamlit Compatibility
# ============================================================================
print("\n" + "="*80)
print("TEST 3: Backend-Streamlit Compatibility")
print("="*80)

try:
    # Test that initial params from backend match Streamlit config
    backend_params = get_initial_params("speed_calculator")
    streamlit_params = {p["name"]: p["default"] for p in config["parameters"]}
    
    for param_name, backend_value in backend_params.items():
        assert param_name in streamlit_params, f"{param_name} in backend but not Streamlit"
        streamlit_value = streamlit_params[param_name]
        assert backend_value == streamlit_value, f"{param_name}: backend={backend_value}, streamlit={streamlit_value}"
        print(f"✅ {param_name}: {backend_value} == {streamlit_value}")
    
    print("\n✅ COMPATIBILITY CHECK: PASS")
    
except Exception as e:
    print(f"\n❌ COMPATIBILITY CHECK: FAIL - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


# ============================================================================
# TEST 4: HTML Simulation File
# ============================================================================
print("\n" + "="*80)
print("TEST 4: HTML Simulation File")
print("="*80)

try:
    html_file = Path(__file__).parent / "simulations" / "simulation_6_speed_calculator.html"
    assert html_file.exists(), f"HTML file not found: {html_file}"
    print(f"✅ HTML file exists: {html_file.name}")
    
    # Read and check for URL parameter handling
    content = html_file.read_text()
    
    checks = [
        ("getURLParams" in content, "URL parameter parsing function"),
        ("initFromURL" in content, "URL initialization function"),
        ("sendParametersToParent" in content, "postMessage sending function"),
        ("window.addEventListener('message'" in content, "postMessage receiving listener"),
        ("calculationMode" in content, "calculationMode parameter"),
        ("distance" in content, "distance parameter"),
        ("time" in content, "time parameter"),
        ("speed" in content, "speed parameter"),
    ]
    
    for passed, check_name in checks:
        if passed:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}")
            raise AssertionError(f"Missing: {check_name}")
    
    print("\n✅ HTML FILE CHECK: PASS")
    
except Exception as e:
    print(f"\n❌ HTML FILE CHECK: FAIL - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)
print("✅ Backend Integration: COMPLETE")
print("   - simulations_config.py: ✅")
print("   - 4 parameters defined: ✅")
print("   - 4 concepts defined: ✅")
print("   - 4 quiz questions: ✅")
print()
print("✅ Streamlit Integration: COMPLETE")
print("   - streamlit_config.py: ✅")
print("   - Dropdown for calculationMode: ✅")
print("   - Sliders for distance, time, speed: ✅")
print("   - URL generation: ✅")
print()
print("✅ Backend-Streamlit Compatibility: VERIFIED")
print("   - Parameters match: ✅")
print("   - Initial values match: ✅")
print()
print("✅ HTML Simulation: ENHANCED")
print("   - URL parameter parsing: ✅")
print("   - postMessage integration: ✅")
print("   - Bidirectional communication: ✅")
print()
print("="*80)
print("🎉 ALL TESTS PASSED - Speed Calculator is fully integrated!")
print("="*80)
print()
print("Ready to use:")
print("1. Backend: python run_test.py (select speed_calculator)")
print("2. Streamlit: streamlit run streamlit_app/app.py (select Speed Calculator)")
print("3. API: python run_test_api.py (use speed_calculator)")
print()
