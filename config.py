"""
Configuration for Version 3 Teaching Agent
==========================================
Handles LLM setup, environment variables, and constants.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(ENV_PATH)

# ═══════════════════════════════════════════════════════════════════════
# LLM CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemma-3-27b-it")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# ═══════════════════════════════════════════════════════════════════════
# TEACHING AGENT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

# Guardrails
MAX_EXCHANGES = int(os.getenv("MAX_EXCHANGES", "6"))      # Absolute ceiling per concept
SCAFFOLD_TRIGGER = int(os.getenv("SCAFFOLD_TRIGGER", "3"))  # Break down after this many tries

# Understanding Levels
UNDERSTANDING_LEVELS = ["none", "partial", "mostly", "complete"]

# Teacher Modes
TEACHER_MODES = ["encouraging", "challenging", "simplifying"]

# Teaching Strategies
STRATEGIES = [
    "continue",         # Keep current approach
    "try_different",    # Change explanation style
    "scaffold",         # Break into sub-concepts
    "give_hint",        # More direct guidance
    "summarize_advance" # Wrap up and move on
]

# ═══════════════════════════════════════════════════════════════════════
# TOPIC CONTENT (Time & Pendulums - Intermediate Level)
# ═══════════════════════════════════════════════════════════════════════

TOPIC_TITLE = "Time & Pendulums"

TOPIC_DESCRIPTION = """
An interactive pendulum simulation where you can control pendulum length 
and number of oscillations to demonstrate how time period is measured 
and how it depends on length.

What can be demonstrated:
- Oscillatory motion (back and forth swinging)
- Measurement of time using oscillations
- Effect of pendulum length on time period
- Difference between total time and time period
- Stability of measurement using multiple oscillations
"""

# What this simulation CANNOT demonstrate (agent should NOT mention these)
CANNOT_DEMONSTRATE = [
    "Effect of mass on time period",
    "Effect of gravity on time period",
    "Damping or energy loss"
]

# Initial simulation parameters
INITIAL_PARAMS = {
    "length": 5,                    # 1-10 units
    "number_of_oscillations": 10    # 5-50 count
}

# Parameter details for teacher reference
PARAMETER_INFO = {
    "length": {
        "label": "Pendulum Length",
        "range": "1-10 units",
        "effect": "Longer = slower swings (longer period), Shorter = faster swings (shorter period)"
    },
    "number_of_oscillations": {
        "label": "Oscillations to Observe",
        "range": "5-50 count",
        "effect": "More oscillations = more total time, but time period stays the same"
    }
}

# Pre-defined concepts (Intermediate level from simulation design)
PRE_DEFINED_CONCEPTS = [
    {
        "id": 1,
        "title": "Time Period of a Pendulum",
        "description": "How the length of a pendulum affects how long it takes to complete one swing.",
        "key_insight": "Longer pendulum = longer time period (slower swings)",
        "related_params": ["length"]
    },
    {
        "id": 2,
        "title": "Time Period vs Number of Oscillations",
        "description": "Understanding that changing the number of oscillations changes total time but NOT the time period.",
        "key_insight": "More oscillations = more total time, but time period stays the same",
        "related_params": ["number_of_oscillations"]
    }
]

# ═══════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════

def validate_config():
    """Validate that required configuration is present."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set in .env file")
    print(f"✅ Config loaded: Model={GEMINI_MODEL}, MaxExchanges={MAX_EXCHANGES}")
    return True

# ═══════════════════════════════════════════════════════════════════════
# SIMULATION URL
# ═══════════════════════════════════════════════════════════════════════

SIMULATION_BASE_URL = "https://imhv0609.github.io/simulation_to_concept_github/SimulationsNCERT-main/simple_pendulum.html"

def build_simulation_url(params: dict, autostart: bool = True) -> str:
    """Build simulation URL with parameters."""
    url = f"{SIMULATION_BASE_URL}?length={params.get('length', 5)}&oscillations={params.get('number_of_oscillations', 10)}"
    if autostart:
        url += "&autoStart=true"
    return url
