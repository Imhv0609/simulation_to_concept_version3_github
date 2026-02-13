"""
Test Time Units Simulation Integration
=======================================
Quick test to verify time_units simulation is properly integrated.
"""

import sys
from simulations_config import get_simulation, get_concepts, get_quiz_questions, get_parameter_info

def test_time_units_simulation():
    """Test that time_units simulation is properly configured"""
    
    print("\n" + "="*70)
    print("Testing Time Units Simulation Integration")
    print("="*70)
    
    # 1. Test simulation exists
    sim = get_simulation("time_units")
    if not sim:
        print("❌ ERROR: time_units simulation not found!")
        return False
    
    print(f"\n✅ Simulation Found: {sim['title']}")
    print(f"   File: {sim['file']}")
    
    # 2. Test parameters
    params = get_parameter_info("time_units")
    print(f"\n📊 Parameters ({len(params)}):")
    for param_name, param_info in params.items():
        print(f"   • {param_name}: {param_info['label']}")
        print(f"     Range: {param_info['range']}")
        print(f"     URL Key: {param_info['url_key']}")
    
    # 3. Test concepts
    concepts = get_concepts("time_units")
    print(f"\n🎯 Concepts ({len(concepts)}):")
    for concept in concepts:
        print(f"   {concept['id']}. {concept['title']}")
        print(f"      Key Insight: {concept['key_insight']}")
    
    # 4. Test quiz questions
    quiz = get_quiz_questions("time_units")
    print(f"\n❓ Quiz Questions ({len(quiz)}):")
    for q in quiz:
        print(f"   {q['id']}: {q['challenge'][:80]}...")
    
    # 5. Verify required fields
    print("\n🔍 Validation Checks:")
    
    checks = [
        ("title" in sim, "Has title"),
        ("file" in sim, "Has file path"),
        ("description" in sim, "Has description"),
        ("cannot_demonstrate" in sim, "Has cannot_demonstrate list"),
        ("initial_params" in sim, "Has initial_params"),
        ("parameter_info" in sim, "Has parameter_info"),
        ("concepts" in sim, "Has concepts"),
        (len(sim["concepts"]) == 4, "Has 4 concepts"),
        (len(params) == 2, "Has 2 parameters"),
        (len(quiz) == 4, "Has 4 quiz questions"),
        ("timeValue" in params, "Has timeValue parameter"),
        ("timeUnit" in params, "Has timeUnit parameter"),
    ]
    
    all_passed = True
    for passed, check_name in checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ All checks passed! Time Units simulation is ready to use.")
        print("="*70)
        return True
    else:
        print("❌ Some checks failed. Please review the configuration.")
        print("="*70)
        return False


if __name__ == "__main__":
    success = test_time_units_simulation()
    sys.exit(0 if success else 1)
