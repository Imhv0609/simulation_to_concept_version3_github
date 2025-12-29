# Recent Updates Report - Version 3 Teaching Agent
**Date:** December 27, 2025

---

## Overview

This report documents the recent fixes and improvements made to the adaptive physics tutor, focusing on two main issues:
1. **Wrong Answer Evaluation** - LLM was not correctly identifying factually wrong answers
2. **Wrong Answer Correction** - Teacher was praising wrong answers instead of correcting them
3. **Multiple Parameter Requests** - Student requests for multiple params weren't being extracted

---

## Issue 1: Wrong Answer Evaluation

### Problem
The evaluator was marking wrong answers as correct because it didn't have:
- The **physics rules** to determine correctness
- The **comparison context** (what value to compare against)

**Example:**
- Teacher asked: "Does it swing faster or slower compared to when length was 8?"
- Current length: 3
- Student answered: "slower"
- Evaluator said: "MOSTLY" (should be NONE - it's WRONG!)

### Root Cause
The evaluator prompt lacked:
1. Physics rules for simple pendulum
2. Context about what the student was comparing against
3. The `param_history` only tracked teacher-initiated changes, not student-requested changes

### Solution

**File:** `nodes/evaluator.py`

Added physics rules at the top of the evaluation prompt:
```python
═══════════════════════════════════════════════════════════════
PHYSICS RULES FOR SIMPLE PENDULUM (USE THESE TO JUDGE CORRECTNESS):
═══════════════════════════════════════════════════════════════
1. TIME PERIOD depends ONLY on LENGTH (not mass, not oscillation count)
2. LONGER length = LONGER time period = SLOWER swings
3. SHORTER length = SHORTER time period = FASTER swings
4. Formula: T = 2π√(L/g) - period increases with square root of length
5. Number of oscillations does NOT affect how fast each swing is

APPLYING THE RULES:
- If length INCREASED (e.g., 3→8): Correct answer is "slower" or "longer period"
- If length DECREASED (e.g., 8→3): Correct answer is "faster" or "shorter period"
```

Added comparison context using teacher's message:
```python
⚠️ CRITICAL - USE THE TEACHER'S QUESTION TO DETERMINE CORRECTNESS:
Look at the teacher's last message - it usually asks the student to compare 
the CURRENT state to a PREVIOUS state.

CURRENT PARAMETERS: length={current_params.get('length', '?')}

If teacher asked "faster or slower compared to when length was X?":
- Extract X from the teacher's message
- Compare: current length vs X
- If current < X (shorter now): correct answer is "faster"
- If current > X (longer now): correct answer is "slower"
```

### Result
Evaluator now correctly identifies wrong answers:
```
📝 Reasoning: The student answered 'slower'. The teacher asked for a comparison 
to a length of 8. The current length is 3. Since 3 < 8, the pendulum should be 
swinging faster. Saying 'slower' is factually incorrect.
❌ Factually Wrong: Student stated something incorrect
```

---

## Issue 2: Wrong Answer Correction (Teacher Response)

### Problem
Even when the evaluator correctly flagged `is_factually_wrong = True`, the teacher LLM was still saying things like:
- "Exactly right, friend!"
- "Great observation!"
- "You're on the right track!"

### Root Cause
The Gemma model was not prioritizing the correction instructions in the prompt. The instructions existed but were buried in the middle of the prompt.

### Solution

**File:** `nodes/teacher.py`

Added a **very prominent alert** at the VERY TOP of the user prompt:
```python
# Build the correction flag at the very top of prompt
wrong_answer_alert = ""
if is_factually_wrong and not student_asked_question and not student_requested_param:
    wrong_answer_alert = """
🚨🚨🚨 CRITICAL: STUDENT GAVE WRONG ANSWER - MUST CORRECT! 🚨🚨🚨
DO NOT PRAISE! DO NOT SAY "EXACTLY RIGHT" OR "GREAT OBSERVATION"!
The student's answer is FACTUALLY INCORRECT. You MUST start with:
"Not quite, friend..." or "Actually, that's not correct..."
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
"""

user_prompt = f"""{wrong_answer_alert}
CONCEPT BEING TAUGHT:
...
```

The existing correction instructions in the prompt were also kept:
```python
⚠️⚠️⚠️ STUDENT GAVE A FACTUALLY WRONG ANSWER - MUST CORRECT ⚠️⚠️⚠️
The student stated something that is INCORRECT. You MUST:
1. POLITELY but CLEARLY tell them they are wrong
2. STATE the correct fact
3. OFFER to demonstrate with simulation

DO NOT:
❌ Say "Good thinking!" or "You're on the right track!"
❌ Say "Almost!" or "Close!"
❌ Validate their incorrect answer in ANY way
```

### Model Compatibility Note
- **Gemini Flash 2.5:** Works correctly - respects correction instructions
- **Gemma 3 27B:** Sometimes ignores correction instructions despite prominent warnings

---

## Issue 3: Multiple Parameter Requests

### Problem
When student said "change length to 3 and oscillations to 7", the system showed:
```
🎛️ Parameter Request: both = None
```
The values (3 and 7) were not being extracted.

### Root Cause
The param_request handler only extracted `param_value` for single-param requests. For `both`, it needed to extract `length_value` and `oscillations_value` separately.

### Solution

**File:** `nodes/evaluator.py`

Updated the param_request handling section:
```python
elif response_type == "param_request":
    param = result.get("param_requested")
    value = result.get("param_value")
    is_valid = result.get("param_valid", False)
    
    # Handle "both" - multiple params requested
    length_val = result.get("length_value")
    osc_val = result.get("oscillations_value")
    
    if param == "both":
        print(f"   🎛️ Multiple Parameters Requested:")
        print(f"      - length = {length_val}")
        print(f"      - oscillations = {osc_val}")
    else:
        print(f"   🎛️ Parameter Request: {param} = {value}")
    
    # If valid, update the params
    new_params = current_params.copy()
    if param == "both":
        if length_val is not None:
            new_params["length"] = length_val
        if osc_val is not None:
            new_params["number_of_oscillations"] = osc_val
        if length_val is not None or osc_val is not None:
            output["current_params"] = new_params
    elif is_valid and param and value is not None:
        new_params[param] = value
        output["current_params"] = new_params
```

### Result
Multiple params now correctly extracted and applied:
```
>>> change the length to 3 units and oscillations to 7 units
🎛️ Multiple Parameters Requested:
   - length = 3
   - oscillations = 7
✅ Updating length → 3
✅ Updating oscillations → 7
```

---

## Files Modified

| File | Changes |
|------|---------|
| `nodes/evaluator.py` | Added physics rules, teacher message context, multiple param extraction |
| `nodes/teacher.py` | Added prominent wrong answer alert at top of prompt |

---

## Testing Summary

| Test Case | Before | After |
|-----------|--------|-------|
| Wrong answer "slower" (length 8→3) | MOSTLY ✗ | NONE ✓ |
| Factually wrong flag | Not set | Set correctly ✓ |
| Multi-param "length 3, osc 7" | both = None ✗ | length=3, osc=7 ✓ |
| Teacher correction (Gemini Flash) | Praised wrong | Corrects properly ✓ |
| Teacher correction (Gemma 3 27B) | Praised wrong | Still sometimes praises ⚠️ |

---

## Recommendations

1. **Use Gemini Flash 2.5** for production - it respects instructions better than Gemma models
2. **Consider adding example corrections** to the prompt for Gemma models
3. **Future enhancement:** Could add a post-processing check that rejects responses starting with praise words when `is_factually_wrong=True`

---

## Debug Features Added

Added debug prints in evaluator (can be removed later):
```python
print(f"   🔎 DEBUG - param_history length: {len(param_history)}")
if last_param_change:
    print(f"   🔎 DEBUG - Last change: ...")
```

---

*End of Report*
