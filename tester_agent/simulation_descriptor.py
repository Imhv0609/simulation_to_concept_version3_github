"""
Generic Simulation Descriptor for Tester Agent
================================================
Provides textual descriptions of what a student would observe in any simulation.

Unlike the reference implementation (which was pendulum-specific), this module
works with ALL simulations by dynamically reading from simulations_config.py.
It generates human-readable descriptions of parameter changes and visual
observations for any simulation type.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def describe_simulation_state(simulation_id: str, current_params: Dict[str, Any]) -> str:
    """
    Describe the current state of any simulation based on its parameters.
    
    Args:
        simulation_id: The simulation identifier (e.g., 'simple_pendulum', 'light_shadows').
        current_params: Current parameter values.
        
    Returns:
        Human-readable description of what the student would see.
    """
    from simulations_config import get_simulation
    
    sim_config = get_simulation(simulation_id)
    if not sim_config:
        return f"[Unknown simulation: {simulation_id}]"
    
    title = sim_config["title"]
    param_info = sim_config.get("parameter_info", {})
    
    # Build parameter description
    param_lines = []
    for param_name, param_value in current_params.items():
        info = param_info.get(param_name, {})
        label = info.get("label", param_name)
        effect = info.get("effect", "")
        param_lines.append(f"  - {label}: {param_value}")
        if effect:
            param_lines.append(f"    (Effect: {effect})")
    
    params_text = "\n".join(param_lines) if param_lines else "  - Default parameters"
    
    return f"""🔬 **SIMULATION: {title}**

**Current Parameters:**
{params_text}
"""


def describe_parameter_change(
    simulation_id: str,
    param_name: str,
    old_value: Any,
    new_value: Any
) -> str:
    """
    Describe what would visually change when a parameter is modified.
    
    Args:
        simulation_id: The simulation identifier.
        param_name: Which parameter changed.
        old_value: Previous value.
        new_value: New value.
        
    Returns:
        Human-readable description of the visual change.
    """
    from simulations_config import get_simulation
    
    sim_config = get_simulation(simulation_id)
    if not sim_config:
        return f"Parameter {param_name} changed from {old_value} to {new_value}."
    
    param_info = sim_config.get("parameter_info", {})
    info = param_info.get(param_name, {})
    label = info.get("label", param_name)
    effect = info.get("effect", "")
    
    description = f"The {label} changed from {old_value} to {new_value}."
    if effect:
        description += f"\nExpected observation: {effect}"
    
    return description


def format_simulation_context_for_tester(agent_state: Dict[str, Any]) -> str:
    """
    Build a comprehensive simulation description for the tester agent,
    based on the current agent state.
    
    This is the main function called by run_test.py/run_test_api.py to give
    the tester agent context about what's happening in the simulation.
    
    Args:
        agent_state: The full teaching agent state dict.
        
    Returns:
        Formatted string describing the simulation for the tester to "observe".
    """
    simulation_id = agent_state.get("simulation_id", "simple_pendulum")
    current_params = agent_state.get("current_params", {})
    param_history = agent_state.get("parameter_history", [])
    last_teacher_message = agent_state.get("last_teacher_message", "")
    concepts = agent_state.get("concepts", [])
    current_concept_index = agent_state.get("current_concept_index", 0)
    
    from simulations_config import get_simulation
    sim_config = get_simulation(simulation_id)
    if not sim_config:
        return ""
    
    title = sim_config["title"]
    param_info = sim_config.get("parameter_info", {})
    
    # Current concept being taught
    current_concept_name = "Unknown"
    if current_concept_index < len(concepts):
        current_concept_name = concepts[current_concept_index].get("title", "Unknown")
    
    # Build current parameters description
    param_lines = []
    for param_name, param_value in current_params.items():
        info = param_info.get(param_name, {})
        label = info.get("label", param_name)
        param_lines.append(f"  - {label}: {param_value}")
    params_text = "\n".join(param_lines) if param_lines else "  - Default parameters"
    
    # Build parameter change description (if any recent changes)
    change_text = ""
    if param_history:
        last_change = param_history[-1]
        changed_param = last_change.get("parameter", "unknown")
        info = param_info.get(changed_param, {})
        label = info.get("label", changed_param)
        effect = info.get("effect", "")
        
        change_text = f"""
**Recent Change:**
  The teacher changed {label} from {last_change.get('old_value', '?')} to {last_change.get('new_value', '?')}.
  Reason: {last_change.get('reason', 'to demonstrate a concept')}
"""
        if effect:
            change_text += f"  What you would observe: {effect}\n"
    
    # Build the full context
    description = f"""
📺 **SIMULATION HAPPENING RIGHT NOW: {title}**

**What's being taught:** {current_concept_name}

**Current Simulation State:**
{params_text}
{change_text}
**The teacher said:** "{last_teacher_message[:300]}..."

**For your response:**
- Respond as if you're watching this simulation
- Comment on what you observe
- Ask questions if curious about what you see
- Stay in character while discussing what you observe
""".strip()
    
    return description


def format_simulation_from_api_metadata(metadata: Dict[str, Any]) -> Optional[str]:
    """
    Build simulation description from API response metadata.
    Used by run_test_api.py when interacting via the API.
    
    Args:
        metadata: The metadata dict from the API response (contains simulation info).
        
    Returns:
        Formatted simulation description string, or None if no simulation data.
    """
    simulation_data = metadata.get("simulation", {})
    if not simulation_data:
        return None
    
    sim_id = simulation_data.get("id", "unknown")
    sim_title = simulation_data.get("title", "Unknown Simulation")
    current_params = simulation_data.get("current_params", {})
    param_change = simulation_data.get("param_change")
    
    # Build parameter description
    param_lines = []
    for param_name, param_value in current_params.items():
        param_lines.append(f"  - {param_name}: {param_value}")
    params_text = "\n".join(param_lines) if param_lines else "  - Default parameters"
    
    # Build change description
    change_text = ""
    if param_change:
        change_text = f"""
**Recent Change:**
  {param_change.get('parameter', 'unknown')} changed from {param_change.get('before', '?')} to {param_change.get('after', '?')}.
  Reason: {param_change.get('reason', 'demonstration')}
"""
    
    # Get teacher message from metadata
    teacher_msg = metadata.get("teacher_message", {}).get("text", "")
    
    description = f"""
📺 **SIMULATION: {sim_title}** (ID: {sim_id})

**Current Parameters:**
{params_text}
{change_text}
**The teacher said:** "{teacher_msg[:300]}"

**For your response:**
- Respond as if you're watching this simulation
- Comment on what you observe
- Ask questions if curious about what you see
- Stay in character
""".strip()
    
    return description
