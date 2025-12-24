# Version 3 Teaching Agent - Fixes Report

## Overview

This document details all the fixes and improvements made to the Version 3 adaptive teaching agent to make the conversation more natural, less robotic, and properly track student understanding.

---

## Fix #1: Evaluator Too Strict (Stuck in "Partial")

### Problem
The evaluator was too strict - students giving correct directional answers like "time period is longer" were being marked as "partial" with invented misconceptions. This caused students to get stuck and never advance.

### Solution
Rewrote the evaluator prompt to be generous with correct answers while still maintaining quality:

**File:** `nodes/evaluator.py`

**Changes:**
- Correct direction = "complete" (e.g., "longer", "slower", "increases")
- Wrong direction = "partial" (they tried but need guidance)
- "okay" / "sure" = "partial" (not demonstrating anything)
- "I don't know" = "none" (needs teaching)

**Key Prompt Update:**
```
SCORING RULES:
1. CORRECT DIRECTION = COMPLETE: "longer", "slower", "increases" - if correct, give "complete"
2. WRONG DIRECTION = PARTIAL: If they predict wrong, that's "partial"
3. ACKNOWLEDGMENTS ARE PARTIAL: "okay", "sure" = "partial"
4. "I don't know" = NONE
```

---

## Fix #2: Teacher Asking Vague Questions

### Problem
The teacher was asking vague, unanswerable questions like:
- "What do you think?"
- "Interesting, isn't it?"
- "Let's think about this..."

Students didn't know what they were supposed to answer.

### Solution
Added explicit rules for asking specific, answerable questions with options.

**File:** `nodes/teacher.py`

**Changes:**
Added "CRITICAL RULES FOR ASKING QUESTIONS" section:
```
1. ALWAYS end with ONE specific, answerable question
2. Give options when asking for predictions: "Will it swing faster or slower?"
3. Be explicit about what you want
4. Avoid vague prompts like "what do you think?" without context

EXAMPLES OF GOOD SPECIFIC QUESTIONS:
- "If we make the pendulum longer, will it swing faster or slower?"
- "What do you think happens to the time period - does it increase or decrease?"

EXAMPLES OF BAD VAGUE QUESTIONS (AVOID):
- "What do you think about that?"
- "Interesting, isn't it?"
```

---

## Fix #3: Simplified Topic Description

### Problem
The original pendulum description was too technical and complex:
```
A simple pendulum consists of a mass (called the bob) suspended from a fixed point 
by a string or rod of length L. When displaced from its equilibrium position...
The relationship is given by T = 2π√(L/g).
```

### Solution
Simplified to be understandable by everyone:

**File:** `config.py`

**New Description:**
```
A pendulum is a weight hanging from a string that swings back and forth.
Think of a child on a swing or a grandfather clock.

What affects how fast it swings?
- The length of the string (longer = slower swings)
- Gravity (stronger gravity = faster swings)
- Surprisingly, the weight and starting angle don't change the speed much!

You can change: string length, weight, starting angle, and gravity.
```

---

## Fix #4: Parameters Not Being Used

### Problem
The teacher wasn't suggesting parameter changes to make the simulation interactive. The simulation was static.

### Solution
Added stronger encouragement for the teacher to use parameter changes.

**File:** `nodes/teacher.py`

**Changes:**
Added instruction in user prompt:
```
⚠️ IMPORTANT - USE THE SIMULATION:
You SHOULD suggest changing a parameter to help the student learn!
- If exchange >= 1, suggest a parameter change with suggests_param_change=true
- Ask "What do you think will happen if we change X to Y?" with options
- Use parameter changes to make learning interactive and visual
```

**Result:** Teacher now actively changes parameters (length, mass, angle, gravity) and asks for predictions.

---

## Fix #5: Concept Numbering Mismatch

### Problem
Display showed "Concepts: 1/4" but logs said "advancing to concept 2". This was confusing.

### Solution
Clarified the counting logic in the progress display.

**File:** `main.py`

**Change:**
```python
# Progress bar - current_idx IS the number of completed concepts
# (we're working on concept at index current_idx, so current_idx concepts are done)
total = len(concepts)
completed = current_idx  # Index 0 = working on 1st, 0 done. Index 1 = working on 2nd, 1 done.
```

---

## Fix #6: Observation vs Understanding

### Problem
When a student said "it took longer" (correct observation from simulation), it was marked as "complete" and the agent moved to the next concept. But this is just an OBSERVATION - the student didn't explain WHY.

### Solution
Introduced distinction between observation and understanding:

**File:** `nodes/evaluator.py`

**New Levels:**
- **"complete"**: Student explains WHAT happens AND gives a reason WHY
- **"mostly"**: Correct observation/prediction but NO reasoning (good start, needs follow-up!)
- **"partial"**: Wrong direction, vague, or just acknowledgment
- **"none"**: "I don't know", off-topic

**Examples:**
```
- "it takes longer" → MOSTLY (observation only, no because/why)
- "longer because more distance" → COMPLETE ✓
- "because it's longer" → COMPLETE ✓ (simple but counts!)
- "I think because gravity" → COMPLETE ✓ (any reasoning attempt)
```

---

## Fix #7: Teacher Not Summarizing Completed Concepts

### Problem
When moving to a new concept, the teacher just introduced the new one without summarizing what the student had just learned. This felt abrupt.

### Solution
Teacher now summarizes the completed concept before introducing the new one.

**File:** `nodes/teacher.py`

**Changes:**
When `exchange_count == 0` and `current_idx > 0`:
```python
# We just completed a concept - summarize it and introduce the new one
user_prompt = f"""
PREVIOUS CONCEPT (just completed):
Title: {previous_concept['title']}
Key Insight: {previous_concept['key_insight']}

NEW CONCEPT TO INTRODUCE:
Title: {current_concept['title']}
...

Your job is to:
1. FIRST: Celebrate and SUMMARIZE what they just learned
2. THEN: Smoothly transition to the new concept
3. End with a question about the new concept
```

**Result:** Teacher says things like "Fantastic work! You've discovered that longer pendulums take more time. Now let's explore..."

---

## Fix #8: Needs Deeper Flag for Observations

### Problem
When student gives correct observation without reasoning, the teacher should ask WHY, not just move on.

### Solution
Added `needs_deeper` flag to state and evaluator.

**Files:** `state.py`, `nodes/evaluator.py`, `nodes/teacher.py`

**Flow:**
1. Evaluator sets `needs_deeper: true` when level is "mostly"
2. Teacher sees this flag and asks "Can you think of WHY that happens?"
3. Teacher resets flag after handling

**Teacher Instruction:**
```
⚠️ STUDENT GAVE CORRECT OBSERVATION BUT NO REASONING:
They said WHAT happens correctly, but didn't explain WHY. Your job is to:
1. CELEBRATE their correct observation ("Exactly right!")
2. ASK them WHY they think that happens
3. Give a hint if helpful
This is NOT a correction - they're on the right track!
```

---

## Fix #9: "Mostly" Shouldn't Auto-Advance (with Safety Valve)

### Problem
Even after Fix #6, "mostly" was still advancing to the next concept because the trajectory analyzer treated it as "complete enough".

### Solution
Only "complete" advances, BUT added a safety valve to prevent getting stuck.

**File:** `nodes/trajectory.py`

**Changes:**
```python
# Check for concept completion
# ONLY "complete" counts as understood
# BUT: Safety valve - if they got "mostly" twice, they understand (just not explaining)
concept_complete = False

if current_level == "complete":
    concept_complete = True
elif current_level == "mostly":
    # Safety valve: 2 "mostly" in a row = advance
    if len(trajectory) >= 2 and trajectory[-2] == "mostly":
        concept_complete = True
        print("   🔓 Safety valve: 2x 'mostly' - advancing")
```

**Why Safety Valve:**
- Prevents students from getting stuck if LLM is too strict about "reasoning"
- If student gives correct observation twice without reasoning, they clearly understand
- Balances quality (asking for WHY) with progress (not getting stuck)

---

## Fix #10: Generous Reasoning Detection

### Problem
Risk that LLM would be too strict about what counts as "reasoning" and students would get stuck.

### Solution
Made evaluator very generous about what counts as reasoning for "complete".

**File:** `nodes/evaluator.py`

**Examples that count as COMPLETE:**
```
- "because it's longer" = COMPLETE (simple but valid)
- "more distance" = COMPLETE
- "gravity pulls more" = COMPLETE (any physics reasoning)
- "because..." followed by anything = COMPLETE
- "slower, more to travel" = COMPLETE (implied reasoning)
```

---

## Fix #11: False Praise for "I Don't Know"

### Problem
When student said "I don't know" or "I can't answer", the teacher responded with false praise like:
- "Great observation, friend! You correctly noticed that..."
- "Fantastic! You correctly observed..."

This gave false intuition and was confusing.

### Solution
Added explicit rule to prevent false praise when understanding is "none".

**File:** `nodes/teacher.py`

**Changes:**
```
RULE 1 - HONEST FEEDBACK (NO FALSE PRAISE):
- If understanding is "none" or student said "I don't know": Do NOT say "Great observation!" or "You correctly noticed..."
- Instead say: "That's okay! Let me help you..." or "No problem, let's figure this out together..."
- ONLY praise when they actually gave a correct answer
```

**Before (wrong):**
```
Student: "I don't know"
Teacher: "Great observation, friend! You correctly noticed..."
```

**After (correct):**
```
Student: "I don't know"
Teacher: "That's okay! Let's figure this out together..."
```

---

## Fix #12: Teacher Not Specific About Expected Action

### Problem
Teacher wasn't clear about what action the student should take:
- Should they OBSERVE the simulation?
- Should they PREDICT what will happen?
- Should they EXPLAIN why something happens?

Students didn't know what was expected of them.

### Solution
Added explicit action labels: PREDICT, OBSERVE, EXPLAIN.

**File:** `nodes/teacher.py`

**Changes:**
```
RULE 2 - ALWAYS BE SPECIFIC ABOUT WHAT YOU WANT:
Every response MUST end with a CLEAR ACTION for the student. Use these formats:

For PREDICTIONS (before changing parameter):
"I'm going to change the length to 2m. PREDICT: Will the pendulum swing faster or slower?"

For OBSERVATIONS (after changing parameter):
"Watch the simulation now. OBSERVE: What do you notice about the swing speed?"

For EXPLANATIONS:
"EXPLAIN: Why do you think a longer pendulum takes more time?"

RULE 3 - ONE CLEAR QUESTION:
- End with exactly ONE question
- Make it specific with options when possible
- Label it clearly: PREDICT/OBSERVE/EXPLAIN
```

**Examples from testing:**
```
"EXPLAIN: Why do you think a longer pendulum takes more time to complete one swing?"
"OBSERVE: What do you notice about how quickly the pendulum swings now compared to before?"
"OBSERVE: What do you notice about the TIME it takes to complete one full swing compared to when the mass was 1.0kg?"
```

---

## Summary of All Files Modified

| File | Changes |
|------|---------|
| `config.py` | Simplified pendulum description |
| `state.py` | Added `needs_deeper` flag |
| `main.py` | Fixed concept progress display |
| `nodes/evaluator.py` | Rewrote prompt for generous but quality evaluation; added `needs_deeper` output |
| `nodes/teacher.py` | Added specific question rules; summary before new concept; handling `needs_deeper`; encourage parameter use; NO false praise; PREDICT/OBSERVE/EXPLAIN labels |
| `nodes/trajectory.py` | Only "complete" advances; safety valve for 2x "mostly" |
| `nodes/strategy.py` | No changes needed |

---

## Testing Results

After all fixes, the agent now:

✅ Asks specific questions with options ("faster or slower?")
✅ Marks correct observations as "mostly" and asks for WHY
✅ Marks any reasoning attempt as "complete"
✅ Uses parameters actively (length, mass, angle, gravity)
✅ Summarizes concepts before moving to next
✅ Shows correct concept count (1/4 when working on concept 2)
✅ Has safety valve to prevent getting stuck (2x "mostly" = advance)
✅ Handles "I don't know" properly (marks as "none", provides teaching)
✅ **NO false praise** - says "That's okay!" instead of "Great observation!" when student doesn't know
✅ **Clear action labels** - PREDICT, OBSERVE, EXPLAIN tell student exactly what to do

---

## Version

- **Date:** December 23, 2025
- **Agent Version:** 3.0 with all 12 fixes
- **Model:** gemma-3-27b-it (configurable)
