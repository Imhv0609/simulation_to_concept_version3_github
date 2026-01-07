"""
API Request/Response Models
============================
Pydantic models for FastAPI request validation and response serialization.
These define the structure of data exchanged between Android app and API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


# ═══════════════════════════════════════════════════════════════════════
# REQUEST MODELS
# ═══════════════════════════════════════════════════════════════════════

class StartSessionRequest(BaseModel):
    """Request to start a new teaching session"""
    simulation_id: str = Field(
        ..., 
        description="ID of simulation: 'simple_pendulum', 'earth_rotation_revolution', or 'light_shadows'"
    )
    student_id: Optional[str] = Field(
        None, 
        description="Optional student identifier for tracking"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "simulation_id": "simple_pendulum",
                "student_id": "student_12345"
            }
        }


class StudentResponseRequest(BaseModel):
    """Request to send student's response"""
    student_response: str = Field(
        ..., 
        description="What the student typed/said"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_response": "I think it swings faster?"
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# RESPONSE MODELS (Nested Structure)
# ═══════════════════════════════════════════════════════════════════════

class ParameterChange(BaseModel):
    """Details about a parameter change"""
    parameter: str
    before: Any
    after: Any
    reason: str
    before_url: str
    after_url: str


class SimulationState(BaseModel):
    """Current simulation state"""
    id: str
    title: str
    html_url: str
    current_params: Dict[str, Any]
    param_change: Optional[ParameterChange] = None


class ConceptInfo(BaseModel):
    """Information about a concept"""
    id: int
    title: str
    description: str
    key_insight: str
    related_params: List[str]


class ConceptsState(BaseModel):
    """Current concept state"""
    total: int
    current_index: int
    current_concept: Optional[ConceptInfo] = None
    all_concepts: List[ConceptInfo] = []
    all_completed: Optional[bool] = False
    previous_concept: Optional[Dict[str, Any]] = None


class TeacherMessage(BaseModel):
    """Teacher's message structure"""
    text: str
    timestamp: str
    requires_response: bool
    correction_made: Optional[bool] = False
    asks_for_reasoning: Optional[bool] = False
    concept_transition: Optional[bool] = False
    session_ending: Optional[bool] = False


class LearningState(BaseModel):
    """Student's learning state"""
    understanding_level: str
    understanding_reasoning: Optional[str] = None
    exchange_count: int
    concept_complete: bool
    session_complete: bool
    strategy: str
    teacher_mode: str
    trajectory_status: Optional[str] = None
    needs_deeper: Optional[bool] = False


class SessionResponse(BaseModel):
    """Complete response for session operations"""
    session_id: str
    simulation: SimulationState
    concepts: ConceptsState
    teacher_message: TeacherMessage
    learning_state: LearningState
    summary: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "thread_abc123",
                "simulation": {
                    "id": "simple_pendulum",
                    "title": "Time & Pendulums",
                    "html_url": "https://imhv0609.github.io/.../simple_pendulum.html",
                    "current_params": {"length": 5, "number_of_oscillations": 10},
                    "param_change": None
                },
                "concepts": {
                    "total": 2,
                    "current_index": 0,
                    "current_concept": {
                        "id": 1,
                        "title": "Time Period of a Pendulum",
                        "description": "How length affects swing time",
                        "key_insight": "Longer = slower",
                        "related_params": ["length"]
                    },
                    "all_concepts": []
                },
                "teacher_message": {
                    "text": "Hi friend! Today we're going to explore pendulums...",
                    "timestamp": "2026-01-06T10:15:00Z",
                    "requires_response": True
                },
                "learning_state": {
                    "understanding_level": "none",
                    "exchange_count": 0,
                    "concept_complete": False,
                    "session_complete": False,
                    "strategy": "continue",
                    "teacher_mode": "encouraging"
                }
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# ERROR RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: str
    status_code: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Session Not Found",
                "detail": "Session thread_abc123 does not exist",
                "status_code": 404
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# HELPER RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    available_simulations: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "online",
                "service": "Teaching Agent API",
                "version": "1.0.0",
                "available_simulations": [
                    "simple_pendulum",
                    "earth_rotation_revolution", 
                    "light_shadows"
                ]
            }
        }
