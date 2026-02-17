"""
Agent Teaching Demonstration - Distributive Property Simulation
================================================================

This demonstration shows how the teaching agent can strategically use
the distributive property simulation's multiple modes to teach concepts
progressively.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from simulations_config import SIMULATIONS


def demonstrate_teaching_strategies():
    """
    Show various teaching strategies the agent can employ using
    different visualization modes and parameter combinations.
    """
    
    sim = SIMULATIONS["distributive"]
    concepts = sim["concepts"]
    mental_math = sim["mental_math_examples"]
    
    print("=" * 80)
    print("DISTRIBUTIVE PROPERTY - AGENT TEACHING STRATEGIES")
    print("=" * 80)
    
    # ========================================================================
    # STRATEGY 1: Start with Visual - Dot Array
    # ========================================================================
    print("\n📚 STRATEGY 1: Building Understanding with Dot Array")
    print("-" * 80)
    print("\n🎯 Goal: Help student visualize the distributive property")
    print("\n💡 Agent Action: Use simple numbers in dot array mode")
    print("   Parameters: mode=dots, a=2, b=3, c=5")
    print("\n🗣️ Agent might say:")
    print("   'Let's visualize 2 × (3 + 5). Look at the dot array:'")
    print("   '- You see 2 ROWS'")
    print("   '- Each row has 3 BLUE dots and 5 GREEN dots'")
    print("   '- Blue total: 2 × 3 = 6 dots'")
    print("   '- Green total: 2 × 5 = 10 dots'")
    print("   '- TOTAL: 6 + 10 = 16 dots'")
    print("   '- This is the same as 2 × 8 = 16!'")
    
    concept = concepts[1]  # Dot array concept
    print(f"\n📖 Teaching Concept: {concept['title']}")
    print(f"   {concept['key_insight'][:150]}...")
    
    # ========================================================================
    # STRATEGY 2: Same Concept, Different Visualization
    # ========================================================================
    print("\n\n📚 STRATEGY 2: Reinforcing with Area Model")
    print("-" * 80)
    print("\n🎯 Goal: Show the SAME concept in a different way")
    print("\n💡 Agent Action: Switch to area mode, keep same numbers")
    print("   Parameters: mode=area, a=2, b=3, c=5")
    print("\n🗣️ Agent might say:")
    print("   'Now let's see the SAME problem as a rectangle!'")
    print("   '- Rectangle height: 2 units'")
    print("   '- Rectangle width: 8 units (3 + 5)'")
    print("   '- Blue section area: 2 × 3 = 6 square units'")
    print("   '- Green section area: 2 × 5 = 10 square units'")
    print("   '- Total area: 16 square units'")
    print("   '- Different picture, SAME math!'")
    
    concept = concepts[2]  # Area model concept
    print(f"\n📖 Teaching Concept: {concept['title']}")
    print(f"   Key insight: Rectangle splits into two parts that add up to whole")
    
    # ========================================================================
    # STRATEGY 3: Progressive Complexity
    # ========================================================================
    print("\n\n📚 STRATEGY 3: Increasing Complexity")
    print("-" * 80)
    print("\n🎯 Goal: Build confidence with larger numbers")
    print("\n💡 Agent Action: Increase to a=4, b=6, c=7")
    print("   Parameters: mode=dots, a=4, b=6, c=7")
    print("\n🗣️ Agent might say:")
    print("   'Great! Now you understand the pattern. Let's try bigger numbers:'")
    print("   '4 × (6 + 7) = 4 × 13 = 52'")
    print("   'Breaking it down: 4 × 6 = 24 (blue) and 4 × 7 = 28 (green)'")
    print("   '24 + 28 = 52 ✓'")
    print("   'The property works for ANY numbers!'")
    
    # ========================================================================
    # STRATEGY 4: Real-World Application - Mental Math
    # ========================================================================
    print("\n\n📚 STRATEGY 4: Real-World Mental Math Application")
    print("-" * 80)
    print("\n🎯 Goal: Show WHY this matters - practical mental math")
    print("\n💡 Agent Action: Switch to mental math mode")
    print("   Parameters: mode=mental, mentalMathIndex=0")
    
    example = mental_math[0]
    print(f"\n🧮 Example: {example['problem']}")
    print("\n🗣️ Agent might say:")
    print("   'Now let's see the POWER of distributive property!'")
    print(f"   'Imagine you need to calculate {example['problem']}'")
    print(f"   'That seems hard, right? But watch this trick:'")
    print(f"   '97 is close to 100, so let's think: 97 = 100 − 3'")
    print(f"   'Now we can use distributive property:'")
    print(f"   '{example['decomposition']} × 25'")
    print(f"   '= 100 × 25 − 3 × 25'")
    print(f"   '= 2500 − 75'")
    print(f"   '= {example['result']}'")
    print("   'You just did a hard multiplication in your head!'")
    
    concept = concepts[3]  # Mental math concept
    print(f"\n📖 Teaching Concept: {concept['title']}")
    
    # ========================================================================
    # STRATEGY 5: Different Mental Math Pattern - Addition
    # ========================================================================
    print("\n\n📚 STRATEGY 5: Mental Math with Addition")
    print("-" * 80)
    print("\n🎯 Goal: Show it works for numbers ABOVE round numbers too")
    print("\n💡 Agent Action: Change to example with addition")
    print("   Parameters: mode=mental, mentalMathIndex=2")
    
    example = mental_math[2]
    print(f"\n🧮 Example: {example['problem']}")
    print("\n🗣️ Agent might say:")
    print("   'The trick works both ways!'")
    print(f"   '{example['problem']} seems hard'")
    print(f"   'But 104 = 100 + 4, so:'")
    print(f"   '{example['decomposition']} × 15'")
    print(f"   '= 100 × 15 + 4 × 15'")
    print(f"   '= 1500 + 60'")
    print(f"   '= {example['result']}'")
    print("   'Whether you ADD or SUBTRACT, distributive property helps!'")
    
    # ========================================================================
    # STRATEGY 6: Extreme Example - Very Large Numbers
    # ========================================================================
    print("\n\n📚 STRATEGY 6: Challenge with Large Numbers")
    print("-" * 80)
    print("\n🎯 Goal: Show power with impressive calculation")
    print("\n💡 Agent Action: Show the 998 × 7 example")
    print("   Parameters: mode=mental, mentalMathIndex=4")
    
    example = mental_math[4]
    print(f"\n🧮 Example: {example['problem']}")
    print("\n🗣️ Agent might say:")
    print("   'Ready for something impressive?'")
    print(f"   '{example['problem']} looks impossible to do mentally!'")
    print(f"   'But 998 = 1000 − 2, so:'")
    print(f"   '{example['decomposition']} × 7'")
    print(f"   '= 1000 × 7 − 2 × 7'")
    print(f"   '= 7000 − 14'")
    print(f"   '= {example['result']}'")
    print("   'With this property, you can be a mental math wizard!'")
    
    # ========================================================================
    # STRATEGY 7: Testing Understanding - Quiz Mode
    # ========================================================================
    print("\n\n📚 STRATEGY 7: Assessing Understanding")
    print("-" * 80)
    print("\n🎯 Goal: Check if student grasped the concept")
    print("\n💡 Agent Action: Switch to quiz mode")
    print("   Parameters: mode=quiz, quizIndex=0")
    print("\n🗣️ Agent might say:")
    print("   'You've learned a lot! Let's test your understanding.'")
    print("   'Try answering these questions in quiz mode.'")
    print("   'They'll help you remember the key rules.'")
    
    # ========================================================================
    # STRATEGY 8: Subtraction with Distributive Property
    # ========================================================================
    print("\n\n📚 STRATEGY 8: Extending to Subtraction")
    print("-" * 80)
    print("\n🎯 Goal: Show distributive property works with subtraction too")
    print("\n💡 Agent Action: Use area model with different values")
    print("   Parameters: mode=area, a=5, b=9, c=2")
    print("\n🗣️ Agent might say:")
    print("   'The distributive property isn't just for addition!'")
    print("   'It works with subtraction too: a × (b − c) = a × b − a × c'")
    print("   'Example: 5 × (9 − 2) = 5 × 7 = 35'")
    print("   'But also: 5 × 9 − 5 × 2 = 45 − 10 = 35 ✓'")
    
    concept = concepts[4]  # Subtraction concept
    print(f"\n📖 Teaching Concept: {concept['title']}")
    
    # ========================================================================
    # Summary of Agent Capabilities
    # ========================================================================
    print("\n\n" + "=" * 80)
    print("AGENT TEACHING CAPABILITIES SUMMARY")
    print("=" * 80)
    
    print("\n🎨 VISUALIZATION MODES (mode parameter):")
    print("   • dots  → Visual with colored dot arrays (concrete)")
    print("   • area  → Visual with rectangle areas (geometric)")
    print("   • mental → Real-world mental math examples (practical)")
    print("   • quiz  → Interactive self-assessment (testing)")
    
    print("\n📊 PARAMETER CONTROL (for dots/area modes):")
    print("   • a (1-8)   → Number of rows/multiplier")
    print("   • b (1-10)  → Blue columns/first addend")
    print("   • c (1-10)  → Green columns/second addend")
    print("   • → Agent can choose simple (2×(3+5)) or complex (8×(10+9))")
    
    print("\n🧮 MENTAL MATH EXAMPLES (mentalMathIndex 0-4):")
    for i, ex in enumerate(mental_math):
        print(f"   • [{i}] {ex['problem']:12s} = {ex['result']:5d} "
              f"using {ex['decomposition']}")
    
    print("\n📝 QUIZ MODE (quizIndex 0-9):")
    print("   • 10 interactive questions testing:")
    print("     - Filling in missing operators (+, −, ×)")
    print("     - Identifying which number distributes")
    print("     - Number decomposition strategies")
    
    print("\n🎯 TEACHING STRATEGIES DEMONSTRATED:")
    strategies = [
        "1. Visual introduction (dots)",
        "2. Same concept, different view (area)",
        "3. Progressive complexity (larger numbers)",
        "4. Real-world application (mental math)",
        "5. Pattern variation (addition vs subtraction)",
        "6. Impressive calculations (large numbers)",
        "7. Assessment (quiz mode)",
        "8. Concept extension (subtraction distribution)"
    ]
    for strategy in strategies:
        print(f"   ✓ {strategy}")
    
    print("\n💡 WHY MULTIPLE MODES MATTER:")
    print("   Different students learn differently:")
    print("   • Visual learners → dots/area modes show concrete representation")
    print("   • Practical learners → mental math shows real usefulness")
    print("   • Abstract learners → can jump straight to algebraic rule")
    print("   • Agent adapts approach based on student responses!")
    
    print("\n🔍 EXAMPLE ADAPTIVE TEACHING FLOW:")
    print("   1. Start with simple dots: 2×(3+5) - build confidence")
    print("   2. Switch to area: same problem, different picture")
    print("   3. Increase complexity: 4×(6+7) - test understanding")
    print("   4. Show practical use: 97×25 mental math - motivation")
    print("   5. Give quiz: check mastery")
    print("   6. If struggling: back to simpler visualizations")
    print("   7. If excelling: challenge with 998×7")
    
    print("\n" + "=" * 80)
    print("🎉 The agent has RICH control over this simulation!")
    print("   Multiple modes, adjustable complexity, diverse examples,")
    print("   and strategic parameter choices enable personalized teaching.")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_teaching_strategies()
