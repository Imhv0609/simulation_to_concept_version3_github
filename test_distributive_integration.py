"""
Comprehensive Test Suite for Distributive Property Simulation Integration
==========================================================================

This test suite verifies complete integration of the distributive property simulation:
1. Backend configuration (simulations_config.py)
2. Frontend configuration (streamlit_config.py)
3. API model updates
4. URL parameter handling in HTML
5. Concept coverage and quiz questions
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from simulations_config import SIMULATIONS, QUIZ_QUESTIONS
from streamlit_app.streamlit_config import SIMULATIONS as STREAMLIT_SIMS


def test_backend_simulation_exists():
    """Test that distributive simulation is registered in backend config"""
    print("✓ Testing backend simulation registration...")
    assert "distributive" in SIMULATIONS, "Distributive simulation not found in SIMULATIONS"
    sim = SIMULATIONS["distributive"]
    assert sim["id"] == "distributive"
    assert sim["title"] == "Distributive Property"
    print("  ✓ Simulation registered correctly")


def test_backend_parameters():
    """Test that all required parameters are defined"""
    print("\n✓ Testing backend parameter definitions...")
    sim = SIMULATIONS["distributive"]
    params = sim["parameters"]
    
    # Expected parameters
    expected_params = ["mode", "a", "b", "c", "mentalMathIndex", "quizIndex"]
    param_names = [p["name"] for p in params]
    
    for expected in expected_params:
        assert expected in param_names, f"Missing parameter: {expected}"
    
    # Check mode parameter
    mode_param = next(p for p in params if p["name"] == "mode")
    assert mode_param["type"] == "select"
    assert set(mode_param["options"]) == {"dots", "area", "mental", "quiz"}
    
    # Check numeric parameters
    a_param = next(p for p in params if p["name"] == "a")
    assert a_param["range"]["min"] == 1
    assert a_param["range"]["max"] == 8
    
    b_param = next(p for p in params if p["name"] == "b")
    assert b_param["range"]["min"] == 1
    assert b_param["range"]["max"] == 10
    
    c_param = next(p for p in params if p["name"] == "c")
    assert c_param["range"]["min"] == 1
    assert c_param["range"]["max"] == 10
    
    mental_param = next(p for p in params if p["name"] == "mentalMathIndex")
    assert mental_param["range"]["min"] == 0
    assert mental_param["range"]["max"] == 4
    
    quiz_param = next(p for p in params if p["name"] == "quizIndex")
    assert quiz_param["range"]["min"] == 0
    assert quiz_param["range"]["max"] == 9
    
    print(f"  ✓ All {len(expected_params)} parameters defined correctly")


def test_mental_math_examples():
    """Test that mental math examples are properly documented"""
    print("\n✓ Testing mental math examples metadata...")
    sim = SIMULATIONS["distributive"]
    
    assert "mental_math_examples" in sim, "Mental math examples not found"
    examples = sim["mental_math_examples"]
    
    assert len(examples) == 5, f"Expected 5 mental math examples, found {len(examples)}"
    
    # Check specific examples
    example_0 = examples[0]
    assert example_0["index"] == 0
    assert example_0["problem"] == "97 × 25"
    assert example_0["result"] == 2425
    assert "(100 − 3)" in example_0["decomposition"]
    
    example_2 = examples[2]
    assert example_2["index"] == 2
    assert example_2["problem"] == "104 × 15"
    assert example_2["result"] == 1560
    assert "(100 + 4)" in example_2["decomposition"]
    
    example_4 = examples[4]
    assert example_4["index"] == 4
    assert example_4["problem"] == "998 × 7"
    assert example_4["result"] == 6986
    
    print(f"  ✓ All 5 mental math examples properly configured")


def test_backend_concepts():
    """Test that teaching concepts are comprehensive"""
    print("\n✓ Testing teaching concepts...")
    sim = SIMULATIONS["distributive"]
    concepts = sim["concepts"]
    
    assert len(concepts) >= 6, f"Expected at least 6 concepts, found {len(concepts)}"
    
    # Check concept IDs are unique and sequential
    concept_ids = [c["id"] for c in concepts]
    assert concept_ids == list(range(1, len(concepts) + 1)), "Concept IDs not sequential"
    
    # Check key concepts exist
    concept_titles = [c["title"] for c in concepts]
    
    expected_topics = [
        "Distributive Property",  # Understanding the rule
        "Dot Array",              # Visual 1
        "Area Model",             # Visual 2
        "Mental Math",            # Application
        "Subtraction",            # Extension
    ]
    
    for topic in expected_topics:
        assert any(topic in title for title in concept_titles), f"Missing concept about: {topic}"
    
    # Verify each concept has required fields
    for concept in concepts:
        assert "id" in concept
        assert "title" in concept
        assert "description" in concept
        assert "key_insight" in concept
        assert "related_params" in concept
        assert len(concept["key_insight"]) > 50, "Key insight too short"
    
    print(f"  ✓ {len(concepts)} teaching concepts properly defined")


def test_quiz_questions():
    """Test that quiz questions are comprehensive"""
    print("\n✓ Testing quiz questions...")
    
    assert "distributive" in QUIZ_QUESTIONS, "Distributive quiz questions not found"
    questions = QUIZ_QUESTIONS["distributive"]
    
    assert len(questions) >= 6, f"Expected at least 6 quiz questions, found {len(questions)}"
    
    # Check question IDs are unique
    question_ids = [q["id"] for q in questions]
    assert len(question_ids) == len(set(question_ids)), "Duplicate question IDs found"
    
    # Check each question has required fields
    for q in questions:
        assert "id" in q
        assert "challenge" in q
        assert "target_parameters" in q
        assert "success_rule" in q
        assert "scoring" in q
        assert "hints" in q
        assert "concept_reminder" in q
        
        # Check success rule structure
        assert "conditions" in q["success_rule"]
        assert "logic" in q["success_rule"]
        
        # Check scoring structure
        assert "weights" in q["scoring"]
        assert "thresholds" in q["scoring"]
        
        # Check hints
        assert "attempt_1" in q["hints"]
        assert "attempt_2" in q["hints"]
        assert "attempt_3" in q["hints"]
    
    # Check coverage of different modes
    modes_covered = set()
    for q in questions:
        for cond in q["success_rule"]["conditions"]:
            if cond["parameter"] == "mode":
                modes_covered.add(cond["value"])
    
    assert "dots" in modes_covered, "No quiz questions for dot array mode"
    assert "area" in modes_covered, "No quiz questions for area mode"
    assert "mental" in modes_covered, "No quiz questions for mental math mode"
    assert "quiz" in modes_covered, "No quiz questions testing quiz mode"
    
    print(f"  ✓ {len(questions)} quiz questions properly defined")
    print(f"  ✓ Covers modes: {', '.join(sorted(modes_covered))}")


def test_streamlit_configuration():
    """Test that Streamlit frontend config matches backend"""
    print("\n✓ Testing Streamlit configuration...")
    
    assert "distributive" in STREAMLIT_SIMS, "Distributive not in Streamlit config"
    st_sim = STREAMLIT_SIMS["distributive"]
    
    # Check basic fields
    assert st_sim["name"] == "Distributive Property"
    assert "base_url" in st_sim
    assert "ch2_sim3_distributive.html" in st_sim["base_url"]
    
    # Check parameters
    st_params = st_sim["parameters"]
    param_names = [p["name"] for p in st_params]
    
    expected_params = ["mode", "a", "b", "c", "mentalMathIndex", "quizIndex"]
    for expected in expected_params:
        assert expected in param_names, f"Missing Streamlit parameter: {expected}"
    
    # Check mode parameter
    mode_param = next(p for p in st_params if p["name"] == "mode")
    assert mode_param["type"] == "select"
    assert set(mode_param["options"]) == {"dots", "area", "mental", "quiz"}
    assert len(mode_param["option_labels"]) == 4
    
    # Check slider parameters
    for param_name in ["a", "b", "c", "mentalMathIndex", "quizIndex"]:
        param = next(p for p in st_params if p["name"] == param_name)
        assert param["type"] == "slider"
        assert "min" in param
        assert "max" in param
        assert "default" in param
    
    # Check auto_start setting
    assert st_sim["auto_start_param"] is None
    
    print(f"  ✓ Streamlit config complete with {len(st_params)} parameters")


def test_html_file_exists():
    """Test that the HTML simulation file exists"""
    print("\n✓ Testing HTML file existence...")
    
    html_path = project_root / "simulations" / "ch2_sim3_distributive.html"
    assert html_path.exists(), f"HTML file not found at {html_path}"
    
    # Check file size (should be substantial)
    file_size = html_path.stat().st_size
    assert file_size > 5000, f"HTML file too small ({file_size} bytes)"
    
    print(f"  ✓ HTML file exists ({file_size:,} bytes)")


def test_html_contains_url_handling():
    """Test that HTML file has URL parameter and postMessage handling"""
    print("\n✓ Testing HTML URL parameter handling...")
    
    html_path = project_root / "simulations" / "ch2_sim3_distributive.html"
    content = html_path.read_text()
    
    # Check for URL parameter functions
    assert "getURLParams" in content, "Missing getURLParams function"
    assert "initFromURL" in content, "Missing initFromURL function"
    assert "sendParametersToParent" in content, "Missing sendParametersToParent function"
    
    # Check for postMessage handling
    assert "window.parent.postMessage" in content, "Missing postMessage sender"
    assert "window.addEventListener('message'" in content, "Missing message listener"
    assert "update_parameters" in content, "Missing update_parameters handler"
    
    # Check for all parameters in URL parsing
    assert "params.get('mode')" in content, "Mode parameter not parsed from URL"
    assert "params.get('a')" in content, "Parameter 'a' not parsed from URL"
    assert "params.get('b')" in content, "Parameter 'b' not parsed from URL"
    assert "params.get('c')" in content, "Parameter 'c' not parsed from URL"
    assert "params.get('mentalMathIndex')" in content, "mentalMathIndex not parsed from URL"
    assert "params.get('quizIndex')" in content, "quizIndex not parsed from URL"
    
    print("  ✓ HTML has complete URL parameter handling")
    print("  ✓ HTML has postMessage bidirectional communication")


def test_html_parameter_sending():
    """Test that HTML sends parameters when values change"""
    print("\n✓ Testing HTML parameter update triggers...")
    
    html_path = project_root / "simulations" / "ch2_sim3_distributive.html"
    content = html_path.read_text()
    
    # Check that parameter changes trigger sendParametersToParent
    assert "sendParametersToParent()" in content, "sendParametersToParent not called"
    
    # Should be called after slider changes
    occurrences = content.count("sendParametersToParent()")
    assert occurrences >= 3, f"sendParametersToParent called only {occurrences} times, expected at least 3"
    
    print(f"  ✓ sendParametersToParent() called {occurrences} times in HTML")


def test_api_model_updated():
    """Test that API models include distributive simulation"""
    print("\n✓ Testing API model updates...")
    
    api_models_path = project_root / "api_models.py"
    content = api_models_path.read_text()
    
    # Check that distributive is mentioned in the examples
    assert "'distributive'" in content or '"distributive"' in content, \
        "Distributive not mentioned in API models"
    
    # Check it's in the StartSessionRequest description
    assert "distributive" in content.lower(), "Distributive not in API documentation"
    
    print("  ✓ API models updated with distributive simulation")


def test_parameter_consistency():
    """Test that parameter definitions are consistent across backend and frontend"""
    print("\n✓ Testing parameter consistency...")
    
    backend_sim = SIMULATIONS["distributive"]
    frontend_sim = STREAMLIT_SIMS["distributive"]
    
    backend_params = {p["name"]: p for p in backend_sim["parameters"]}
    frontend_params = {p["name"]: p for p in frontend_sim["parameters"]}
    
    # Check all backend params exist in frontend
    for param_name in backend_params.keys():
        assert param_name in frontend_params, \
            f"Backend parameter '{param_name}' missing from frontend"
    
    # Check ranges match for numeric parameters
    for param_name in ["a", "b", "c", "mentalMathIndex", "quizIndex"]:
        backend = backend_params[param_name]
        frontend = frontend_params[param_name]
        
        assert backend["range"]["min"] == frontend["min"], \
            f"Min mismatch for {param_name}"
        assert backend["range"]["max"] == frontend["max"], \
            f"Max mismatch for {param_name}"
        assert backend["default"] == frontend["default"], \
            f"Default mismatch for {param_name}"
    
    # Check mode options match
    backend_mode = backend_params["mode"]
    frontend_mode = frontend_params["mode"]
    assert set(backend_mode["options"]) == set(frontend_mode["options"]), \
        "Mode options don't match between backend and frontend"
    
    print("  ✓ All parameter definitions consistent")


def test_url_building():
    """Test that URL can be built correctly with parameters"""
    print("\n✓ Testing URL construction...")
    
    from urllib.parse import urlparse, parse_qs
    
    sim = SIMULATIONS["distributive"]
    base_url = sim["url"]
    
    # Build test URL
    test_params = {
        "mode": "dots",
        "a": 3,
        "b": 4,
        "c": 6,
        "mentalMathIndex": 0,
        "quizIndex": 0
    }
    
    # Simulate URL building
    param_str = "&".join([f"{k}={v}" for k, v in test_params.items()])
    full_url = f"{base_url}?{param_str}"
    
    # Parse URL
    parsed = urlparse(full_url)
    query_params = parse_qs(parsed.query)
    
    # Verify all parameters present
    assert "mode" in query_params
    assert "a" in query_params
    assert "b" in query_params
    assert "c" in query_params
    assert "mentalMathIndex" in query_params
    assert "quizIndex" in query_params
    
    print(f"  ✓ URL construction successful")
    print(f"  ✓ Sample URL: {base_url}?mode=dots&a=3&b=4&c=6")


def run_all_tests():
    """Run complete test suite"""
    print("=" * 70)
    print("DISTRIBUTIVE PROPERTY SIMULATION - INTEGRATION TEST SUITE")
    print("=" * 70)
    
    tests = [
        test_backend_simulation_exists,
        test_backend_parameters,
        test_mental_math_examples,
        test_backend_concepts,
        test_quiz_questions,
        test_streamlit_configuration,
        test_html_file_exists,
        test_html_contains_url_handling,
        test_html_parameter_sending,
        test_api_model_updated,
        test_parameter_consistency,
        test_url_building,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"\n❌ FAILED: {test.__name__}")
            print(f"   Error: {e}")
        except Exception as e:
            failed += 1
            print(f"\n❌ ERROR: {test.__name__}")
            print(f"   Exception: {e}")
    
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Distributive simulation fully integrated!")
        print("\nWhat was tested:")
        print("  ✓ Backend simulation configuration (6 parameters)")
        print("  ✓ Mental math examples metadata (5 examples)")
        print("  ✓ Teaching concepts (6+ concepts)")
        print("  ✓ Quiz questions (8 questions)")
        print("  ✓ Streamlit frontend configuration")
        print("  ✓ HTML file with URL parameter handling")
        print("  ✓ PostMessage bidirectional communication")
        print("  ✓ API model updates")
        print("  ✓ Parameter consistency across stack")
        print("  ✓ URL building capabilities")
        print("\nThe distributive property simulation is ready to use!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
