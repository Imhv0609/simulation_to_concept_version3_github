#!/usr/bin/env python3
"""
Comprehensive Test Suite for Brackets & Sign Rules Simulation Integration
==========================================================================
Tests backend config, Streamlit config, and integration points.

Run: python test_brackets_signs_integration.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "streamlit_app"))

def test_backend_configuration():
    """Test that simulation is properly configured in simulations_config.py"""
    print("=" * 70)
    print("BACKEND CONFIGURATION TESTS")
    print("=" * 70)
    
    from simulations_config import SIMULATIONS, QUIZ_QUESTIONS
    
    sim_key = "brackets_signs"
    
    # Test 1: Simulation exists
    assert sim_key in SIMULATIONS, f"❌ Simulation '{sim_key}' not found in SIMULATIONS"
    print(f"✅ Test 1: Simulation '{sim_key}' exists in backend config")
    
    config = SIMULATIONS[sim_key]
    
    # Test 2: Required fields present
    required_fields = ["title", "file", "description", "initial_params", "parameter_info", "concepts"]
    for field in required_fields:
        assert field in config, f"❌ Missing required field: {field}"
    print(f"✅ Test 2: All required fields present: {required_fields}")
    
    # Test 3: Check title and file
    assert config["title"] == "Brackets & Sign Rules", f"❌ Wrong title: {config['title']}"
    assert "ch2_sim2_brackets_signs.html" in config["file"], f"❌ Wrong file: {config['file']}"
    print(f"✅ Test 3: Title and file path correct")
    
    # Test 4: Check parameters
    param_info = config["parameter_info"]
    assert "mode" in param_info, "❌ Missing 'mode' parameter"
    assert "problemIndex" in param_info, "❌ Missing 'problemIndex' parameter"
    print(f"✅ Test 4: Both parameters defined (mode, problemIndex)")
    
    # Test 5: Check parameter ranges
    assert param_info["mode"]["options"] == ["learn", "quiz"], "❌ Wrong mode options"
    assert param_info["problemIndex"]["min"] == 0, "❌ Wrong min for problemIndex"
    assert param_info["problemIndex"]["max"] == 9, "❌ Wrong max for problemIndex"
    print(f"✅ Test 5: Parameter ranges correct (mode: learn/quiz, problemIndex: 0-9)")
    
    # Test 6: Check initial params
    init = config["initial_params"]
    assert init["mode"] == "learn", f"❌ Wrong initial mode: {init['mode']}"
    assert init["problemIndex"] == 0, f"❌ Wrong initial problemIndex: {init['problemIndex']}"
    print(f"✅ Test 6: Initial parameters correct (mode='learn', problemIndex=0)")
    
    # Test 7: Check concepts
    concepts = config["concepts"]
    assert len(concepts) == 4, f"❌ Expected 4 concepts, got {len(concepts)}"
    
    concept_titles = [c["title"] for c in concepts]
    expected_concepts = [
        "Understanding Brackets in Arithmetic",
        "The Minus-Before-Bracket Rule",
        "The Plus-Before-Bracket Rule",
        "Why Signs Flip - The Logic Behind It"
    ]
    for expected in expected_concepts:
        assert expected in concept_titles, f"❌ Missing concept: {expected}"
    print(f"✅ Test 7: All 4 concepts defined correctly")
    
    # Test 8: Quiz questions exist
    assert sim_key in QUIZ_QUESTIONS, f"❌ No quiz questions for '{sim_key}'"
    quiz = QUIZ_QUESTIONS[sim_key]
    assert len(quiz) == 4, f"❌ Expected 4 quiz questions, got {len(quiz)}"
    print(f"✅ Test 8: Quiz questions defined (4 questions)")
    
    # Test 9: Check quiz question structure
    for i, q in enumerate(quiz):
        assert "id" in q, f"❌ Quiz {i}: Missing 'id'"
        assert "challenge" in q, f"❌ Quiz {i}: Missing 'challenge'"
        assert "target_parameters" in q, f"❌ Quiz {i}: Missing 'target_parameters'"
        assert "success_rule" in q, f"❌ Quiz {i}: Missing 'success_rule'"
        assert "hints" in q, f"❌ Quiz {i}: Missing 'hints'"
    print(f"✅ Test 9: All quiz questions have required structure")
    
    # Test 10: Check quiz progression
    q1_params = quiz[0]["target_parameters"]
    q2_params = quiz[1]["target_parameters"]
    q3_params = quiz[2]["target_parameters"]
    q4_params = quiz[3]["target_parameters"]
    
    assert "mode" in q1_params and "problemIndex" in q1_params, "❌ Q1: Wrong params"
    assert "mode" in q2_params and "problemIndex" in q2_params, "❌ Q2: Wrong params"
    assert "mode" in q3_params and "problemIndex" in q3_params, "❌ Q3: Wrong params"
    assert "mode" in q4_params, "❌ Q4: Missing mode param"
    print(f"✅ Test 10: Quiz questions target correct parameters")
    
    print(f"\n{'='*70}")
    print(f"✅ ALL BACKEND TESTS PASSED (10/10)")
    print(f"{'='*70}\n")
    
    return True


def test_streamlit_configuration():
    """Test Streamlit app configuration"""
    print("=" * 70)
    print("STREAMLIT CONFIGURATION TESTS")
    print("=" * 70)
    
    from streamlit_config import SIMULATIONS, get_simulation_config, build_simulation_url
    
    sim_key = "brackets_signs"
    
    # Test 1: Simulation in Streamlit config
    assert sim_key in SIMULATIONS, f"❌ '{sim_key}' not in Streamlit SIMULATIONS"
    print(f"✅ Test 1: Simulation exists in Streamlit config")
    
    config = get_simulation_config(sim_key)
    
    # Test 2: Required Streamlit fields
    required = ["name", "description", "base_url", "parameters"]
    for field in required:
        assert field in config, f"❌ Missing field: {field}"
    print(f"✅ Test 2: All required Streamlit fields present")
    
    # Test 3: Check base URL
    assert "ch2_sim2_brackets_signs.html" in config["base_url"], f"❌ Wrong base_url"
    assert config["base_url"].startswith("https://"), f"❌ base_url should use GitHub Pages"
    print(f"✅ Test 3: Base URL correct (GitHub Pages)")
    
    # Test 4: Check parameters
    params = config["parameters"]
    assert len(params) == 2, f"❌ Expected 2 parameters, got {len(params)}"
    
    param_names = [p["name"] for p in params]
    assert "mode" in param_names, "❌ Missing 'mode' parameter"
    assert "problemIndex" in param_names, "❌ Missing 'problemIndex' parameter"
    print(f"✅ Test 4: Both Streamlit parameters defined")
    
    # Test 5: Check mode parameter config
    mode_param = next(p for p in params if p["name"] == "mode")
    assert mode_param["type"] == "select", f"❌ mode should be 'select' type"
    assert mode_param["options"] == ["learn", "quiz"], f"❌ Wrong mode options"
    assert mode_param["default"] == "learn", f"❌ Wrong mode default"
    print(f"✅ Test 5: Mode parameter correctly configured")
    
    # Test 6: Check problemIndex parameter config
    prob_param = next(p for p in params if p["name"] == "problemIndex")
    assert prob_param["type"] == "slider", f"❌ problemIndex should be 'slider' type"
    assert prob_param["min"] == 0, f"❌ Wrong min for problemIndex"
    assert prob_param["max"] == 9, f"❌ Wrong max for problemIndex"
    assert prob_param["default"] == 0, f"❌ Wrong default for problemIndex"
    print(f"✅ Test 6: ProblemIndex parameter correctly configured")
    
    # Test 7: Test URL building - learn mode, first example
    url1 = build_simulation_url(sim_key, {"mode": "learn", "problemIndex": 0})
    assert "mode=learn" in url1, f"❌ URL missing mode=learn"
    assert "problemIndex=0" in url1, f"❌ URL missing problemIndex=0"
    print(f"✅ Test 7: URL building works for learn mode")
    
    # Test 8: Test URL building - quiz mode
    url2 = build_simulation_url(sim_key, {"mode": "quiz", "problemIndex": 5})
    assert "mode=quiz" in url2, f"❌ URL missing mode=quiz"
    assert "problemIndex=5" in url2, f"❌ URL missing problemIndex=5"
    print(f"✅ Test 8: URL building works for quiz mode")
    
    # Test 9: Check topic
    assert "topic" in config, "❌ Missing 'topic' field"
    assert "Algebra" in config["topic"] or "Brackets" in config["topic"], f"❌ Topic should mention Algebra or Brackets"
    print(f"✅ Test 9: Topic field present and relevant")
    
    # Test 10: Check auto_start_param
    assert "auto_start_param" in config, "❌ Missing 'auto_start_param'"
    assert config["auto_start_param"] is None, f"❌ This simulation shouldn't have autostart"
    print(f"✅ Test 10: AutoStart correctly set to None (not needed for this sim)")
    
    print(f"\n{'='*70}")
    print(f"✅ ALL STREAMLIT TESTS PASSED (10/10)")
    print(f"{'='*70}\n")
    
    return True


def test_integration_points():
    """Test that backend and Streamlit configs are aligned"""
    print("=" * 70)
    print("INTEGRATION TESTS")
    print("=" * 70)
    
    import simulations_config as backend_config
    from streamlit_config import SIMULATIONS as streamlit_sims
    
    sim_key = "brackets_signs"
    
    backend = backend_config.SIMULATIONS[sim_key]
    streamlit = streamlit_sims[sim_key]
    
    # Test 1: Parameter count matches
    backend_params = set(backend["parameter_info"].keys())
    streamlit_params = set(p["name"] for p in streamlit["parameters"])
    
    assert backend_params == streamlit_params, f"❌ Parameter mismatch: backend={backend_params}, streamlit={streamlit_params}"
    print(f"✅ Test 1: Backend and Streamlit have same parameters: {backend_params}")
    
    # Test 2: URL parameter keys match
    for param_name in backend_params:
        backend_url_key = backend["parameter_info"][param_name]["url_key"]
        streamlit_param = next(p for p in streamlit["parameters"] if p["name"] == param_name)
        streamlit_url_key = streamlit_param["url_param"]
        
        assert backend_url_key == streamlit_url_key, f"❌ URL key mismatch for {param_name}"
    print(f"✅ Test 2: URL parameter keys match between backend and Streamlit")
    
    # Test 3: File paths aligned
    backend_file = backend["file"]
    streamlit_url = streamlit["base_url"]
    
    assert "ch2_sim2_brackets_signs.html" in backend_file, f"❌ Backend file wrong"
    assert "ch2_sim2_brackets_signs.html" in streamlit_url, f"❌ Streamlit URL wrong"
    print(f"✅ Test 3: File paths aligned between configs")
    
    # Test 4: Titles similar
    backend_title = backend["title"]
    streamlit_name = streamlit["name"]
    
    assert "Brackets" in backend_title and "Brackets" in streamlit_name, f"❌ Titles don't match theme"
    print(f"✅ Test 4: Titles aligned ('{backend_title}' / '{streamlit_name}')")
    
    print(f"\n{'='*70}")
    print(f"✅ ALL INTEGRATION TESTS PASSED (4/4)")
    print(f"{'='*70}\n")
    
    return True


def test_html_file_exists():
    """Test that HTML file exists and has URL parameter support"""
    print("=" * 70)
    print("HTML FILE TESTS")
    print("=" * 70)
    
    html_file = project_root / "simulations" / "ch2_sim2_brackets_signs.html"
    
    # Test 1: File exists
    assert html_file.exists(), f"❌ HTML file not found: {html_file}"
    print(f"✅ Test 1: HTML file exists at {html_file.name}")
    
    # Test 2: Check for URL parameter support
    content = html_file.read_text()
    
    assert "URLSearchParams" in content, "❌ Missing URLSearchParams code"
    print(f"✅ Test 2: HTML has URLSearchParams support")
    
    # Test 3: Check for getURLParams function
    assert "getURLParams" in content, "❌ Missing getURLParams function"
    print(f"✅ Test 3: HTML has getURLParams function")
    
    # Test 4: Check for postMessage support
    assert "postMessage" in content, "❌ Missing postMessage code"
    print(f"✅ Test 4: HTML has postMessage support for Streamlit")
    
    # Test 5: Check for mode parameter handling
    assert "mode" in content, "❌ HTML doesn't handle 'mode' parameter"
    print(f"✅ Test 5: HTML handles 'mode' parameter")
    
    # Test 6: Check for problemIndex parameter handling
    assert "problemIndex" in content, "❌ HTML doesn't handle 'problemIndex' parameter"
    print(f"✅ Test 6: HTML handles 'problemIndex' parameter")
    
    print(f"\n{'='*70}")
    print(f"✅ ALL HTML FILE TESTS PASSED (6/6)")
    print(f"{'='*70}\n")
    
    return True


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "BRACKETS & SIGN RULES - INTEGRATION TEST SUITE" + " " * 12 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    all_passed = True
    
    try:
        test_backend_configuration()
    except AssertionError as e:
        print(f"\n❌ BACKEND TESTS FAILED: {e}\n")
        all_passed = False
    
    try:
        test_streamlit_configuration()
    except AssertionError as e:
        print(f"\n❌ STREAMLIT TESTS FAILED: {e}\n")
        all_passed = False
    
    try:
        test_integration_points()
    except AssertionError as e:
        print(f"\n❌ INTEGRATION TESTS FAILED: {e}\n")
        all_passed = False
    
    try:
        test_html_file_exists()
    except AssertionError as e:
        print(f"\n❌ HTML FILE TESTS FAILED: {e}\n")
        all_passed = False
    
    print("\n")
    print("╔" + "=" * 68 + "╗")
    if all_passed:
        print("║" + " " * 20 + "✅ ALL TESTS PASSED! ✅" + " " * 25 + "║")
        print("║" + " " * 68 + "║")
        print("║  Total: 30 tests passed" + " " * 43 + "║")
        print("║  - Backend Configuration: 10/10" + " " * 36 + "║")
        print("║  - Streamlit Configuration: 10/10" + " " * 33 + "║")
        print("║  - Integration Tests: 4/4" + " " * 41 + "║")
        print("║  - HTML File Tests: 6/6" + " " * 43 + "║")
        print("║" + " " * 68 + "║")
        print("║  🎉 Brackets & Sign Rules simulation is fully integrated!" + " " * 11 + "║")
    else:
        print("║" + " " * 25 + "❌ SOME TESTS FAILED" + " " * 23 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
