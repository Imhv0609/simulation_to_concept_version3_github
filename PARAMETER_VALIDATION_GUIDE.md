# Parameter Validation System

## Overview

The parameter validation system automatically verifies that parameter changes in the teaching agent are accurate and correct. This ensures that when the teacher claims to change a simulation parameter, the change actually happens correctly in the system.

## What Gets Validated

### ✅ Teacher Claims Match State
- Extracts parameter change claims from teacher messages using pattern matching
- Verifies claimed values match actual values in the agent state
- Example: If teacher says "I'll set the car speed to 80", checks that `current_params.speedCar == 80`

### ✅ State Matches URL
- Verifies simulation URLs contain correct parameter values
- Checks that URL query parameters match the state's current_params
- Example: If `current_params.speedCar = 80`, URL must have `?speedCar=80`

### ✅ Parameters in Valid Ranges
- Checks all parameters are within their configured min/max ranges
- Prevents impossible or unrealistic values
- Example: speedWalker must be between 1-10 km/h, not 50 km/h

### ✅ Parameter Changes Detected
- Tracks actual parameter changes between turns
- Records additions to parameter_history
- Warns if teacher mentions a change but no change was recorded

## Files Added/Modified

### New Files

1. **`tester_agent/parameter_validator.py`** - Core validation logic
   - `ParameterValidator` class - Main validator
   - `ParameterValidation` class - Results for each turn
   - Validation methods for claims, URLs, ranges

2. **`test_parameter_validator.py`** - Unit tests
   - Tests all validation scenarios
   - Verifies error detection works correctly

### Modified Files

1. **`run_test.py`** - Direct mode test runner
   - Imports ParameterValidator
   - Initializes validator at start
   - Validates each turn after teacher response
   - Includes validation results in reports

2. **`run_test_api.py`** - API mode test runner
   - Same validation integration as run_test.py
   - Extracts state from API responses

3. **`simulations_config.py`** - Added min/max values
   - Added explicit `min` and `max` fields to parameter_info
   - Enables range validation for all simulations

## How to Use

### Running Tests with Validation

```bash
# Direct mode (no API needed)
python run_test.py

# API mode (API server must be running)
python run_test_api.py
```

Validation runs automatically during testing and shows:
- ✅ Validation passed - All checks successful
- ❌ Validation failed - Issues detected with details
- ⚠️ Warnings - Non-critical issues

### Reading Validation Reports

Test reports now include a `parameter_validation` section:

```json
{
  "parameter_validation": {
    "simulation_id": "speed_race",
    "total_turns_validated": 5,
    "turns_passed": 4,
    "turns_failed": 1,
    "pass_rate": 0.8,
    "total_issues": 1,
    "total_warnings": 2,
    "total_parameter_claims": 5,
    "total_actual_changes": 5,
    "validation_history": [
      {
        "turn": 1,
        "passed": true,
        "issues": [],
        "warnings": [],
        "claimed_changes": [{"parameter": "speedCar", "value": 80}],
        "actual_changes": [{"parameter": "speedCar", "old_value": 60, "new_value": 80}],
        "url_params": {"speedCar": "80", "speedWalker": "5", ...}
      }
    ]
  }
}
```

### Validation Output During Tests

```
--- Turn 3 ---
👤 Student: Can you make the car faster?
   ⏳ Waiting 15s for rate limits...
🤖 Teacher: Let me increase the car speed to 100 km/h...
   🔍 Validating parameters...
   ✅ Validation passed
   📊 Concept: 2/4 | Understanding: moderate | Quiz Mode: ❌
```

Or when issues are detected:

```
--- Turn 4 ---
👤 Student: What about the cyclist?
🤖 Teacher: I'll set the cyclist speed to 30 km/h...
   🔍 Validating parameters...
   ❌ Validation failed: 1 issues
      • Parameter mismatch: Teacher claimed 'speedCyclist' = 30, but state shows 25
   ⚠️  1 warnings
      • URL parameter 'speedCar' in state but not in URL
```

### Final Summary

```
======================================================================
🔍 PARAMETER VALIDATION SUMMARY
======================================================================
  Simulation:          speed_race
  Turns Validated:     5
  Passed:              4 ✅
  Failed:              1 ❌
  Pass Rate:           80.0%
  Critical Issues:     1
  Warnings:            2
  Parameter Claims:    5
  Actual Changes:      5

❌ Issues Found:

  Turn 4:
    • Parameter mismatch: Teacher claimed 'speedCyclist' = 30, but state shows 25
======================================================================
```

## Validation Logic Details

### Pattern Matching for Teacher Claims

The validator uses regex patterns to extract parameter mentions from teacher messages:

- `"set X to Y"` → parameter X, value Y
- `"change X to Y"` → parameter X, value Y
- `"adjust X to Y"` → parameter X, value Y
- `"X is now Y"` → parameter X, value Y
- `"increase/decrease X to Y"` → parameter X, value Y
- `"make X Y"` → parameter X, value Y

Parameter names are fuzzy-matched against config:
- Removes spaces and underscores
- Checks labels too (e.g., "car speed" → "speedCar")
- Partial matching (e.g., "speed" matches "speedCar")

### URL Parameter Extraction

Parses simulation URLs to extract query parameters:
```python
# URL: https://example.com/race.html?speedCar=80&speedWalker=5
# Extracted: {"speedCar": "80", "speedWalker": "5"}
```

Matches URL parameter keys using `url_key` from config:
```python
parameter_info = {
    "speedCar": {
        "url_key": "speedCar",  # Used to find param in URL
        "min": 20,
        "max": 120
    }
}
```

### Range Validation

Checks against `min` and `max` in parameter_info:
```python
if param_value < min_val:
    issue: "Parameter below minimum"
    
if param_value > max_val:
    issue: "Parameter above maximum"
```

## Configuration Requirements

For validation to work, each parameter in `simulations_config.py` must have:

```python
"parameter_info": {
    "parameterName": {
        "label": "Display Name",       # Required - for matching claims
        "range": "1-10 units",          # Optional - for display
        "min": 1,                       # Required - for range validation
        "max": 10,                      # Required - for range validation
        "url_key": "parameterName",     # Required - for URL validation
        "effect": "What this does"      # Optional - for descriptions
    }
}
```

## Benefits

1. **Catches Implementation Bugs**
   - Teacher says "speed is 80" but code sets it to 60
   - URL construction errors
   - State update failures

2. **Verifies Conversation Accuracy**
   - Ensures teacher doesn't lie about parameter values
   - Maintains trust in the teaching agent

3. **Prevents Invalid States**
   - Catches out-of-range values
   - Prevents simulation errors from bad parameters

4. **Comprehensive Test Reports**
   - Clear pass/fail metrics
   - Detailed issue tracking
   - Easy debugging with full history

## Future Enhancements

Possible improvements:

1. **Visual Change Verification**
   - Use computer vision to verify simulation actually renders changes
   - Compare screenshots before/after parameter changes

2. **Response Time Validation**
   - Verify parameters update quickly enough
   - Detect lag or failure to update

3. **Semantic Understanding**
   - Use LLM to understand more complex parameter mentions
   - Handle indirect references ("make it faster" → speed parameter)

4. **Automated Repair**
   - Automatically fix detected issues
   - Suggest corrections to teacher prompts

## Testing the Validator

Run the unit tests:

```bash
python test_parameter_validator.py
```

Expected output:
- Turn 1: ✅ Pass (correct claim and state)
- Turn 2: ❌ Fail (teacher claimed 30, state shows 25)
- Turn 3: ❌ Fail (parameter out of valid range)
- Turn 4: ❌ Fail (URL doesn't match state)

All failures are intentional tests of error detection.
