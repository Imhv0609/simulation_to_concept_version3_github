# Simulation URL Integration - Implementation Summary

## Overview
Integrated hosted GitHub Pages simulation with the adaptive teaching agent so that the browser automatically opens the simulation with updated parameters whenever the teacher suggests a parameter change.

## Date
December 26, 2025

---

## Problems Identified

### 1. **Simulation Not Opening**
- Teacher mentioned parameter changes (e.g., "changing length from 5 to 8") but the simulation didn't open
- The `current_params` in state weren't being updated even though teacher mentioned the change

### 2. **JSON Parsing Failures**
- Teacher node was returning raw text instead of JSON
- Error message: `⚠️ JSON parse failed, using raw response`
- When JSON parsing failed, `suggests_param_change` defaulted to `False`, preventing parameter updates

### 3. **Root Cause**
- **Gemma models** (gemma-3-27b-it) don't follow JSON formatting instructions well
- The prompts asked for JSON at the end, but Gemma often adds explanatory text or responds naturally
- Without proper JSON parsing, the system couldn't detect when parameters should change

---

## Solutions Implemented

### Solution 1: Stricter JSON Format Instructions

**File Modified:** `nodes/teacher.py`

**Changes:**
1. Added emphatic JSON requirement at the start of system prompt:
```python
⚠️ CRITICAL: You MUST respond with ONLY a valid JSON object. No extra text before or after.
Your response must start with { and end with }.
```

2. Replaced all `Return JSON:` blocks with more explicit format:
```python
⚠️ RESPOND WITH ONLY THIS JSON FORMAT (no other text):
```json
{
    "teacher_message": "...",
    "suggests_param_change": true/false,
    "param_to_change": "length or number_of_oscillations or null",
    "new_value": "number or null",
    "change_reason": "...",
    "prediction_question": "..."
}
```

REMEMBER: Output ONLY the JSON object. Start your response with { and end with }.
```

3. Added JSON code fence (```json) to guide the model better

**Result:** JSON parsing now works consistently - no more parse failures

---

### Solution 2: Simulation URL Configuration

**File Modified:** `config.py`

**Changes Added:**
```python
# Simulation URL
SIMULATION_BASE_URL = "https://imhv0609.github.io/simulation_to_concept_github/SimulationsNCERT-main/simple_pendulum.html"

def build_simulation_url(params: dict, autostart: bool = True) -> str:
    """Build simulation URL with parameters."""
    url = f"{SIMULATION_BASE_URL}?length={params.get('length', 5)}&oscillations={params.get('number_of_oscillations', 10)}"
    if autostart:
        url += "&autoStart=true"
    return url
```

**What it does:**
- Stores the GitHub Pages hosted simulation URL
- Builds query string with current parameters
- Adds `autoStart=true` to automatically start the simulation

**Example URL generated:**
```
https://imhv0609.github.io/simulation_to_concept_github/SimulationsNCERT-main/simple_pendulum.html?length=2&oscillations=20&autoStart=true
```

---

### Solution 3: Browser Opening Logic

**File Modified:** `main.py`

**Changes Made:**

1. **Added import:**
```python
import webbrowser
```

2. **Updated config imports:**
```python
from config import (
    validate_config, 
    TOPIC_DESCRIPTION, 
    INITIAL_PARAMS,
    MAX_EXCHANGES,
    build_simulation_url  # NEW
)
```

3. **Added function to detect param changes and open browser:**
```python
def open_simulation_if_changed(current_params: Dict[str, Any], previous_params: Dict[str, Any]) -> bool:
    """Open simulation in browser if parameters have changed."""
    if current_params != previous_params:
        url = build_simulation_url(current_params)
        print(f"\n🔗 Opening simulation with new parameters...")
        webbrowser.open(url)
        return True
    return False
```

4. **Added tracking variable in main loop:**
```python
# Track previous params to detect changes
previous_params = INITIAL_PARAMS.copy()
```

5. **Added check after student response:**
```python
# Continue session with response
print("\n⏳ Processing your response...")
state = continue_session(response, thread_id)

# Check if params changed and open simulation
current_params = state.get("current_params", INITIAL_PARAMS)
if open_simulation_if_changed(current_params, previous_params):
    previous_params = current_params.copy()
```

**How it works:**
- Tracks `previous_params` throughout the session
- After each `continue_session()`, checks if `current_params` changed
- Opens browser ONLY when actual parameter change detected
- Updates `previous_params` to track for next change

---

## Simulation URL Parameters

The hosted simulation at `simple_pendulum.html` accepts these URL parameters:

| Parameter | Accepted Names | Range | Description |
|-----------|---------------|-------|-------------|
| Length | `length` or `lengthSlider` | 1-10 | Pendulum length in units |
| Oscillations | `oscillations`, `oscCount`, or `oscCountSlider` | 5-50 | Number of oscillations to observe |
| Auto Start | `autoStart` | `true` or `1` | Automatically start simulation |

**Example URLs:**
```
# Length 5, Oscillations 10, auto-start
https://imhv0609.github.io/.../simple_pendulum.html?length=5&oscillations=10&autoStart=true

# Length 2, Oscillations 20, auto-start
https://imhv0609.github.io/.../simple_pendulum.html?length=2&oscillations=20&autoStart=true
```

---

## Testing Results

### Test Session Output:
```
📊 Parameter Change: length = 8 → 5
🔗 Opening simulation with new parameters...
┌──────────────────────────────────────────────────┐
│ 🧪 SIMULATION STATE                               │
├──────────────────────────────────────────────────┤
│  Length:       5 units                           │
│  Oscillations: 10 count                          │
└──────────────────────────────────────────────────┘

📊 Parameter Change: length = 5 → 2
🔗 Opening simulation with new parameters...
┌──────────────────────────────────────────────────┐
│ 🧪 SIMULATION STATE                               │
├──────────────────────────────────────────────────┤
│  Length:       2 units                           │
│  Oscillations: 10 count                          │
└──────────────────────────────────────────────────┘

📊 Parameter Change: number_of_oscillations = 10 → 20
🔗 Opening simulation with new parameters...
┌──────────────────────────────────────────────────┐
│ 🧪 SIMULATION STATE                               │
├──────────────────────────────────────────────────┤
│  Length:       2 units                           │
│  Oscillations: 20 count                          │
└──────────────────────────────────────────────────┘
```

### ✅ Verified Working:
1. **JSON parsing** - No more "JSON parse failed" errors
2. **Parameter updates** - State correctly updates with new values
3. **Display updates** - SIMULATION STATE box shows current params
4. **Browser opens** - Simulation loads with correct parameters
5. **Auto-start** - Simulation begins automatically with new settings

---

## Files Modified Summary

| File | Lines Changed | Purpose |
|------|---------------|---------|
| `config.py` | +13 | Added SIMULATION_BASE_URL and build_simulation_url() |
| `nodes/teacher.py` | ~20 | Made JSON format instructions more explicit |
| `main.py` | +23 | Added browser opening logic with change detection |

**Total:** 3 files, ~56 lines changed/added

---

## User Experience Flow

1. **Student responds** to teacher's question
2. **Teacher decides** parameter change needed (via JSON response)
3. **State updates** with new parameter values
4. **Display shows** updated SIMULATION STATE
5. **Browser opens** automatically with simulation URL + parameters
6. **Simulation starts** automatically (`autoStart=true`)
7. **Student observes** the updated simulation

---

## Technical Details

### Why "Only on Actual Changes"?
- Teacher might **mention** parameters without changing them
- Teacher might repeat the same parameters for emphasis
- Opening browser on every response would be annoying
- **Solution:** Compare `current_params != previous_params` before opening

### Why Gemma Models Need Stricter Instructions?
- Gemma models are smaller, instruction-following models
- They don't handle JSON formatting as reliably as Gemini models
- Need very explicit, repeated instructions
- Code fences (```json) help guide the output format
- Multiple reminders throughout the prompt increase compliance

### Browser Opening Implementation
- Uses Python's built-in `webbrowser` module
- Opens in user's default browser
- Non-blocking (doesn't pause the agent)
- Works cross-platform (macOS, Windows, Linux)

---

## Future Enhancements (Not Implemented)

### Potential Improvements:
1. **Fallback param extraction** - Parse teacher's text to extract param changes when JSON fails
2. **Multi-simulation support** - Handle multiple different simulations
3. **Browser control** - Keep same tab instead of opening new ones
4. **Parameter validation** - Ensure values are within valid ranges
5. **URL preview** - Show the URL before opening

---

## Conclusion

The simulation URL integration is now **fully working**. When the teacher suggests a parameter change:
- JSON is parsed correctly ✅
- Parameters update in state ✅
- Browser opens with simulation ✅
- Student sees the updated physics simulation ✅

This creates a **seamless interactive learning experience** where the student can immediately observe the effects of parameter changes the teacher suggests.
