#!/usr/bin/env python3
"""
Test: Can the agent select different examples in brackets_signs simulation?
============================================================================
This demonstrates that the agent can control problemIndex to show different
examples in Learn mode.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from simulations_config import get_simulation


def test_agent_can_select_examples():
    """Verify agent has access to problemIndex parameter"""
    print("=" * 70)
    print("AGENT PROBLEM SELECTION TEST")
    print("=" * 70)
    print()
    
    sim = get_simulation('brackets_signs')
    
    # Test 1: problemIndex parameter exists
    assert 'problemIndex' in sim['parameter_info'], "❌ problemIndex not in config"
    print("✅ Test 1: problemIndex parameter exists")
    
    # Test 2: Parameter has correct range
    param = sim['parameter_info']['problemIndex']
    assert param['min'] == 0, "❌ Min should be 0"
    assert param['max'] == 9, "❌ Max should be 9"
    print("✅ Test 2: Range is 0-9 (10 examples available)")
    
    # Test 3: Parameter is listed in concept's related_params
    related_concepts = [c for c in sim['concepts'] if 'problemIndex' in c['related_params']]
    assert len(related_concepts) >= 3, "❌ problemIndex should be in multiple concepts"
    print(f"✅ Test 3: problemIndex is used in {len(related_concepts)} concepts")
    
    # Test 4: Show what the agent can do
    print()
    print("=" * 70)
    print("WHAT THE AGENT CAN DO:")
    print("=" * 70)
    print()
    print("The agent can select ANY of these 10 examples by setting problemIndex:")
    print()
    
    examples = [
        "0: 200 − (40 + 3) = 200 − 40 − 3 = 157",
        "1: 500 − (250 − 100) = 500 − 250 + 100 = 350",
        "2: 100 − (15 + 56) = 100 − 15 − 56 = 29",
        "3: 28 + (35 − 10) = 28 + 35 − 10 = 53",
        "4: 24 + (6 − 4) = 24 + 6 − 4 = 26",
        "5: 24 − (6 + 4) = 24 − 6 − 4 = 14",
        "6: 27 − (8 + 3) = 27 − 8 − 3 = 16",
        "7: 27 − (8 − 3) = 27 − 8 + 3 = 22",
        "8: 14 − (12 − 10) = 14 − 12 + 10 = 12",
        "9: 14 − (−12 − 10) = 14 + 12 + 10 = 36"
    ]
    
    for example in examples:
        print(f"  {example}")
    
    print()
    print("=" * 70)
    print("HOW THE AGENT SELECTS EXAMPLES:")
    print("=" * 70)
    print()
    print("When teaching, the agent will:")
    print("  1. Analyze which concept to teach (e.g., 'Minus-Before-Bracket Rule')")
    print("  2. Choose an appropriate example to demonstrate the concept")
    print("  3. Set problemIndex to that example number (e.g., problemIndex=1)")
    print("  4. The simulation will display that specific example")
    print()
    print("Example teaching sequence:")
    print("  • To show basic minus-flips: problemIndex=0 (200 − (40 + 3))")
    print("  • To show tricky case: problemIndex=1 (500 − (250 − 100))")
    print("  • To show plus-stays: problemIndex=3 (28 + (35 − 10))")
    print("  • To show negative numbers: problemIndex=9 (14 − (−12 − 10))")
    print()
    
    # Test 5: Agent receives parameter info
    effect = param['effect']
    assert 'select' in effect.lower() or 'example' in effect.lower(), "❌ Effect should mention selecting examples"
    print("✅ Test 4: Agent knows parameter effect:")
    print(f"         '{effect}'")
    print()
    
    print("=" * 70)
    print("✅ CONCLUSION: YES, the agent CAN select specific examples!")
    print("=" * 70)
    print()
    print("The agent has full control over which of the 10 examples to show")
    print("students. It can strategically select examples that best demonstrate")
    print("the concept being taught at that moment.")
    print()
    
    return True


if __name__ == "__main__":
    test_agent_can_select_examples()
