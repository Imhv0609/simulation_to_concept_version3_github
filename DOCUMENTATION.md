# Version 3 Teaching Agent - Comprehensive Documentation

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [State Structure](#state-structure)
4. [Node Details](#node-details)
   - [Content Loader](#1-content-loader-node)
   - [Teacher](#2-teacher-node)
   - [Understanding Evaluator](#3-understanding-evaluator-node)
   - [Trajectory Analyzer](#4-trajectory-analyzer-node)
   - [Strategy Selector](#5-strategy-selector-node)
5. [Graph Flow](#graph-flow)
6. [Configuration](#configuration)
7. [Running the Agent](#running-the-agent)
8. [Examples](#examples)

---

## Overview

Version 3 is an **adaptive teaching agent** that simulates a human-like physics tutor. Unlike previous versions that relied on rigid flows, this version:

- **Tracks learning trajectory** to adapt in real-time
- **Maintains rich parameter history** to learn from what worked/didn't
- **Uses natural conversation** with varied responses
- **Implements guardrails** to prevent infinite loops while staying adaptive

### Key Innovations

| Feature | Description |
|---------|-------------|
| **Understanding Levels** | Nuanced 4-level scale (none → partial → mostly → complete) |
| **Trajectory Analysis** | Detects improving/stagnating/regressing patterns |
| **Parameter History** | Tracks what changes helped learning |
| **Adaptive Strategy** | Dynamically selects teaching approach |
| **Teacher Modes** | Switches between encouraging/challenging/simplifying |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        VERSION 3 TEACHING AGENT                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐      ┌─────────────┐      ┌──────────────────┐           │
│   │   CONTENT   │ ──▶  │   TEACHER   │ ──▶  │  WAIT FOR INPUT  │           │
│   │   LOADER    │      │    NODE     │      │   (interrupt)    │           │
│   └─────────────┘      └─────────────┘      └────────┬─────────┘           │
│                                                      │                      │
│                                                      ▼                      │
│   ┌─────────────┐      ┌─────────────┐      ┌──────────────────┐           │
│   │  STRATEGY   │ ◀──  │ TRAJECTORY  │ ◀──  │   UNDERSTANDING  │           │
│   │  SELECTOR   │      │  ANALYZER   │      │    EVALUATOR     │           │
│   └──────┬──────┘      └─────────────┘      └──────────────────┘           │
│          │                                                                  │
│          ▼                                                                  │
│   ┌─────────────────────────────────────────────────────────┐              │
│   │                    ROUTING DECISION                      │              │
│   │  ┌──────────┬──────────┬──────────┬──────────┬────────┐ │              │
│   │  │ continue │ scaffold │ hint     │ summarize│ advance│ │              │
│   │  └──────────┴──────────┴──────────┴──────────┴────────┘ │              │
│   └─────────────────────────────────────────────────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## State Structure

The state is the central data structure that flows through all nodes. It's designed to be **rich and informative**.

### Core State Fields

```python
class TeachingState(TypedDict):
    # CONTENT
    topic_description: str              # Source material (pendulum description)
    concepts: List[Concept]             # Extracted teachable concepts
    current_concept_index: int          # Which concept we're teaching
    
    # CONVERSATION
    conversation_history: List[ConversationMessage]  # Full chat with metadata
    student_response: str               # Latest student input
    last_teacher_message: str           # Most recent teacher output
    
    # UNDERSTANDING TRACKING
    understanding_level: str            # "none" | "partial" | "mostly" | "complete"
    understanding_trajectory: List[str] # History: ["none", "partial", "partial", "mostly"]
    understanding_reasoning: str        # LLM's explanation
    
    # PARAMETER HISTORY
    parameter_history: List[ParameterChange]  # Rich change records
    current_params: Dict[str, float]    # Current simulation state
    
    # TEACHING CONTROL
    exchange_count: int                 # Back-and-forth count
    strategy: str                       # continue|try_different|scaffold|give_hint|summarize_advance
    teacher_mode: str                   # encouraging|challenging|simplifying
    trajectory_status: str              # improving|stagnating|regressing
    
    # FLAGS
    should_scaffold: bool
    concept_complete: bool
    session_complete: bool
    waiting_for_input: bool
```

### ConversationMessage Structure

Each message includes metadata for richer context:

```python
{
    "role": "teacher",                    # or "student"
    "content": "What do you think...",
    "timestamp": "2025-12-22T10:30:00",
    "understanding_level": "partial",     # Level at time of message
    "exchange_number": 2
}
```

### ParameterChange Structure

Tracks everything about a parameter change:

```python
{
    "parameter": "length",
    "old_value": 1.0,
    "new_value": 2.0,
    "reason": "To show how length affects period",
    "prediction_asked": "What do you think will happen to the swing time?",
    "student_reaction": "I think it will swing slower",
    "understanding_before": "partial",
    "understanding_after": "mostly",
    "was_effective": True
}
```

---

## Node Details

### 1. Content Loader Node

**File:** `nodes/content_loader.py`

**Purpose:** Parses the topic description and extracts teachable concepts using LLM.

**When it runs:** Once at session start.

**Input State:**
- `topic_description`: The source material

**Output State:**
- `concepts`: List of extracted concepts
- `current_concept_index`: Set to 0

#### How It Works

1. Takes the pendulum description
2. Sends it to LLM with extraction prompt
3. LLM identifies 2-4 key concepts
4. Each concept includes:
   - Title
   - Description
   - Key insight (the "aha" moment)
   - Related parameters

#### Example Output

```python
concepts = [
    {
        "id": 1,
        "title": "Length affects time period",
        "description": "Longer pendulums take more time to complete one swing.",
        "key_insight": "T = 2π√(L/g) - period increases with square root of length",
        "related_params": ["length"]
    },
    {
        "id": 2,
        "title": "Mass doesn't affect period",
        "description": "Surprisingly, changing the bob's mass doesn't change how fast it swings.",
        "key_insight": "Mass cancels out in the physics - only length and gravity matter",
        "related_params": ["mass"]
    },
    {
        "id": 3,
        "title": "Small angle approximation",
        "description": "For small angles, the period is nearly independent of starting angle.",
        "key_insight": "sin(θ) ≈ θ for small angles, making the motion simple harmonic",
        "related_params": ["angle"]
    }
]
```

#### Example Prompt to LLM

```
You are an expert physics teacher. Analyze this topic description and extract 
2-4 KEY CONCEPTS that should be taught to a student.

TOPIC DESCRIPTION:
A simple pendulum consists of a mass (called the bob) suspended...
[full description]

For each concept, provide:
1. A short title (5-7 words)
2. A clear description of what to teach
3. The key insight or "aha moment"
4. Which simulation parameters best illustrate this concept

Return ONLY valid JSON...
```

---

### 2. Teacher Node

**File:** `nodes/teacher.py`

**Purpose:** The heart of the agent - generates natural, adaptive responses like a real teacher.

**When it runs:** After content loading, and after each strategy selection.

**Input State:**
- `concepts`, `current_concept_index`
- `conversation_history`
- `understanding_level`
- `parameter_history`
- `current_params`
- `strategy`, `teacher_mode`
- `exchange_count`
- `student_response`

**Output State:**
- `last_teacher_message`: Generated response
- `conversation_history`: Updated
- `current_params`: Updated if param change
- `parameter_history`: Updated if param change
- `waiting_for_input`: True
- `exchange_count`: Incremented

#### How It Works

1. **Gathers context** from state
2. **Builds system prompt** with:
   - Teacher personality (warm, patient "Alex")
   - Current mode (encouraging/challenging/simplifying)
   - Current strategy
   - Simulation parameters
3. **Builds user prompt** based on:
   - First exchange? → Introduction prompt
   - Continuing? → Response prompt with history
4. **Generates response** that may include:
   - Explanation
   - Question
   - Prediction request
   - Parameter change suggestion
5. **Updates state** with message and any param changes

#### Teacher Personality

```
YOUR PERSONALITY:
- Warm, patient, and genuinely interested in helping students learn
- Uses analogies and real-world examples
- Celebrates small wins and acknowledges effort
- Never makes students feel bad for wrong answers
- Asks thought-provoking questions rather than just telling
```

#### Mode-Specific Behaviors

| Mode | Behavior |
|------|----------|
| **Encouraging** | Celebrate progress, build confidence, gentle guidance |
| **Challenging** | Push deeper thinking, ask "why", extend understanding |
| **Simplifying** | Break down concepts, use simpler language, more concrete examples |

#### Example: First Exchange Introduction

**State:**
- `exchange_count`: 0
- `strategy`: "continue"
- `teacher_mode`: "encouraging"
- Current concept: "Length affects time period"

**Generated Response:**
```
"Hey there, friend! 👋 Today we're going to explore something really cool about 
pendulums. Have you ever noticed how a grandfather clock's pendulum swings so 
steadily? What do you think determines how fast or slow it swings? Take a look 
at our simulation - the pendulum is currently 1 meter long. What do you think 
would happen if we made it longer?"
```

#### Example: Continuing with Parameter Change

**State:**
- `exchange_count`: 2
- `understanding_level`: "partial"
- `strategy`: "try_different"
- Student said: "I think heavier things fall faster"

**Generated Response:**
```
"That's a really common intuition! Many people think that way. But here's 
something fascinating to test - let's try an experiment. Currently our bob 
weighs 1 kg. What do you PREDICT will happen to the swing time if we double 
the mass to 2 kg? Take a guess before we try it!"
```

**Parameter Change Record Created:**
```python
{
    "parameter": "mass",
    "old_value": 1.0,
    "new_value": 2.0,
    "reason": "To demonstrate mass independence",
    "prediction_asked": "What will happen if we double the mass?",
    ...
}
```

---

### 3. Understanding Evaluator Node

**File:** `nodes/evaluator.py`

**Purpose:** Analyzes student responses to determine their understanding level.

**When it runs:** After receiving student input.

**Input State:**
- `student_response`
- `concepts`, `current_concept_index`
- `conversation_history`
- `last_teacher_message`
- `parameter_history`

**Output State:**
- `understanding_level`: none/partial/mostly/complete
- `understanding_reasoning`: Explanation
- `understanding_trajectory`: Updated history
- `conversation_history`: Updated with student message
- `parameter_history`: Updated with effectiveness

#### Understanding Levels Explained

| Level | Description | Example Response |
|-------|-------------|------------------|
| **none** | No understanding, off-topic, or "I don't know" | "I have no idea" |
| **partial** | Some grasp but gaps or misconceptions | "Longer pendulums are slower because they're heavier" |
| **mostly** | Good understanding, minor gaps | "Length affects the period - longer is slower" |
| **complete** | Clear, accurate understanding | "The period depends on length's square root, not mass" |

#### Evaluation Guidelines (from prompt)

```
IMPORTANT GUIDELINES:
1. Be generous but accurate - look for evidence of understanding
2. Consider if they're answering a prediction question
3. "I think X because Y" shows more understanding than just "X"
4. Look for conceptual understanding, not memorized formulas
5. If they show they're thinking through it, that's "partial" at minimum
```

#### Example Evaluation

**Context:**
- Concept: "Mass doesn't affect period"
- Teacher asked: "What do you predict will happen if we double the mass?"
- Student response: "I think it will swing at the same speed because the mass doesn't matter for pendulums"

**Evaluation Output:**
```python
{
    "level": "complete",
    "reasoning": "Student correctly identifies mass independence with clear reasoning",
    "what_they_got_right": "Understands mass doesn't affect period",
    "what_needs_work": "Could explain WHY mass cancels out",
    "detected_misconception": None
}
```

#### Parameter History Update

After evaluation, updates the last parameter change record:
```python
parameter_history[-1]["student_reaction"] = "I think it will swing the same..."
parameter_history[-1]["understanding_after"] = "complete"
parameter_history[-1]["was_effective"] = True  # Because understanding improved
```

---

### 4. Trajectory Analyzer Node

**File:** `nodes/trajectory.py`

**Purpose:** Detects learning patterns from understanding history.

**When it runs:** After evaluation.

**Input State:**
- `understanding_trajectory`
- `understanding_level`
- `exchange_count`

**Output State:**
- `trajectory_status`: improving/stagnating/regressing
- `concept_complete`: Boolean

#### Trajectory Detection Logic

```python
def calculate_trajectory_status(trajectory: List[str]) -> str:
    # Map levels to scores
    level_scores = {"none": 0, "partial": 1, "mostly": 2, "complete": 3}
    
    # Compare recent trend
    # If score increasing → "improving"
    # If score decreasing → "regressing"  
    # If score flat → "stagnating"
```

#### Examples

| Trajectory | Status | Interpretation |
|------------|--------|----------------|
| `["none", "partial", "mostly"]` | improving | Student is learning! |
| `["partial", "partial", "partial"]` | stagnating | Stuck, need new approach |
| `["mostly", "partial", "none"]` | regressing | Lost them, simplify! |
| `["partial", "none", "partial"]` | stagnating | Oscillating (uncertain) |

#### Special Detection: Oscillation

If trajectory shows back-and-forth pattern (up-down-up or down-up-down), it's treated as stagnation because the student seems uncertain.

---

### 5. Strategy Selector Node

**File:** `nodes/strategy.py`

**Purpose:** The "brain" that decides what to do next.

**When it runs:** After trajectory analysis.

**Input State:**
- `understanding_level`
- `trajectory_status`
- `exchange_count`
- `concept_complete`
- `parameter_history`
- `concepts`, `current_concept_index`

**Output State:**
- `strategy`: continue/try_different/scaffold/give_hint/summarize_advance
- `teacher_mode`: encouraging/challenging/simplifying
- `should_scaffold`: Boolean
- `current_concept_index`: Updated if advancing
- `session_complete`: True if all done

#### Strategy Decision Matrix

| Trajectory | Understanding | Exchange | → Strategy | → Mode |
|------------|---------------|----------|------------|--------|
| any | complete | any | summarize_advance | encouraging |
| improving | mostly | any | continue | challenging |
| improving | partial | < 3 | continue | encouraging |
| improving | partial | >= 3 | try_different | encouraging |
| stagnating | any | < 3 | try_different | encouraging |
| stagnating | any | 3-4 | scaffold | simplifying |
| stagnating | any | >= 5 | give_hint | simplifying |
| regressing | any | < 3 | scaffold | simplifying |
| regressing | any | >= 3 | give_hint | simplifying |
| any | any | >= MAX | summarize_advance | encouraging |

#### Strategy Definitions

| Strategy | What Teacher Does |
|----------|-------------------|
| **continue** | Keep same approach, it's working |
| **try_different** | Change explanation style, use new analogy |
| **scaffold** | Break concept into smaller sub-parts |
| **give_hint** | More direct guidance toward the answer |
| **summarize_advance** | Wrap up, give key takeaway, move to next concept |

#### Example Decision Flow

**State:**
- `understanding_level`: "partial"
- `trajectory_status`: "stagnating"
- `exchange_count`: 4
- All params tried, none effective

**Decision:**
```
Strategy: scaffold
Mode: simplifying
Reasoning: Student has been stuck for 4 exchanges with no improvement.
           Need to break this down into simpler parts.
```

---

## Graph Flow

### Visual Flow

```
START
  │
  ▼
┌─────────────────┐
│ content_loader  │ Extract concepts from description
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    teacher      │◄──────────────────────────────────┐
└────────┬────────┘                                   │
         │                                            │
         ▼                                            │
   [INTERRUPT]      Wait for student input            │
         │                                            │
         ▼                                            │
┌─────────────────┐                                   │
│   evaluator     │ Assess understanding              │
└────────┬────────┘                                   │
         │                                            │
         ▼                                            │
┌─────────────────┐                                   │
│   trajectory    │ Detect learning pattern           │
└────────┬────────┘                                   │
         │                                            │
         ▼                                            │
┌─────────────────┐                                   │
│    strategy     │───────────────────────────────────┘
└────────┬────────┘   (if not session_complete)
         │
         ▼ (if session_complete)
       [END]
```

### Checkpointing

The graph uses LangGraph's `MemorySaver` checkpointer with `interrupt_before=["evaluator"]`. This means:

1. Graph runs until reaching evaluator node
2. **Pauses** to wait for student input
3. When input received, resumes from evaluator
4. Continues through trajectory → strategy → back to teacher
5. Pauses again for next input

---

## Configuration

### Environment Variables (`.env`)

```bash
# LLM
GOOGLE_API_KEY="your-api-key"
GEMINI_MODEL=gemini-2.0-flash

# Teaching Guardrails
TEMPERATURE=0.7
MAX_EXCHANGES=6        # Maximum back-and-forth per concept
SCAFFOLD_TRIGGER=3     # When to start breaking down concepts
```

### Pendulum Content (`config.py`)

```python
PENDULUM_DESCRIPTION = """
A simple pendulum consists of a mass (called the bob) suspended...
[Full description with formulas and parameters]
"""

INITIAL_PARAMS = {
    "length": 1.0,      # meters
    "mass": 1.0,        # kg
    "angle": 15,        # degrees
    "gravity": 9.8      # m/s²
}
```

---

## Running the Agent

### Installation

```bash
cd simulation_to_concept_version3
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

### Sample Session

```
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║      🎓 ADAPTIVE PHYSICS TUTOR - Version 3                        ║
║      Interactive Teaching with Parameter History                   ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

📝 Session ID: session_abc12345

📖 Topic: Simple Pendulum
   We'll explore how pendulums work through interactive simulation!

⏳ Initializing teaching session...

┌──────────────────────────────────────────────────┐
│ 🧪 SIMULATION STATE                              │
├──────────────────────────────────────────────────┤
│  Length:  1.00 m                                 │
│  Mass:    1.00 kg                                │
│  Angle:   15.0°                                  │
│  Gravity: 9.8 m/s²                               │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ 📊 LEARNING PROGRESS                             │
├──────────────────────────────────────────────────┤
│  Concepts: [▒▒▒] 0/3                             │
│  Current:  Length affects time period            │
│  Understanding: ⬜⬜⬜⬜ (none)                    │
│  Trend: 📈 improving                             │
│  Exchange: 0/6                                   │
└──────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────
🎓 Teacher Alex:
────────────────────────────────────────────────────────────
  Hey there, friend! 👋 Today we're going to explore something 
  really fascinating about pendulums. Have you ever watched a 
  grandfather clock? What do you think determines how fast the 
  pendulum swings back and forth?
────────────────────────────────────────────────────────────

👩‍🎓 Your response (or 'quit' to exit):
>>> I think heavier pendulums swing slower

⏳ Processing your response...

[... evaluation, trajectory, strategy ...]

┌──────────────────────────────────────────────────┐
│ 📊 LEARNING PROGRESS                             │
├──────────────────────────────────────────────────┤
│  Understanding: 🟨⬜⬜⬜ (partial)                │
│  Trend: 📈 improving                             │
│  Exchange: 1/6                                   │
└──────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────
🎓 Teacher Alex:
────────────────────────────────────────────────────────────
  That's a really interesting thought! Many people have that 
  same intuition. Let's test it! Our pendulum bob currently 
  weighs 1 kg. What do you PREDICT will happen if we double 
  it to 2 kg - will it swing faster, slower, or the same?
────────────────────────────────────────────────────────────

👩‍🎓 Your response (or 'quit' to exit):
>>> I think it will swing slower since it's heavier

[... continues ...]
```

---

## Examples

### Example 1: Student Improving Steadily

**Trajectory:** `["none", "partial", "mostly", "complete"]`

**Strategy Decisions:**
1. Exchange 1: continue (encouraging) - student engaged
2. Exchange 2: continue (encouraging) - making progress
3. Exchange 3: continue (challenging) - almost there
4. Exchange 4: summarize_advance - got it!

### Example 2: Student Stuck (Stagnating)

**Trajectory:** `["partial", "partial", "partial"]`

**Strategy Decisions:**
1. Exchange 1: continue - normal start
2. Exchange 2: try_different - not improving, change approach
3. Exchange 3: scaffold (simplifying) - still stuck, break it down
4. Exchange 4: give_hint (simplifying) - more direct help

### Example 3: Student Regressing

**Trajectory:** `["partial", "none"]`

**Strategy Decisions:**
1. Exchange 1: continue - started okay
2. Exchange 2: scaffold (simplifying) - lost them, simplify immediately

### Example 4: Max Exchanges Reached

**Trajectory:** `["none", "partial", "partial", "partial", "partial", "partial"]`

**Strategy Decision at Exchange 6:**
- summarize_advance (encouraging)
- Teacher gives key takeaway and moves on
- Prevents infinite loop while being graceful

---

## Summary

Version 3 represents a significant advancement in adaptive teaching:

1. **Rich State Tracking** - Every aspect of learning is captured
2. **Intelligent Adaptation** - Strategy changes based on student needs
3. **Natural Conversation** - Teacher persona with varied responses
4. **Guardrails** - Prevents infinite loops while staying flexible
5. **Parameter History** - Learns from what teaching approaches worked

The agent behaves like a thoughtful human tutor who:
- Notices when students are struggling
- Tries different approaches
- Celebrates successes
- Knows when to simplify
- Knows when to move on
