"""
Test Speed Calculator Simulation Integration
=============================================
Quick test to verify speed_calculator simulation is properly integrated.
"""

import sys
from simulations_config import get_simulation, get_concepts, get_quiz_questions, get_parameter_info

def test_speed_calculator_simulation():
    """Test that speed_calculator simulation is properly configured"""
    
    print("\n" + "="*70)
    print("Testing Speed Calculator Simulation Integration")
    print("="*70)
    
    # 1. Test simulation exists
    sim = get_simulation("speed_calculator")
    if not sim:
        print("❌ ERROR: speed_calculator simulation not found!")
        return False
    
    print(f"\n✅ Simulation Found: {sim['title']}")
    print(f"   File: {sim['file']}")
    
    # 2. Test parameters
    params = get_parameter_info("speed_calculator")
    print(f"\n📊 Parameters ({len(params)}):")
    for param_name, param_info in params.items():
        print(f"   • {param_name}: {param_info['label']}")
        print(f"     Range: {param_info['range']}")
        print(f"     URL Key: {param_info['url_key']}")
    
    # 3. Test concepts
    concepts = get_concepts("speed_calculator")
    print(f"\n🎯 Concepts ({len(concepts)}):")
    for concept in concepts:
        print(f"   {concept['id']}. {concept['title']}")
        print(f"      Key Insight: {concept['key_insight'][:80]}...")
    
    # 4. Test quiz questions
    quiz = get_quiz_questions("speed_calculator")
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
        (len(params) == 4, "Has 4 parameters"),
        (len(quiz) == 4, "Has 4 quiz questions"),
        ("calculationMode" in params, "Has calculationMode parameter"),
        ("distance" in params, "Has distance parameter"),
        ("time" in params, "Has time parameter"),
        ("speed" in params, "Has speed parameter"),
        (sim["initial_params"]["calculationMode"] == "speed", "Initial mode is 'speed'"),
        (sim["initial_params"]["distance"] == 100, "Initial distance is 100"),
        (sim["initial_params"]["time"] == 2, "Initial time is 2"),
        (sim["initial_params"]["speed"] == 50, "Initial speed is 50"),
    ]
    
    all_passed = True
    for passed, check_name in checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ All checks passed! Speed Calculator simulation is ready to use.")
        print("="*70)
        return True
    else:
        print("❌ Some checks failed. Please review the configuration.")
        print("="*70)
        return False


if __name__ == "__main__":
    success = test_speed_calculator_simulation()
    sys.exit(0 if success else 1)
