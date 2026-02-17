#!/usr/bin/env python3
"""
Test: Verify agent now has access to problem examples
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from simulations_config import get_simulation


def test_problem_examples_available():
    """Test that agent can now see which problems have which rules"""
    print("=" * 70)
    print("TESTING: Agent Access to Problem Examples")
    print("=" * 70)
    print()
    
    sim = get_simulation('brackets_signs')
    
    # Test 1: problem_examples exists
    assert 'problem_examples' in sim, "❌ problem_examples not in config"
    print("✅ Test 1: problem_examples field exists in config")
    
    examples = sim['problem_examples']
    
    # Test 2: Has 10 examples
    assert len(examples) == 10, f"❌ Expected 10 examples, got {len(examples)}"
    print(f"✅ Test 2: Has all 10 examples")
    
    # Test 3: Check problem 2 specifically (the one causing the issue)
    problem_2 = examples[2]
    assert problem_2['index'] == 2, "❌ Wrong index"
    assert problem_2['rule'] == 'minus', f"❌ Problem 2 should have 'minus' rule, got '{problem_2['rule']}'"
    assert '100 − (15 + 56)' in problem_2['expression'], "❌ Wrong expression"
    print(f"✅ Test 3: Problem 2 correctly identified as MINUS rule")
    print(f"         Expression: {problem_2['expression']}")
    print(f"         Rule: {problem_2['rule']}")
    
    # Test 4: Check first PLUS example
    plus_examples = [ex for ex in examples if ex['rule'] == 'plus']
    assert len(plus_examples) == 2, f"❌ Expected 2 PLUS examples, got {len(plus_examples)}"
    first_plus = plus_examples[0]
    assert first_plus['index'] == 3, f"❌ First PLUS should be index 3, got {first_plus['index']}"
    print(f"✅ Test 4: First PLUS example is at index 3 (not 2!)")
    print(f"         Expression: {first_plus['expression']}")
    
    # Test 5: Display what agent will see
    print()
    print("=" * 70)
    print("WHAT THE AGENT NOW SEES:")
    print("=" * 70)
    print()
    
    for ex in examples:
        rule_emoji = "➖" if ex["rule"] == "minus" else "➕"
        rule_label = "MINUS" if ex["rule"] == "minus" else "PLUS"
        print(f"{rule_emoji} Index {ex['index']}: {ex['expression']} ({rule_label} before bracket)")
    
    print()
    print("=" * 70)
    print("✅ FIX VERIFIED!")
    print("=" * 70)
    print()
    print("The agent can now correctly identify:")
    print("  • Problem 2 has MINUS (−) before bracket")
    print("  • Problem 3 has PLUS (+) before bracket")
    print("  • This prevents incorrect statements about sign rules")
    print()
    
    return True


if __name__ == "__main__":
    test_problem_examples_available()
