"""
Simulations Configuration
=========================
Contains metadata, parameters, and concepts for all available simulations.
Allows the teaching agent to work with multiple simulations dynamically.
"""

# ═══════════════════════════════════════════════════════════════════════
# SIMULATION DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════

SIMULATIONS = {
    "simple_pendulum": {
        "title": "Time & Pendulums",
        "file": "simulations/simple_pendulum.html",
        "description": """
An interactive pendulum simulation where you can control pendulum length 
and number of oscillations to demonstrate how time period is measured 
and how it depends on length.

What can be demonstrated:
- Oscillatory motion (back and forth swinging)
- Measurement of time using oscillations
- Effect of pendulum length on time period
- Difference between total time and time period
- Stability of measurement using multiple oscillations
""",
        "cannot_demonstrate": [
            "Effect of mass on time period",
            "Effect of gravity on time period",
            "Damping or energy loss"
        ],
        "initial_params": {
            "length": 5,
            "number_of_oscillations": 10
        },
        "parameter_info": {
            "length": {
                "label": "Pendulum Length",
                "range": "1-10 units",
                "url_key": "length",
                "effect": "Longer = slower swings (longer period), Shorter = faster swings (shorter period)"
            },
            "number_of_oscillations": {
                "label": "Oscillations to Observe",
                "range": "5-50 count",
                "url_key": "oscillations",
                "effect": "More oscillations = more total time, but time period stays the same"
            }
        },
        "concepts": [
            {
                "id": 1,
                "title": "Time Period of a Pendulum",
                "description": "How the length of a pendulum affects how long it takes to complete one swing.",
                "key_insight": "Longer pendulum = longer time period (slower swings)",
                "related_params": ["length"]
            },
            {
                "id": 2,
                "title": "Measuring Time with Multiple Oscillations",
                "description": "Why observing multiple swings gives a more accurate measurement of the time period.",
                "key_insight": "Multiple oscillations reduce measurement error and show consistency",
                "related_params": ["number_of_oscillations"]
            }
        ]
    },
    
    "earth_rotation_revolution": {
        "title": "Earth's Rotation & Revolution",
        "file": "simulations/rotAndRev.html",
        "description": """
An interactive simulation demonstrating Earth's rotation (day/night cycle) 
and revolution around the Sun (seasons), including the effect of axial tilt.

What can be demonstrated:
- Day and night cycle from Earth's rotation
- Seasonal changes from Earth's revolution and axial tilt
- Effect of axial tilt on seasons
- Relationship between rotation speed and day length
- Relationship between revolution speed and year length
""",
        "cannot_demonstrate": [
            "Moon phases or lunar orbit",
            "Solar and lunar eclipses",
            "Tides"
        ],
        "initial_params": {
            "rotationSpeed": 50,
            "axialTilt": 23.5,
            "revolutionSpeed": 50
        },
        "parameter_info": {
            "rotationSpeed": {
                "label": "Rotation Speed",
                "range": "0-100%",
                "url_key": "rotationSpeed",
                "effect": "Controls how fast Earth spins (day/night cycle speed)"
            },
            "axialTilt": {
                "label": "Axial Tilt Angle",
                "range": "0-30 degrees",
                "url_key": "axialTilt",
                "effect": "Affects seasons - more tilt = more extreme seasons, no tilt = no seasons"
            },
            "revolutionSpeed": {
                "label": "Revolution Speed",
                "range": "0-100%",
                "url_key": "revolutionSpeed",
                "effect": "Controls how fast Earth orbits the Sun (year length)"
            }
        },
        "concepts": [
            {
                "id": 1,
                "title": "Earth's Rotation and Day/Night",
                "description": "How Earth's spinning on its axis creates the day and night cycle.",
                "key_insight": "Earth's rotation causes day and night - one complete rotation = one day",
                "related_params": ["rotationSpeed"]
            },
            {
                "id": 2,
                "title": "Axial Tilt and Seasons",
                "description": "How Earth's tilted axis causes different seasons throughout the year.",
                "key_insight": "Axial tilt causes seasons - more tilt = more extreme seasonal differences",
                "related_params": ["axialTilt", "revolutionSpeed"]
            },
            {
                "id": 3,
                "title": "Revolution Around the Sun",
                "description": "How Earth's orbit around the Sun, combined with axial tilt, creates yearly seasonal cycles.",
                "key_insight": "Revolution + axial tilt creates seasons - one complete orbit = one year",
                "related_params": ["revolutionSpeed", "axialTilt"]
            }
        ]
    },
    
    "light_shadows": {
        "title": "Light & Shadows",
        "file": "simulations/lightsShadows.html",
        "description": """
An interactive simulation exploring how light creates shadows and how 
shadow properties change based on light source distance, object properties, 
and object size.

What can be demonstrated:
- Shadow formation from light blocking
- Effect of light distance on shadow size
- Effect of object size on shadow size
- Different shadow properties (opaque, translucent, transparent)
- Relationship between light rays and shadow boundaries
""",
        "cannot_demonstrate": [
            "Color effects or refraction",
            "Multiple light sources",
            "Reflection from mirrors"
        ],
        "initial_params": {
            "lightDistance": 5,
            "objectType": "Opaque",
            "objectSize": 5
        },
        "parameter_info": {
            "lightDistance": {
                "label": "Light Distance",
                "range": "1-10 units",
                "url_key": "lightDistance",
                "effect": "Closer light = larger shadow, Further light = smaller shadow"
            },
            "objectType": {
                "label": "Object Type",
                "range": "Opaque, Translucent, Transparent",
                "url_key": "objectType",
                "effect": "Opaque = dark shadow, Translucent = lighter fuzzy shadow, Transparent = no shadow"
            },
            "objectSize": {
                "label": "Object Size",
                "range": "1-10 units",
                "url_key": "objectSize",
                "effect": "Larger object = larger shadow, Smaller object = smaller shadow"
            }
        },
        "concepts": [
            {
                "id": 1,
                "title": "Shadow Formation",
                "description": "How shadows are created when objects block light.",
                "key_insight": "Opaque objects block light completely, creating shadows",
                "related_params": ["objectType"]
            },
            {
                "id": 2,
                "title": "Light Distance and Shadow Size",
                "description": "How the distance of the light source affects the size of the shadow.",
                "key_insight": "Closer light source = larger shadow (light rays are more divergent)",
                "related_params": ["lightDistance"]
            },
            {
                "id": 3,
                "title": "Object Properties and Shadows",
                "description": "How different object types (opaque, translucent, transparent) create different shadow characteristics.",
                "key_insight": "Material transparency affects shadow darkness - opaque blocks most, transparent blocks none",
                "related_params": ["objectType", "objectSize"]
            }
        ]
    }
}

# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def get_simulation(simulation_id: str) -> dict:
    """Get a specific simulation configuration."""
    return SIMULATIONS.get(simulation_id, None)

def get_all_simulations() -> dict:
    """Get all available simulations."""
    return SIMULATIONS

def get_simulation_list() -> list:
    """Get list of available simulation IDs and titles."""
    return [
        {"id": sim_id, "title": config["title"]} 
        for sim_id, config in SIMULATIONS.items()
    ]

def get_parameter_info(simulation_id: str) -> dict:
    """Get parameter information for a specific simulation."""
    sim = get_simulation(simulation_id)
    return sim["parameter_info"] if sim else {}

def get_concepts(simulation_id: str) -> list:
    """Get concepts for a specific simulation."""
    sim = get_simulation(simulation_id)
    return sim["concepts"] if sim else []

def get_initial_params(simulation_id: str) -> dict:
    """Get initial parameters for a specific simulation."""
    sim = get_simulation(simulation_id)
    return sim["initial_params"] if sim else {}
