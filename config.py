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

# ═══════════════════════════════════════════════════════════════════════════
# LLM CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemma-3-27b-it")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# ═══════════════════════════════════════════════════════════════════════════
# TEACHING AGENT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

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

# ═══════════════════════════════════════════════════════════════════════════
# TOPIC CONTENT (Simple Pendulum)
# ═══════════════════════════════════════════════════════════════════════════

PENDULUM_DESCRIPTION = """
A pendulum is a weight hanging from a string that swings back and forth.
Think of a child on a swing or a grandfather clock.

What affects how fast it swings?
- The length of the string (longer = slower swings)
- Gravity (stronger gravity = faster swings)
- Surprisingly, the weight and starting angle don't change the speed much!

You can change: string length, weight, starting angle, and gravity.
"""

# Initial simulation parameters
INITIAL_PARAMS = {
    "length": 1.0,      # meters
    "mass": 1.0,        # kg
    "angle": 15,        # degrees
    "gravity": 9.8      # m/s²
}

# ═══════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════

def validate_config():
    """Validate that required configuration is present."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set in .env file")
    print(f"✅ Config loaded: Model={GEMINI_MODEL}, MaxExchanges={MAX_EXCHANGES}")
    return True
