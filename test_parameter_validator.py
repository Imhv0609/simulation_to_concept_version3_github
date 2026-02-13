"""
Quick Test for Parameter Validator
===================================
Tests the ParameterValidator class with sample data to verify it works correctly.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from tester_agent.parameter_validator import ParameterValidator


def test_basic_validation():
    """Test basic parameter validation with speed_race simulation."""
    
    print("\n" + "="*70)
    print("🧪 TEST: Parameter Validator - Speed Race Simulation")
    print("="*70)
    
    # Initialize validator for speed_race
    validator = ParameterValidator("speed_race")
    print("✅ Validator initialized for speed_race")
    
    # Turn 1: Teacher claims to set speedCar to 80
    print("\n--- Turn 1: Teacher sets speedCar to 80 ---")
    
    teacher_msg_1 = "Let me set the car speed to 80 km/h so you can see how fast it moves compared to others."
    
    state_1 = {
        "current_params": {
            "speedWalker": 5,
            "speedCyclist": 20,
            "speedCar": 80,
            "speedTrain": 100
        },
        "parameter_history": [
            {
                "parameter": "speedCar",
                "old_value": 60,
                "new_value": 80,
                "reason": "demonstrate higher speed"
            }
        ],
        "simulation_url": "https://example.com/speed_race.html?speedWalker=5&speedCyclist=20&speedCar=80&speedTrain=100"
    }
    
    result_1 = validator.validate_turn(
        turn_number=1,
        teacher_message=teacher_msg_1,
        state=state_1,
        previous_params={"speedWalker": 5, "speedCyclist": 20, "speedCar": 60, "speedTrain": 100}
    )
    
    print(f"  Passed: {result_1.passed}")
    print(f"  Issues: {len(result_1.issues)}")
    print(f"  Warnings: {len(result_1.warnings)}")
    print(f"  Claims detected: {len(result_1.claimed_changes)}")
    
    if result_1.claimed_changes:
        for claim in result_1.claimed_changes:
            print(f"    - Claimed: {claim['parameter']} = {claim['value']}")
    
    if result_1.issues:
        print("  ❌ Issues:")
        for issue in result_1.issues:
            print(f"    - {issue}")
    
    # Turn 2: Teacher claims wrong value (mismatch test)
    print("\n--- Turn 2: Teacher claims speedCyclist=30 but state shows 25 ---")
    
    teacher_msg_2 = "Now I'll increase the cyclist speed to 30 km/h."
    
    state_2 = {
        "current_params": {
            "speedWalker": 5,
            "speedCyclist": 25,  # Actual value is 25, not 30!
            "speedCar": 80,
            "speedTrain": 100
        },
        "parameter_history": [
            {
                "parameter": "speedCyclist",
                "old_value": 20,
                "new_value": 25,
                "reason": "demonstrate moderate speed increase"
            }
        ],
        "simulation_url": "https://example.com/speed_race.html?speedWalker=5&speedCyclist=25&speedCar=80&speedTrain=100"
    }
    
    result_2 = validator.validate_turn(
        turn_number=2,
        teacher_message=teacher_msg_2,
        state=state_2,
        previous_params=state_1["current_params"]
    )
    
    print(f"  Passed: {result_2.passed}")
    print(f"  Issues: {len(result_2.issues)}")
    
    if result_2.issues:
        print("  ❌ Issues (expected - this is a test of mismatch detection):")
        for issue in result_2.issues:
            print(f"    - {issue}")
    
    # Turn 3: Out of range test
    print("\n--- Turn 3: Teacher sets speedWalker to 50 (out of valid range) ---")
    
    teacher_msg_3 = "Let's make the walker speed 50 km/h."
    
    state_3 = {
        "current_params": {
            "speedWalker": 50,  # Out of range! Max is 10
            "speedCyclist": 25,
            "speedCar": 80,
            "speedTrain": 100
        },
        "parameter_history": [],
        "simulation_url": "https://example.com/speed_race.html?speedWalker=50&speedCyclist=25&speedCar=80&speedTrain=100"
    }
    
    result_3 = validator.validate_turn(
        turn_number=3,
        teacher_message=teacher_msg_3,
        state=state_3,
        previous_params=state_2["current_params"]
    )
    
    print(f"  Passed: {result_3.passed}")
    print(f"  Issues: {len(result_3.issues)}")
    
    if result_3.issues:
        print("  ❌ Issues (expected - parameter out of range):")
        for issue in result_3.issues:
            print(f"    - {issue}")
    
    # Turn 4: URL mismatch test
    print("\n--- Turn 4: State shows speedCar=100 but URL shows speedCar=80 ---")
    
    teacher_msg_4 = "The car is now at 100 km/h."
    
    state_4 = {
        "current_params": {
            "speedWalker": 5,
            "speedCyclist": 25,
            "speedCar": 100,  # State says 100
            "speedTrain": 100
        },
        "parameter_history": [],
        "simulation_url": "https://example.com/speed_race.html?speedWalker=5&speedCyclist=25&speedCar=80&speedTrain=100"  # URL says 80!
    }
    
    result_4 = validator.validate_turn(
        turn_number=4,
        teacher_message=teacher_msg_4,
        state=state_4,
        previous_params=state_3["current_params"]
    )
    
    print(f"  Passed: {result_4.passed}")
    print(f"  Issues: {len(result_4.issues)}")
    
    if result_4.issues:
        print("  ❌ Issues (expected - URL doesn't match state):")
        for issue in result_4.issues:
            print(f"    - {issue}")
    
    # Print overall summary
    print("\n" + "="*70)
    print("📊 VALIDATION SUMMARY")
    print("="*70)
    validator.print_summary()
    
    print("\n✅ Test completed!")
    print("   Turn 1 should pass (correct claim and state)")
    print("   Turn 2 should fail (teacher claimed 30, state shows 25)")
    print("   Turn 3 should fail (parameter out of valid range)")
    print("   Turn 4 should fail (URL doesn't match state)")


def test_simple_pendulum():
    """Test with simple_pendulum simulation."""
    
    print("\n" + "="*70)
    print("🧪 TEST: Parameter Validator - Simple Pendulum Simulation")
    print("="*70)
    
    validator = ParameterValidator("simple_pendulum")
    print("✅ Validator initialized for simple_pendulum")
    
    # Test turn with length change
    print("\n--- Turn 1: Teacher adjusts pendulum length ---")
    
    teacher_msg = "Let me adjust the pendulum length to 0.8 meters."
    
    state = {
        "current_params": {
            "length": 0.8,
            "amplitude": 30
        },
        "parameter_history": [
            {
                "parameter": "length",
                "old_value": 0.5,
                "new_value": 0.8,
                "reason": "demonstrate longer period"
            }
        ],
        "simulation_url": "https://example.com/pendulum.html?length=0.8&amplitude=30"
    }
    
    result = validator.validate_turn(
        turn_number=1,
        teacher_message=teacher_msg,
        state=state,
        previous_params={"length": 0.5, "amplitude": 30}
    )
    
    print(f"  Passed: {result.passed}")
    print(f"  Issues: {len(result.issues)}")
    print(f"  Warnings: {len(result.warnings)}")
    print(f"  Claims detected: {len(result.claimed_changes)}")
    
    if result.claimed_changes:
        for claim in result.claimed_changes:
            print(f"    - Claimed: {claim['parameter']} = {claim['value']}")
    
    validator.print_summary()
    print("\n✅ Simple pendulum test completed!")


if __name__ == "__main__":
    test_basic_validation()
    print("\n" + "="*70 + "\n")
    test_simple_pendulum()
