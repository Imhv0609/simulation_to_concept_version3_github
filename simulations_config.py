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

# =============================================================================
# PARALLEL LINES & TRANSVERSAL SIMULATION
# =============================================================================
SIMULATIONS["parallel_lines_angles"] = {
    "title": "Parallel Lines & Transversal",
    "file": "simulations/parallel-angles-interactive.html",
    "description": """
An interactive simulation where you explore angle relationships when a transversal 
line crosses two parallel lines. Drag the purple transversal to change its angle 
and observe how all 8 angles change together. Discover why corresponding angles are equal, 
alternate interior angles are equal, and co-interior angles sum to 180°.
    """.strip(),
    "concepts": [
        {
            "id": 1,
            "title": "Corresponding Angles",
            "key_insight": "When a transversal crosses parallel lines, angles in the same position at each intersection are always equal (∠1 = ∠5, ∠2 = ∠6, ∠3 = ∠7, ∠4 = ∠8)",
            "related_params": ["angle", "highlightPair"]
        },
        {
            "id": 2,
            "title": "Alternate Interior Angles",
            "key_insight": "Angles on opposite sides of the transversal, between the parallel lines, are always equal (∠3 = ∠5, ∠4 = ∠6)",
            "related_params": ["angle", "highlightPair"]
        },
        {
            "id": 3,
            "title": "Co-interior Angles (Consecutive Interior)",
            "key_insight": "Angles on the same side of the transversal, between parallel lines, always sum to 180° (∠3 + ∠6 = 180°, ∠4 + ∠5 = 180°)",
            "related_params": ["angle", "highlightPair"]
        },
        {
            "id": 4,
            "title": "Vertically Opposite Angles",
            "key_insight": "When two lines intersect, angles opposite each other are always equal (∠1 = ∠4, ∠2 = ∠3, ∠5 = ∠8, ∠6 = ∠7)",
            "related_params": ["angle"]
        }
    ],
    "cannot_demonstrate": [
        "Non-parallel lines",
        "More than two parallel lines",
        "Curved transversal",
        "Angles with non-Euclidean geometry",
        "Perpendicular relationships between the parallel lines"
    ],
    "initial_params": {
        "angle": 60,
        "phase": "explore",
        "highlightPair": None,
        "showRelationships": True,
        "lockAngle": False
    },
    "parameter_info": {
        "angle": {
            "label": "Transversal Angle",
            "range": "20-160 degrees",
            "url_key": "angle",
            "effect": "Changes the acute angle of the transversal line crossing the parallel lines"
        },
        "phase": {
            "label": "Phase",
            "range": "explore, quiz",
            "url_key": "phase",
            "effect": "Switches between exploration mode and built-in quiz mode"
        },
        "highlightPair": {
            "label": "Highlight Angle Pair",
            "range": "None, '1-5', '2-6', '3-7', '4-8', '3-5', '4-6', '3-6', '4-5'",
            "url_key": "highlightPair",
            "effect": "Highlights specific angle pair to focus student attention on relationships"
        },
        "showRelationships": {
            "label": "Show Relationships",
            "range": "true/false",
            "url_key": "showRelationships",
            "effect": "Shows or hides the relationship cards explaining angle types (corresponding, alternate, co-interior)"
        },
        "lockAngle": {
            "label": "Lock Angle",
            "range": "true/false",
            "url_key": "lockAngle",
            "effect": "Prevents student from dragging transversal - useful for demonstrations"
        }
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


# ═══════════════════════════════════════════════════════════════════════
# QUIZ QUESTIONS CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

QUIZ_QUESTIONS = {
    "simple_pendulum": [
        {
            "id": "pendulum_q1",
            "challenge": "Can you make the pendulum swing slower? Apply what you learned about how pendulum characteristics affect its motion.",
            "target_parameters": ["length"],
            "success_rule": {
                "conditions": [],  # No hard conditions, just optimize
                "optimization_target": {
                    "parameter": "length",
                    "objective": "maximize"  # Make it as long as possible for slowest swings
                },
                "tolerances": {
                    "perfect": 0.15,  # Within 15% of maximum
                    "partial": 0.35   # Within 35% of maximum
                },
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                }
            },
            "hints": {
                "attempt_1": "Think about what makes a pendulum swing slower. Which parameter affects the time period?",
                "attempt_2": "Remember from our lesson: longer pendulums take more time per swing. Try significantly increasing the length.",
                "attempt_3": "Make the pendulum much longer - try a high length value to achieve a slower swing."
            },
            "concept_reminder": "The time period of a pendulum depends on its length. A longer pendulum swings slower (longer time period), while a shorter pendulum swings faster (shorter time period)."
        },
        {
            "id": "pendulum_q2",
            "challenge": "Set the pendulum to complete exactly 5 oscillations. Can you make it swing as fast as possible while counting 5 swings?",
            "target_parameters": ["number_of_oscillations", "length"],
            "success_rule": {
                "conditions": [
                    {"parameter": "number_of_oscillations", "operator": "==", "value": 5}
                ],
                "optimization_target": {
                    "parameter": "length",
                    "objective": "minimize"  # Make it as short as possible for fastest swings
                },
                "tolerances": {
                    "perfect": 0.15,  # Within 15% of optimal (min value)
                    "partial": 0.35   # Within 35% of optimal
                },
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                }
            },
            "hints": {
                "attempt_1": "You need to set the number of oscillations to exactly 5, and make the pendulum swing quickly.",
                "attempt_2": "Remember: shorter pendulums swing faster! Try reducing the length significantly while keeping oscillations at 5.",
                "attempt_3": "Set oscillations to exactly 5 and make the length very short for the fastest swings."
            },
            "concept_reminder": "The number of oscillations determines how many swings we count, while length affects how fast each swing happens. Shorter pendulums complete multiple swings in less total time."
        }
    ],
    
    "earth_rotation_revolution": [
        {
            "id": "earth_q1",
            "challenge": "Can you make it nighttime for the observer on Earth? Adjust the rotation to show darkness.",
            "target_parameters": ["rotation_angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "rotation_angle", "operator": ">=", "value": 90},
                    {"parameter": "rotation_angle", "operator": "<=", "value": 270}
                ],
                "scoring": {
                    "perfect": 1.0,    # 90° <= rotation <= 270° (night side)
                    "partial": 0.6,    # close to night (60-90° or 270-300°)
                    "wrong": 0.3       # day side
                },
                "thresholds": {
                    "perfect": {"rotation_angle_min": 90, "rotation_angle_max": 270},
                    "partial": {"rotation_angle_min": 60, "rotation_angle_max": 300}
                }
            },
            "hints": {
                "attempt_1": "Think about when your side of Earth faces away from the Sun. What angle makes it night?",
                "attempt_2": "Earth's rotation causes day and night. Try rotating so the observer faces away from the Sun (between 90° and 270°).",
                "attempt_3": "Set rotation angle between 90° and 270° to place the observer on the night side."
            },
            "concept_reminder": "Earth's rotation on its axis causes day and night. When your location faces the Sun, it's day. When facing away from the Sun (opposite side), it's night."
        },
        {
            "id": "earth_q2",
            "challenge": "Position Earth in winter (for the Northern Hemisphere). Show Earth at the correct position in its orbit.",
            "target_parameters": ["revolution_angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "revolution_angle", "operator": ">=", "value": 250},
                    {"parameter": "revolution_angle", "operator": "<=", "value": 290}
                ],
                "scoring": {
                    "perfect": 1.0,    # ~270° (winter solstice)
                    "partial": 0.6,    # close to winter position
                    "wrong": 0.3       # wrong season
                },
                "thresholds": {
                    "perfect": {"revolution_angle_min": 250, "revolution_angle_max": 290},
                    "partial": {"revolution_angle_min": 230, "revolution_angle_max": 310}
                }
            },
            "hints": {
                "attempt_1": "In winter, the Northern Hemisphere tilts away from the Sun. Where should Earth be in its orbit?",
                "attempt_2": "Remember: Earth's tilt combined with its position in orbit creates seasons. Try around 270° for winter.",
                "attempt_3": "Set revolution angle between 250° and 290° to show Earth in winter position."
            },
            "concept_reminder": "Earth's revolution around the Sun, combined with its tilted axis, causes seasons. In winter, your hemisphere tilts away from the Sun, receiving less direct sunlight."
        }
    ],
    
    "light_shadows": [
        {
            "id": "light_q1",
            "challenge": "Create a partial shadow (penumbra). Adjust the light size to show both dark and lighter shadow regions.",
            "target_parameters": ["light_size"],
            "success_rule": {
                "conditions": [
                    {"parameter": "light_size", "operator": ">=", "value": 3}
                ],
                "scoring": {
                    "perfect": 1.0,    # light_size >= 3 (clear penumbra)
                    "partial": 0.6,    # light_size >= 2 (some penumbra)
                    "wrong": 0.3       # light_size < 2 (sharp shadow)
                },
                "thresholds": {
                    "perfect": {"light_size": 3},
                    "partial": {"light_size": 2}
                }
            },
            "hints": {
                "attempt_1": "A partial shadow forms when the light source is large. How big should the light be?",
                "attempt_2": "Larger light sources create softer shadows with partial shadow regions (penumbra). Try increasing light size.",
                "attempt_3": "Set light size to 3 or more to create a clear partial shadow (penumbra) around the dark shadow (umbra)."
            },
            "concept_reminder": "The size of the light source affects shadow sharpness. Large light sources create soft shadows with partial shadow regions (penumbra), while small light sources create sharp shadows."
        },
        {
            "id": "light_q2",
            "challenge": "Make the shadow as long as possible. Position the light to create the longest shadow.",
            "target_parameters": ["light_distance"],
            "success_rule": {
                "conditions": [
                    {"parameter": "light_distance", "operator": "<=", "value": 3}
                ],
                "scoring": {
                    "perfect": 1.0,    # light_distance <= 3 (very long shadow)
                    "partial": 0.6,    # light_distance <= 5 (longer shadow)
                    "wrong": 0.3       # light_distance > 5 (short shadow)
                },
                "thresholds": {
                    "perfect": {"light_distance": 3},
                    "partial": {"light_distance": 5}
                }
            },
            "hints": {
                "attempt_1": "Shadow length depends on how close or far the light is. What distance creates the longest shadow?",
                "attempt_2": "When light is closer to the object, shadows appear longer. Try moving the light closer.",
                "attempt_3": "Set light distance to 3 or less to create the longest possible shadow."
            },
            "concept_reminder": "Shadow length depends on the distance between the light source and the object. Closer light sources create longer shadows, while farther light sources create shorter shadows."
        }
    ],
    
    "angle_sum_property": [
        {
            "id": "angle_q1",
            "challenge": "Show the geometric proof! Enable the proof visualization to understand why triangle angles always sum to 180 degrees.",
            "target_parameters": ["show_proof_lines"],
            "success_rule": {
                "conditions": [
                    {"parameter": "show_proof_lines", "operator": "==", "value": True}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.0,
                    "wrong": 0.0
                },
                "thresholds": {
                    "perfect": {"show_proof_lines": True}
                }
            },
            "hints": {
                "attempt_1": "You need to enable the proof visualization. Look for the control to show the proof steps.",
                "attempt_2": "The proof uses a parallel line through the top vertex. Try turning on the proof display.",
                "attempt_3": "Set 'Show Proof Steps' to true to reveal the parallel line and alternate angles that prove the angle sum property."
            },
            "concept_reminder": "The parallel line proof shows that the three angles of a triangle can be rearranged at one vertex to form a straight line (180°), using the property of alternate interior angles formed by parallel lines."
        },
        {
            "id": "angle_q2",
            "challenge": "Verify the angle sum property yourself! Change the triangle shape and observe that the angle sum always remains 180 degrees, no matter what.",
            "target_parameters": ["vertexA_y", "vertexC_x"],
            "success_rule": {
                "conditions": [
                    {"parameter": "vertexA_y", "operator": "!=", "value": 150},
                    {"parameter": "vertexC_x", "operator": "!=", "value": 800}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                },
                "thresholds": {
                    "perfect": {"any_changed": True}
                }
            },
            "hints": {
                "attempt_1": "Try moving the triangle vertices to create a different shape. Does the angle sum still equal 180°?",
                "attempt_2": "Change the position of vertex A or vertex C to make a different triangle. The angle sum should remain constant.",
                "attempt_3": "Adjust any vertex position to verify that triangle angles always sum to 180° regardless of the shape."
            },
            "concept_reminder": "The angle sum property is universal for all triangles. No matter if it's equilateral, isosceles, scalene, acute, or obtuse - the interior angles always add up to exactly 180 degrees."
        }
    ],
    
    "parallel_lines_angles": [
        {
            "id": "parallel_q1",
            "challenge": "Set the transversal angle to 70° to demonstrate corresponding angles. Corresponding angles are equal when parallel lines are cut by a transversal.",
            "target_parameters": ["angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "angle", "operator": ">=", "value": 68},
                    {"parameter": "angle", "operator": "<=", "value": 72}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                },
                "thresholds": {
                    "perfect": {"angle": 70},
                    "partial": {"angle": 69}
                }
            },
            "hints": {
                "attempt_1": "∠1 is the acute angle formed at the top intersection. Drag the transversal to change the angle.",
                "attempt_2": "Watch the angle values update as you drag. You need to get close to 70°.",
                "attempt_3": "Adjust the transversal until the angle reads approximately 70°."
            },
            "concept_reminder": "Corresponding angles are in the same position at each intersection. When parallel lines are cut by a transversal, corresponding angles are always equal."
        },
        {
            "id": "parallel_q2",
            "challenge": "Set the angle to 60° to make the obtuse angle ∠3 equal to 120°. This demonstrates alternate interior angles.",
            "target_parameters": ["angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "angle", "operator": ">=", "value": 58},
                    {"parameter": "angle", "operator": "<=", "value": 62}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                },
                "thresholds": {
                    "perfect": {"angle": 60},
                    "partial": {"angle": 59}
                }
            },
            "hints": {
                "attempt_1": "∠3 is the obtuse angle at the top. If the acute angle is 60°, then ∠3 will be 120°.",
                "attempt_2": "The obtuse angle is always 180° minus the acute angle. Set the acute angle to 60°.",
                "attempt_3": "Adjust the transversal until the acute angle shows 60°, making the obtuse angle 120°."
            },
            "concept_reminder": "Alternate interior angles are on opposite sides of the transversal, between parallel lines, and are always equal."
        },
        {
            "id": "parallel_q3",
            "challenge": "Set the angle to 100° to demonstrate that co-interior angles sum to 180°. The obtuse angle ∠3 will be 80°, and ∠6 will be 100°.",
            "target_parameters": ["angle"],
            "success_rule": {
                "conditions": [
                    {"parameter": "angle", "operator": ">=", "value": 98},
                    {"parameter": "angle", "operator": "<=", "value": 102}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.3
                },
                "thresholds": {
                    "perfect": {"angle": 100},
                    "partial": {"angle": 99}
                }
            },
            "hints": {
                "attempt_1": "Co-interior angles are on the same side of the transversal, between the parallel lines.",
                "attempt_2": "If you set the acute angle to 100°, the obtuse angle will be 80°, and they sum to 180°.",
                "attempt_3": "Adjust to 100° and watch how ∠3 (80°) and ∠6 (100°) sum to 180°."
            },
            "concept_reminder": "Co-interior angles (also called consecutive interior angles) are on the same side of the transversal, between parallel lines, and always sum to 180°."
        },
        {
            "id": "parallel_q4",
            "challenge": "Use the highlight feature to show the corresponding angle pair ∠1 and ∠5. These angles are in the same relative position.",
            "target_parameters": ["highlightPair"],
            "success_rule": {
                "conditions": [
                    {"parameter": "highlightPair", "operator": "==", "value": "1-5"}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.0,
                    "wrong": 0.0
                },
                "thresholds": {
                    "perfect": {"highlightPair": "1-5"}
                }
            },
            "hints": {
                "attempt_1": "Corresponding angles are in the same position at each intersection.",
                "attempt_2": "∠1 is at the top right, ∠5 is at the bottom right - same position.",
                "attempt_3": "Set highlightPair to '1-5' to show these corresponding angles."
            },
            "concept_reminder": "Corresponding angles are in matching positions at each intersection where the transversal crosses the parallel lines."
        },
        {
            "id": "parallel_q5",
            "challenge": "Highlight the co-interior angle pair ∠4 and ∠5. These angles are on the same side of the transversal and sum to 180°.",
            "target_parameters": ["highlightPair"],
            "success_rule": {
                "conditions": [
                    {"parameter": "highlightPair", "operator": "in", "value": ["4-5", "3-6"]}
                ],
                "scoring": {
                    "perfect": 1.0,
                    "partial": 0.6,
                    "wrong": 0.0
                },
                "thresholds": {
                    "perfect": {"highlightPair": "4-5"},
                    "partial": {"highlightPair": "3-6"}
                }
            },
            "hints": {
                "attempt_1": "Co-interior angles are on the same side of the transversal, between the parallel lines.",
                "attempt_2": "∠4 and ∠5 are both on the right side - they're co-interior angles.",
                "attempt_3": "Set highlightPair to '4-5' or '3-6' to show co-interior angle pairs."
            },
            "concept_reminder": "Co-interior angles lie on the same side of the transversal, between the parallel lines, and their sum is always 180°."
        }
    ]
}
    
    # ═══════════════════════════════════════════════════════════════════════
    # ANGLE SUM PROPERTY SIMULATION (in SIMULATIONS dict above)
    # ═══════════════════════════════════════════════════════════════════════

SIMULATIONS["angle_sum_property"] = {
    "title": "Triangle Angle Sum",
    "file": "simulations/AngleSumProperty.html",
    "description": """
An interactive triangle simulation where you can drag vertices to change 
the triangle's shape and observe that the sum of interior angles always 
equals 180 degrees. Includes a geometric proof using parallel lines.

What can be demonstrated:
- Triangle interior angles sum to 180°
- Angle sum remains constant regardless of triangle shape
- Geometric proof using parallel lines and alternate angles
- Relationship between triangle angles and parallel line properties
""",
    "cannot_demonstrate": [
        "Exterior angles",
        "Triangle area calculations",
        "Side length relationships",
        "Pythagorean theorem"
    ],
    "initial_params": {
        "vertexA_x": 500,
        "vertexA_y": 150,
        "vertexB_x": 200,
        "vertexB_y": 450,
        "vertexC_x": 800,
        "vertexC_y": 450,
        "show_proof_lines": False
    },
    "parameter_info": {
        "show_proof_lines": {
            "label": "Show Proof Steps",
            "range": "true/false",
            "url_key": "show_proof_lines",
            "effect": "Shows parallel line through vertex A and demonstrates alternate angles proof"
        },
        "vertexA_x": {
            "label": "Vertex A X Position",
            "range": "50-950 pixels",
            "url_key": "vertexA_x",
            "effect": "Horizontal position of top vertex A"
        },
        "vertexA_y": {
            "label": "Vertex A Y Position",
            "range": "50-550 pixels",
            "url_key": "vertexA_y",
            "effect": "Vertical position of top vertex A"
        },
        "vertexB_x": {
            "label": "Vertex B X Position",
            "range": "50-950 pixels",
            "url_key": "vertexB_x",
            "effect": "Horizontal position of bottom-left vertex B"
        },
        "vertexB_y": {
            "label": "Vertex B Y Position",
            "range": "50-550 pixels",
            "url_key": "vertexB_y",
            "effect": "Vertical position of bottom-left vertex B"
        },
        "vertexC_x": {
            "label": "Vertex C X Position",
            "range": "50-950 pixels",
            "url_key": "vertexC_x",
            "effect": "Horizontal position of bottom-right vertex C"
        },
        "vertexC_y": {
            "label": "Vertex C Y Position",
            "range": "50-550 pixels",
            "url_key": "vertexC_y",
            "effect": "Vertical position of bottom-right vertex C"
        }
    },
    "concepts": [
        {
            "id": 1,
            "title": "Triangle Angle Sum Property",
            "description": "The sum of the three interior angles in any triangle is always 180 degrees, regardless of the triangle's shape or size.",
            "key_insight": "No matter how you change the triangle shape, angle A + angle B + angle C always equals 180°",
            "related_params": ["vertexA_x", "vertexA_y", "vertexB_x", "vertexB_y", "vertexC_x", "vertexC_y"]
        },
        {
            "id": 2,
            "title": "Parallel Lines and Alternate Angles",
            "description": "When a line intersects two parallel lines, it creates alternate interior angles that are equal. This property helps prove the angle sum theorem.",
            "key_insight": "A line parallel to the base through vertex A creates alternate angles equal to angles B and C",
            "related_params": ["show_proof_lines"]
        },
        {
            "id": 3,
            "title": "Geometric Proof Visualization",
            "description": "The parallel line proof shows that all three angles can be rearranged at one vertex to form a straight line (180°), proving the angle sum property.",
            "key_insight": "When you show the proof, angles B and C appear at vertex A as alternate angles, and together with angle A, they form a straight line",
            "related_params": ["show_proof_lines"]
        }
    ]
}


def get_quiz_questions(simulation_id: str) -> list:
    """Get quiz questions for a specific simulation."""
    return QUIZ_QUESTIONS.get(simulation_id, [])
