"""
Test Script for Simple Pendulum New Simulation - Backend Configuration
========================================================================
Tests backend integration of simple_pendulum_new simulation.

This verifies:
1. Simulation exists in simulations_config.py
2. All required parameters are configured
3. Concepts are defined
4. Quiz questions are present
5. Parameter ranges and defaults are correct
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from simulations_config import get_simulation, get_quiz_questions


def test_backend_integration():
    """Test backend configuration for simple_pendulum_new"""
    
    print("\n" + "="*70)
    print("TEST 1: Backend Integration for Simple Pendulum New")
    print("="*70)
    
    # Get simulation config
    sim_config = get_simulation("simple_pendulum_new")
    
    if not sim_config:
        print("❌ FAIL: Simulation 'simple_pendulum_new' not found in config")
        return False
    
    print(f"✅ Simulation found: {sim_config['title']}")
    print(f"   File: {sim_config['file']}")
    print(f"   Description length: {len(sim_config['description'])} chars")
    
    # Check initial params
    initial_params = sim_config.get("initial_params", {})
    print(f"\n✅ Initial params: {initial_params}")
    
    expected_params = ["length", "mass"]
    param_info = sim_config.get("parameter_info", {})
    
    print(f"\n✅ Parameter info ({len(param_info)} params):")
    for param_name, info in param_info.items():
        print(f"   - {param_name}: {info.get('label')} ({info.get('range')})")
    
    # Verify all expected params exist
    missing_params = [p for p in expected_params if p not in param_info]
    if missing_params:
        print(f"❌ FAIL: Missing parameters: {missing_params}")
        return False
    
    # Check concepts
    concepts = sim_config.get("concepts", [])
    print(f"\n✅ Concepts ({len(concepts)} total):")
    for concept in concepts:
        print(f"   - Concept {concept['id']}: {concept['title']}")
    
    if len(concepts) < 4:
        print(f"⚠️  WARNING: Expected at least 4 concepts, found {len(concepts)}")
    
    # Check quiz questions
    quiz_questions = get_quiz_questions("simple_pendulum_new")
    print(f"\n✅ Quiz questions ({len(quiz_questions)} total):")
    for q in quiz_questions:
        print(f"   - {q['id']}: {q['challenge'][:60]}...")
    
    if len(quiz_questions) < 4:
        print(f"⚠️  WARNING: Expected at least 4 quiz questions, found {len(quiz_questions)}")
    
    # Verify parameter ranges
    print("\n✅ Parameter details:")
    for param_name in expected_params:
        info = param_info[param_name]
        print(f"   - {param_name}:")
        print(f"      Label: {info.get('label')}")
        print(f"      Range: {info.get('range')}")
        print(f"      Min: {info.get('min')}, Max: {info.get('max')}")
        print(f"      URL key: {info.get('url_key')}")
        print(f"      Effect: {info.get('effect', '')[:80]}...")
    
    # Summary
    print("\n" + "="*70)
    print("BACKEND INTEGRATION TEST SUMMARY")
    print("="*70)
    print(f"✅ Simulation: simple_pendulum_new")
    print(f"✅ Title: {sim_config['title']}")
    print(f"✅ File: {sim_config['file']}")
    print(f"✅ Parameters: {len(param_info)} (length, mass)")
    print(f"✅ Concepts: {len(concepts)}")
    print(f"✅ Quiz Questions: {len(quiz_questions)}")
    print(f"✅ Initial params: length={initial_params.get('length')}, mass={initial_params.get('mass')}")
    
    # All checks passed
    return True


def test_all_validations():
    """Run all validation checks"""
    
    print("\n" + "="*70)
    print("VALIDATION CHECKS FOR SIMPLE_PENDULUM_NEW")
    print("="*70)
    
    sim_config = get_simulation("simple_pendulum_new")
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Simulation exists
    total_checks += 1
    if sim_config:
        print("✅ Check 1: Simulation config exists")
        checks_passed += 1
    else:
        print("❌ Check 1: Simulation config NOT found")
    
    # Check 2: Has title
    total_checks += 1
    if sim_config and sim_config.get("title"):
        print("✅ Check 2: Title present")
        checks_passed += 1
    else:
        print("❌ Check 2: Missing title")
    
    # Check 3: Has file path
    total_checks += 1
    if sim_config and sim_config.get("file") == "simulations/simulation_3_pendulum.html":
        print("✅ Check 3: Correct file path")
        checks_passed += 1
    else:
        print("❌ Check 3: Incorrect or missing file path")
    
    # Check 4: Has description
    total_checks += 1
    if sim_config and len(sim_config.get("description", "")) > 100:
        print("✅ Check 4: Description present (sufficient length)")
        checks_passed += 1
    else:
        print("❌ Check 4: Description missing or too short")
    
    # Check 5: Has length parameter
    total_checks += 1
    if sim_config and "length" in sim_config.get("parameter_info", {}):
        print("✅ Check 5: Length parameter configured")
        checks_passed += 1
    else:
        print("❌ Check 5: Length parameter missing")
    
    # Check 6: Has mass parameter
    total_checks += 1
    if sim_config and "mass" in sim_config.get("parameter_info", {}):
        print("✅ Check 6: Mass parameter configured")
        checks_passed += 1
    else:
        print("❌ Check 6: Mass parameter missing")
    
    # Check 7: Length has correct range
    total_checks += 1
    if sim_config:
        length_info = sim_config.get("parameter_info", {}).get("length", {})
        if length_info.get("min") == 50 and length_info.get("max") == 200:
            print("✅ Check 7: Length range correct (50-200)")
            checks_passed += 1
        else:
            print("❌ Check 7: Length range incorrect")
    
    # Check 8: Mass has correct range
    total_checks += 1
    if sim_config:
        mass_info = sim_config.get("parameter_info", {}).get("mass", {})
        if mass_info.get("min") == 50 and mass_info.get("max") == 200:
            print("✅ Check 8: Mass range correct (50-200)")
            checks_passed += 1
        else:
            print("❌ Check 8: Mass range incorrect")
    
    # Check 9: Has initial params
    total_checks += 1
    if sim_config:
        initial = sim_config.get("initial_params", {})
        if "length" in initial and "mass" in initial:
            print("✅ Check 9: Initial parameters set")
            checks_passed += 1
        else:
            print("❌ Check 9: Initial parameters missing")
    
    # Check 10: Has concepts
    total_checks += 1
    if sim_config and len(sim_config.get("concepts", [])) >= 4:
        print("✅ Check 10: Concepts defined (4)")
        checks_passed += 1
    else:
        print("❌ Check 10: Insufficient concepts")
    
    # Check 11: Has quiz questions
    total_checks += 1
    quiz_questions = get_quiz_questions("simple_pendulum_new")
    if len(quiz_questions) >= 4:
        print("✅ Check 11: Quiz questions defined (4)")
        checks_passed += 1
    else:
        print("❌ Check 11: Insufficient quiz questions")
    
    # Check 12: Quiz questions have proper structure
    total_checks += 1
    if quiz_questions:
        all_valid = all(
            "id" in q and "challenge" in q and "target_parameters" in q 
            for q in quiz_questions
        )
        if all_valid:
            print("✅ Check 12: Quiz questions properly structured")
            checks_passed += 1
        else:
            print("❌ Check 12: Quiz questions have structural issues")
    
    # Check 13: All quiz questions reference valid parameters
    total_checks += 1
    if quiz_questions and sim_config:
        valid_params = set(sim_config.get("parameter_info", {}).keys())
        all_valid = True
        for q in quiz_questions:
            target_params = q.get("target_parameters", [])
            if not all(p in valid_params for p in target_params):
                all_valid = False
                break
        if all_valid:
            print("✅ Check 13: Quiz targets reference valid parameters")
            checks_passed += 1
        else:
            print("❌ Check 13: Quiz questions reference invalid parameters")
    
    # Check 14: Parameter URL keys match
    total_checks += 1
    if sim_config:
        param_info = sim_config.get("parameter_info", {})
        url_keys_match = (
            param_info.get("length", {}).get("url_key") == "length" and
            param_info.get("mass", {}).get("url_key") == "mass"
        )
        if url_keys_match:
            print("✅ Check 14: URL parameter keys correct")
            checks_passed += 1
        else:
            print("❌ Check 14: URL parameter keys incorrect")
    
    # Check 15: Has cannot_demonstrate list
    total_checks += 1
    if sim_config and "cannot_demonstrate" in sim_config:
        print("✅ Check 15: Cannot demonstrate list present")
        checks_passed += 1
    else:
        print("❌ Check 15: Cannot demonstrate list missing")
    
    print("\n" + "="*70)
    print(f"VALIDATION RESULTS: {checks_passed}/{total_checks} checks passed")
    print("="*70)
    
    if checks_passed == total_checks:
        print("🎉 ALL CHECKS PASSED - Backend configuration complete!")
        return True
    else:
        print(f"⚠️  {total_checks - checks_passed} checks failed")
        return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("SIMPLE PENDULUM NEW - BACKEND CONFIGURATION TEST")
    print("="*70)
    
    # Run main test
    backend_success = test_backend_integration()
    
    # Run all validations
    validation_success = test_all_validations()
    
    # Final result
    print("\n" + "="*70)
    print("FINAL RESULT")
    print("="*70)
    
    if backend_success and validation_success:
        print("✅ ALL TESTS PASSED")
        print("✅ Simple Pendulum New is fully configured in backend")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)
