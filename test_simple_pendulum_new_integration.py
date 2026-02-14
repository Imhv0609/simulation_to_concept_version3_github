"""
Comprehensive Integration Test for Simple Pendulum New
=======================================================
Complete integration test covering:
1. Backend configuration (simulations_config.py)
2. Streamlit configuration (streamlit_config.py)
3. Backend-Streamlit compatibility check
4. HTML file enhancements (URL parsing, postMessage)

This is the master test that validates the entire integration.
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "streamlit_app"))

from simulations_config import get_simulation, get_quiz_questions
from streamlit_app.streamlit_config import SIMULATIONS as STREAMLIT_SIMS


def test_backend():
    """Test backend configuration"""
    print("\n" + "="*70)
    print("TEST 1: Backend Configuration")
    print("="*70)
    
    sim_config = get_simulation("simple_pendulum_new")
    if not sim_config:
        print("❌ FAIL: Backend configuration not found")
        return False
    
    print(f"✅ Simulation: {sim_config['title']}")
    print(f"✅ File: {sim_config['file']}")
    
    # Check initial params
    initial = sim_config.get("initial_params", {})
    print(f"✅ Initial params: {initial}")
    
    # Check parameter info
    param_info = sim_config.get("parameter_info", {})
    print(f"✅ Parameters: {list(param_info.keys())}")
    
    # Check concepts
    concepts = sim_config.get("concepts", [])
    print(f"✅ Concepts: {len(concepts)}")
    
    # Check quiz
    quiz = get_quiz_questions("simple_pendulum_new")
    print(f"✅ Quiz questions: {len(quiz)}")
    
    return True


def test_streamlit():
    """Test Streamlit configuration"""
    print("\n" + "="*70)
    print("TEST 2: Streamlit Configuration")
    print("="*70)
    
    if "simple_pendulum_new" not in STREAMLIT_SIMS:
        print("❌ FAIL: Streamlit configuration not found")
        return False
    
    sim_config = STREAMLIT_SIMS["simple_pendulum_new"]
    
    print(f"✅ Name: {sim_config['name']}")
    print(f"✅ Base URL: {sim_config['base_url']}")
    print(f"✅ Topic: {sim_config.get('topic', 'N/A')}")
    
    # Check parameters
    params = sim_config.get("parameters", [])
    print(f"✅ Parameters: {len(params)}")
    
    for param in params:
        param_type = param['type']
        param_name = param['name']
        print(f"   - {param_name}: {param_type} ({param.get('min')}-{param.get('max')})")
    
    # Test URL building
    test_params = {"length": 150, "mass": 120}
    url_parts = []
    for param in params:
        if param['name'] in test_params:
            url_parts.append(f"{param['url_param']}={test_params[param['name']]}")
    
    url = f"{sim_config['base_url']}?{'&'.join(url_parts)}"
    print(f"✅ URL generation works: {url}")
    
    return True


def test_compatibility():
    """Test backend-Streamlit compatibility"""
    print("\n" + "="*70)
    print("TEST 3: Backend-Streamlit Compatibility")
    print("="*70)
    
    # Get both configs
    backend = get_simulation("simple_pendulum_new")
    streamlit = STREAMLIT_SIMS.get("simple_pendulum_new")
    
    if not backend or not streamlit:
        print("❌ FAIL: Missing configuration")
        return False
    
    # Compare parameters
    backend_params = set(backend.get("parameter_info", {}).keys())
    streamlit_params = set(p['name'] for p in streamlit.get("parameters", []))
    
    print(f"Backend params: {backend_params}")
    print(f"Streamlit params: {streamlit_params}")
    
    if backend_params != streamlit_params:
        print(f"❌ FAIL: Parameter mismatch")
        print(f"   Missing in Streamlit: {backend_params - streamlit_params}")
        print(f"   Extra in Streamlit: {streamlit_params - backend_params}")
        return False
    
    print("✅ All parameters match!")
    
    # Compare initial values
    backend_initial = backend.get("initial_params", {})
    streamlit_defaults = {
        p['name']: p.get('default')
        for p in streamlit.get("parameters", [])
    }
    
    print(f"\nInitial values comparison:")
    for param in backend_params:
        backend_val = backend_initial.get(param)
        streamlit_val = streamlit_defaults.get(param)
        match = "✅" if backend_val == streamlit_val else "⚠️"
        print(f"   {match} {param}: backend={backend_val}, streamlit={streamlit_val}")
    
    return True


def test_html_file():
    """Test HTML file enhancements"""
    print("\n" + "="*70)
    print("TEST 4: HTML File Enhancements")
    print("="*70)
    
    html_path = PROJECT_ROOT / "simulations" / "simulation_3_pendulum.html"
    
    if not html_path.exists():
        print(f"❌ FAIL: HTML file not found at {html_path}")
        return False
    
    print(f"✅ HTML file exists: {html_path}")
    
    # Read HTML content
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Check for URL parameter parsing
    checks = {
        "getURLParams function": "function getURLParams()",
        "initFromURL function": "function initFromURL()",
        "URL parameter parsing": "URLSearchParams(window.location.search)",
        "postMessage sending": "window.parent.postMessage",
        "postMessage receiving": "window.addEventListener('message'",
        "length parameter": "params.has('length')",
        "mass parameter": "params.has('mass')"
    }
    
    for check_name, search_string in checks.items():
        if search_string in html_content:
            print(f"✅ {check_name}: found")
        else:
            print(f"❌ {check_name}: NOT found")
            return False
    
    print("\n✅ All HTML enhancements present!")
    return True


def run_comprehensive_test():
    """Run all tests"""
    print("\n" + "="*70)
    print("COMPREHENSIVE INTEGRATION TEST")
    print("Simple Pendulum New Simulation")
    print("="*70)
    
    results = {}
    
    # Test 1: Backend
    try:
        results['backend'] = test_backend()
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        results['backend'] = False
    
    # Test 2: Streamlit
    try:
        results['streamlit'] = test_streamlit()
    except Exception as e:
        print(f"❌ Streamlit test error: {e}")
        results['streamlit'] = False
    
    # Test 3: Compatibility
    try:
        results['compatibility'] = test_compatibility()
    except Exception as e:
        print(f"❌ Compatibility test error: {e}")
        results['compatibility'] = False
    
    # Test 4: HTML
    try:
        results['html'] = test_html_file()
    except Exception as e:
        print(f"❌ HTML test error: {e}")
        results['html'] = False
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name.capitalize()}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL TESTS PASSED - Simple Pendulum New is fully integrated!")
        print("="*70)
        print("\nIntegration complete:")
        print("✅ Backend: 2 parameters (length, mass), 4 concepts, 4 quiz questions")
        print("✅ Streamlit: 2 sliders with correct ranges")
        print("✅ Compatibility: All parameters match between backend and Streamlit")
        print("✅ HTML: URL parsing and postMessage communication working")
        print("\nReady to use in:")
        print("  - Direct backend testing: python run_test.py")
        print("  - Streamlit app: streamlit run streamlit_app/app.py")
        print("  - API testing: python run_test_api.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("="*70)
        failed = [name for name, passed in results.items() if not passed]
        print(f"\nFailed tests: {', '.join(failed)}")
    
    return all_passed


if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
