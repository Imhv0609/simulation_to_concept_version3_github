# FastAPI Integration Guide for Teaching Agent

## Table of Contents
1. [What is FastAPI?](#what-is-fastapi)
2. [Architecture Overview](#architecture-overview)
3. [API Endpoints Design](#api-endpoints-design)
4. [Endpoint Design Reasoning](#endpoint-design-reasoning)
5. [Complete Request/Response Flows](#complete-requestresponse-flows)
6. [Project Structure](#project-structure)
7. [How It Works - Technical Details](#how-it-works---technical-details)
8. [REST API Best Practices](#rest-api-best-practices)
9. [Alternative Designs Considered](#alternative-designs-considered)
10. [Installation Requirements](#installation-requirements)
11. [Testing Strategy](#testing-strategy)
12. [Questions to Consider](#questions-to-consider)

---

## What is FastAPI?

FastAPI is a modern Python web framework that creates **REST APIs** (web endpoints that apps can call over the internet). Think of it as a "waiter" that:

1. **Receives requests** from your Android app (like "start a new session" or "send student response")
2. **Talks to your LangGraph backend** to process the request
3. **Sends back responses** to the Android app in JSON format

### Key Benefits
- **Fast**: Built on modern async Python
- **Type-Safe**: Uses Pydantic for automatic validation
- **Auto-Documentation**: Generates interactive API docs at `/docs`
- **Easy to Learn**: Simple, intuitive syntax
- **Production-Ready**: Used by major companies (Microsoft, Uber, Netflix)

---

## Architecture Overview

```
┌─────────────────────┐
│   Android App       │
│   (Student UI)      │
└──────────┬──────────┘
           │ HTTP Requests (JSON)
           │ POST /api/session/start
           │ POST /api/session/{id}/respond
           │ GET  /api/session/{id}
           ▼
┌─────────────────────┐
│   FastAPI Server    │  ← We'll create this (api_server.py)
│   (API Layer)       │     - Receives HTTP requests
│   Port 8000         │     - Validates JSON
└──────────┬──────────┘     - Routes to backend
           │ Function Calls  - Formats responses
           │ create_new_session()
           │ send_student_response()
           │ get_current_state()
           ▼
┌─────────────────────┐
│   LangGraph Agent   │  ← Your existing backend
│   (graph.py, nodes) │     - Processes teaching logic
│   MemorySaver       │     - Generates responses
└─────────────────────┘     - Updates state
```

### Flow Example

```
Android App: "POST /api/session/start" with {simulation_id: "simple_pendulum"}
     ↓
FastAPI: Receives request → validates JSON → calls create_new_session()
     ↓
LangGraph: Creates session → runs content_loader → teacher node → generates first message
     ↓
FastAPI: Packages state as JSON response
     ↓
Android App: Receives JSON → displays teacher message → loads simulation URL
```

---

## API Endpoints Design

Based on analyzing your existing `backend_integration.py` functions, we need **3 main endpoints**:

### 1. Start New Session

**Endpoint:** `POST /api/session/start`

**Purpose:** Initialize a new teaching session for a specific simulation

**Request Body:**
```json
{
  "simulation_id": "simple_pendulum",
  "student_id": "optional_student_identifier"
}
```

**Response:**
```json
{
  "session_id": "thread_abc123",
  "simulation": {
    "id": "simple_pendulum",
    "title": "Time & Pendulums",
    "html_url": "https://imhv0609.github.io/.../simple_pendulum.html?length=5&oscillations=10&autoStart=true",
    "current_params": {
      "length": 5,
      "number_of_oscillations": 10
    }
  },
  "concepts": {
    "total": 2,
    "current_index": 0,
    "current_concept": {
      "id": 1,
      "title": "Time Period of a Pendulum",
      "description": "How the length of a pendulum affects how long it takes to complete one swing.",
      "key_insight": "Longer pendulum = longer time period (slower swings)",
      "related_params": ["length"]
    },
    "all_concepts": [...]
  },
  "teacher_message": {
    "text": "Hi friend! Today we're going to explore pendulums...",
    "timestamp": "2026-01-06T10:15:00Z",
    "requires_response": true
  },
  "learning_state": {
    "understanding_level": "none",
    "exchange_count": 0,
    "concept_complete": false,
    "session_complete": false,
    "strategy": "continue",
    "teacher_mode": "encouraging"
  }
}
```

---

### 2. Send Student Response

**Endpoint:** `POST /api/session/{session_id}/respond`

**Purpose:** Send student's message and get teacher's response with updated state

**URL Parameters:**
- `session_id`: The session ID returned from `/start`

**Request Body:**
```json
{
  "student_response": "I think it swings faster?"
}
```

**Response:**
```json
{
  "session_id": "thread_abc123",
  "simulation": {
    "id": "simple_pendulum",
    "html_url": "https://.../simple_pendulum.html?length=8&oscillations=10&autoStart=true",
    "current_params": {
      "length": 8,
      "number_of_oscillations": 10
    },
    "param_change": {
      "parameter": "length",
      "before": 5,
      "after": 8,
      "reason": "To demonstrate that longer pendulum swings slower",
      "before_url": "https://.../simple_pendulum.html?length=5&oscillations=10&autoStart=true",
      "after_url": "https://.../simple_pendulum.html?length=8&oscillations=10&autoStart=true"
    }
  },
  "concepts": {
    "total": 2,
    "current_index": 0,
    "current_concept": {...}
  },
  "teacher_message": {
    "text": "Not quite, friend. Actually, a longer pendulum swings SLOWER, not faster. Let me show you! I've changed the length from 5 to 8 units. OBSERVE: Watch the simulation now...",
    "timestamp": "2026-01-06T10:16:30Z",
    "requires_response": true,
    "correction_made": true
  },
  "learning_state": {
    "understanding_level": "none",
    "understanding_reasoning": "Student gave incorrect answer - needs to observe the correct behavior",
    "exchange_count": 1,
    "concept_complete": false,
    "session_complete": false,
    "strategy": "continue",
    "teacher_mode": "encouraging",
    "trajectory_status": "improving"
  }
}
```

---

### 3. Get Session State

**Endpoint:** `GET /api/session/{session_id}`

**Purpose:** Retrieve current session state (for recovery/restoration)

**URL Parameters:**
- `session_id`: The session ID to retrieve

**Response:**
```json
{
  "session_id": "thread_abc123",
  "simulation": {...},
  "concepts": {...},
  "teacher_message": {...},
  "learning_state": {...},
  "conversation_history": [
    {
      "role": "teacher",
      "content": "Hi friend!...",
      "timestamp": "2026-01-06T10:15:00Z"
    },
    {
      "role": "student", 
      "content": "I think it swings faster?",
      "timestamp": "2026-01-06T10:16:00Z"
    }
  ]
}
```

**Use Cases:**
- App crashes and needs to restore state
- User closes app and reopens later
- Network error recovery
- Debugging and monitoring

---

## Endpoint Design Reasoning

### Why These Specific Endpoints?

I analyzed your existing `backend_integration.py` file and found three core functions:

#### 1. `create_new_session()` → `POST /api/session/start`

**Your existing code:**
```python
def create_new_session() -> Tuple[str, Dict[str, Any]]:
    """Create a new teaching session."""
    thread_id = f"streamlit_session_{uuid.uuid4().hex[:8]}"
    initial_state = create_initial_state(...)
    state = start_session(initial_state, thread_id)
    return thread_id, state
```

**Why this endpoint:**
- Your Streamlit app uses this to start sessions
- Android app needs the same functionality
- Creates a new learning session with fresh state

**URL Design Choices:**
- ✅ `POST /api/session/start` - Clear, RESTful, descriptive
- ❌ `POST /start_session` - Not namespaced, unclear it's an API
- ❌ `POST /create` - Create what?
- ❌ `GET /session/new` - GET shouldn't create resources

---

#### 2. `send_student_response(thread_id, response)` → `POST /api/session/{session_id}/respond`

**Your existing code:**
```python
def send_student_response(thread_id: str, response: str) -> Dict[str, Any]:
    """Send a student response and get the updated state."""
    state = continue_session(response, thread_id)
    return state
```

**Why this endpoint:**
- This is the MAIN interaction loop
- Called repeatedly throughout the conversation
- Student speaks → teacher responds

**URL Design Choices:**
- ✅ `POST /api/session/{session_id}/respond` - Clear hierarchy, RESTful
- ❌ `POST /send_message` - Which session? Not clear
- ❌ `POST /session?id=123` - Query params for resource IDs not RESTful
- ❌ `POST /api/message` - Doesn't show relationship to session

---

#### 3. `get_current_state(thread_id)` → `GET /api/session/{session_id}`

**Your existing code:**
```python
def get_current_state(thread_id: str) -> Dict[str, Any]:
    """Get the current state of a session."""
    return get_session_state(thread_id)
```

**Why this endpoint:**
- Essential for error recovery
- Not used in normal flow, but critical for production
- Allows state restoration after crashes

**URL Design Choices:**
- ✅ `GET /api/session/{session_id}` - Simple, RESTful, clear
- ❌ `GET /get_state?id=123` - Verb in URL, not RESTful
- ❌ `POST /api/session/state` - GET is for retrieval, not POST

---

## Complete Request/Response Flows

### Flow 1: Starting a New Session

```
┌─────────────┐                    ┌─────────────┐                    ┌─────────────┐
│ Android App │                    │   FastAPI   │                    │  LangGraph  │
└──────┬──────┘                    └──────┬──────┘                    └──────┬──────┘
       │                                  │                                   │
       │ POST /api/session/start          │                                   │
       │ {simulation_id: "simple_pendulum"}                                  │
       ├─────────────────────────────────>│                                   │
       │                                  │                                   │
       │                                  │ validate_config()                 │
       │                                  │ set CURRENT_SIMULATION_ID         │
       │                                  │                                   │
       │                                  │ create_new_session()              │
       │                                  ├──────────────────────────────────>│
       │                                  │                                   │
       │                                  │                       content_loader_node()
       │                                  │                       (loads concepts)
       │                                  │                                   │
       │                                  │                       teacher_node()
       │                                  │                       (generates first message)
       │                                  │                                   │
       │                                  │<──────────────────────────────────┤
       │                                  │  (thread_id, state)               │
       │                                  │                                   │
       │                                  │ format_response()                 │
       │                                  │ (convert state to JSON)           │
       │                                  │                                   │
       │<─────────────────────────────────┤                                   │
       │ 200 OK                           │                                   │
       │ {session_id, teacher_message,    │                                   │
       │  simulation_url, concepts, ...}  │                                   │
       │                                  │                                   │
       │ Display welcome message          │                                   │
       │ Load simulation iframe           │                                   │
       │                                  │                                   │
```

---

### Flow 2: Ongoing Conversation (No Parameter Change)

```
┌─────────────┐                    ┌─────────────┐                    ┌─────────────┐
│ Android App │                    │   FastAPI   │                    │  LangGraph  │
└──────┬──────┘                    └──────┬──────┘                    └──────┬──────┘
       │                                  │                                   │
       │ User types: "What is time period?"                                  │
       │                                  │                                   │
       │ POST /session/abc123/respond     │                                   │
       │ {student_response: "What is..."}│                                   │
       ├─────────────────────────────────>│                                   │
       │                                  │                                   │
       │                                  │ send_student_response(id, msg)    │
       │                                  ├──────────────────────────────────>│
       │                                  │                                   │
       │                                  │                       evaluator_node()
       │                                  │                       (classifies as question)
       │                                  │                                   │
       │                                  │                       trajectory_node()
       │                                  │                       (analyzes progress)
       │                                  │                                   │
       │                                  │                       strategy_node()
       │                                  │                       (decides: continue)
       │                                  │                                   │
       │                                  │                       teacher_node()
       │                                  │                       (answers question)
       │                                  │                                   │
       │                                  │<──────────────────────────────────┤
       │                                  │  (updated_state)                  │
       │                                  │                                   │
       │<─────────────────────────────────┤                                   │
       │ 200 OK                           │                                   │
       │ {teacher_message: "Time period   │                                   │
       │  is the time for one swing...",  │                                   │
       │  no param_change}                │                                   │
       │                                  │                                   │
       │ Display teacher's answer         │                                   │
       │ (no simulation update)           │                                   │
       │                                  │                                   │
```

---

### Flow 3: Conversation with Parameter Change

```
┌─────────────┐                    ┌─────────────┐                    ┌─────────────┐
│ Android App │                    │   FastAPI   │                    │  LangGraph  │
└──────┬──────┘                    └──────┬──────┘                    └──────┬──────┘
       │                                  │                                   │
       │ User types: "I think it swings faster"                              │
       │                                  │                                   │
       │ POST /session/abc123/respond     │                                   │
       │ {student_response: "...faster"}  │                                   │
       ├─────────────────────────────────>│                                   │
       │                                  │                                   │
       │                                  │ send_student_response(id, msg)    │
       │                                  ├──────────────────────────────────>│
       │                                  │                                   │
       │                                  │                       evaluator_node()
       │                                  │                       (level: "none", wrong answer)
       │                                  │                                   │
       │                                  │                       trajectory_node()
       │                                  │                       (status: "improving")
       │                                  │                                   │
       │                                  │                       strategy_node()
       │                                  │                       (decides: continue)
       │                                  │                                   │
       │                                  │                       teacher_node()
       │                                  │                       - Detects wrong answer
       │                                  │                       - Decides to change length 5→8
       │                                  │                       - Generates corrective message
       │                                  │                                   │
       │                                  │<──────────────────────────────────┤
       │                                  │  (state with param change)        │
       │                                  │                                   │
       │<─────────────────────────────────┤                                   │
       │ 200 OK                           │                                   │
       │ {teacher_message: "Not quite...", │                                  │
       │  param_change: {                 │                                   │
       │    parameter: "length",          │                                   │
       │    before: 5, after: 8,          │                                   │
       │    before_url: "...length=5",    │                                   │
       │    after_url: "...length=8"      │                                   │
       │  }}                              │                                   │
       │                                  │                                   │
       │ Display teacher message          │                                   │
       │ Show before/after comparison     │                                   │
       │ Update simulation to length=8    │                                   │
       │                                  │                                   │
```

---

### Flow 4: Error Recovery

```
┌─────────────┐                    ┌─────────────┐                    ┌─────────────┐
│ Android App │                    │   FastAPI   │                    │  LangGraph  │
└──────┬──────┘                    └──────┬──────┘                    └──────┬──────┘
       │                                  │                                   │
       │ App crashes during conversation  │                                   │
       │ User reopens app                 │                                   │
       │                                  │                                   │
       │ App has session_id saved         │                                   │
       │ in SharedPreferences             │                                   │
       │                                  │                                   │
       │ GET /api/session/abc123          │                                   │
       ├─────────────────────────────────>│                                   │
       │                                  │                                   │
       │                                  │ get_current_state(thread_id)      │
       │                                  ├──────────────────────────────────>│
       │                                  │                                   │
       │                                  │<──────────────────────────────────┤
       │                                  │  (full current state)             │
       │                                  │                                   │
       │<─────────────────────────────────┤                                   │
       │ 200 OK                           │                                   │
       │ {full state with:                │                                   │
       │  - conversation history          │                                   │
       │  - current concept               │                                   │
       │  - simulation params             │                                   │
       │  - understanding level           │                                   │
       │  - all metadata}                 │                                   │
       │                                  │                                   │
       │ Restore UI to exact state        │                                   │
       │ Load simulation with params      │                                   │
       │ Show conversation history        │                                   │
       │ User can continue learning       │                                   │
       │                                  │                                   │
```

---

## Project Structure

After integration, your project will have these new files:

```
simulation_to_concept_version3_github/
├── main.py                           # Terminal runner (existing)
├── graph.py                          # LangGraph workflow (existing)
├── state.py                          # State definitions (existing)
├── config.py                         # Configuration (existing)
├── simulations_config.py             # Simulation metadata (existing)
├── nodes/                            # All nodes (existing)
│   ├── content_loader.py
│   ├── teacher.py
│   ├── evaluator.py
│   ├── trajectory.py
│   └── strategy.py
├── streamlit_app/                    # Streamlit UI (existing)
│   ├── app.py
│   └── backend_integration.py
│
├── api_server.py                     # 🆕 FastAPI server (main entry point)
├── api_integration.py                # 🆕 Helper functions for API
├── api_models.py                     # 🆕 Pydantic request/response models
├── test_api_client.py                # 🆕 Test client script
├── requirements_api.txt              # 🆕 FastAPI dependencies
└── FASTAPI_INTEGRATION_GUIDE.md      # 🆕 This documentation
```

---

## How It Works - Technical Details

### File 1: `api_models.py` (Request/Response Schemas)

This defines the structure of data using Pydantic:

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class StartSessionRequest(BaseModel):
    """Request to start a new teaching session"""
    simulation_id: str = Field(..., description="ID of simulation (simple_pendulum, etc.)")
    student_id: Optional[str] = Field(None, description="Optional student identifier")

class StudentResponseRequest(BaseModel):
    """Request to send student's response"""
    student_response: str = Field(..., description="What the student said/typed")

class TeacherMessage(BaseModel):
    """Teacher's message structure"""
    text: str
    timestamp: str
    requires_response: bool
    correction_made: Optional[bool] = False
    asks_for_reasoning: Optional[bool] = False

class SimulationState(BaseModel):
    """Current simulation state"""
    id: str
    title: str
    html_url: str
    current_params: Dict[str, Any]
    param_change: Optional[Dict[str, Any]] = None

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

class SessionResponse(BaseModel):
    """Complete response for any API call"""
    session_id: str
    simulation: SimulationState
    concepts: Dict[str, Any]
    teacher_message: TeacherMessage
    learning_state: LearningState
```

---

### File 2: `api_integration.py` (Bridge Layer)

This converts between API format and your LangGraph backend:

```python
import os
from datetime import datetime
from typing import Dict, Any, Tuple
from config import build_simulation_url, CURRENT_SIMULATION_ID
from simulations_config import get_simulation

def set_simulation_environment(simulation_id: str):
    """Set environment variable for simulation selection"""
    os.environ['SIMULATION_ID'] = simulation_id

def format_api_response(thread_id: str, state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert LangGraph state to API response format.
    
    This takes the raw state from your backend and packages it
    nicely for the Android app.
    """
    # Get simulation info
    sim_config = get_simulation(state.get('simulation_id', CURRENT_SIMULATION_ID))
    
    # Build current simulation URL
    current_params = state.get('current_params', {})
    sim_url = build_simulation_url(current_params)
    
    # Check for parameter changes
    param_change = None
    param_history = state.get('parameter_history', [])
    if param_history:
        last_change = param_history[-1]
        param_change = {
            "parameter": last_change['parameter'],
            "before": last_change['old_value'],
            "after": last_change['new_value'],
            "reason": last_change['reason'],
            "before_url": build_simulation_url({
                **current_params,
                last_change['parameter']: last_change['old_value']
            }),
            "after_url": sim_url
        }
    
    # Format concepts
    concepts = state.get('concepts', [])
    current_idx = state.get('current_concept_index', 0)
    
    response = {
        "session_id": thread_id,
        "simulation": {
            "id": sim_config['id'],
            "title": sim_config['title'],
            "html_url": sim_url,
            "current_params": current_params,
            "param_change": param_change
        },
        "concepts": {
            "total": len(concepts),
            "current_index": current_idx,
            "current_concept": concepts[current_idx] if current_idx < len(concepts) else None,
            "all_concepts": concepts
        },
        "teacher_message": {
            "text": state.get('last_teacher_message', ''),
            "timestamp": datetime.now().isoformat() + 'Z',
            "requires_response": not state.get('session_complete', False)
        },
        "learning_state": {
            "understanding_level": state.get('understanding_level', 'none'),
            "understanding_reasoning": state.get('understanding_reasoning'),
            "exchange_count": state.get('exchange_count', 0),
            "concept_complete": state.get('concept_complete', False),
            "session_complete": state.get('session_complete', False),
            "strategy": state.get('strategy', 'continue'),
            "teacher_mode": state.get('teacher_mode', 'encouraging'),
            "trajectory_status": state.get('trajectory_status')
        }
    }
    
    return response

def create_teaching_session(simulation_id: str) -> Tuple[str, Dict[str, Any]]:
    """
    Create a new teaching session for specified simulation.
    
    Returns: (session_id, formatted_api_response)
    """
    # Set simulation in environment
    set_simulation_environment(simulation_id)
    
    # Import after environment is set
    from streamlit_app.backend_integration import create_new_session
    
    # Create session using existing backend
    thread_id, state = create_new_session()
    
    # Format for API
    response = format_api_response(thread_id, state)
    
    return thread_id, response

def process_student_input(session_id: str, student_response: str) -> Dict[str, Any]:
    """
    Process student's response and return formatted API response.
    
    Returns: formatted_api_response
    """
    from streamlit_app.backend_integration import send_student_response
    
    # Process through existing backend
    state = send_student_response(session_id, student_response)
    
    # Format for API
    response = format_api_response(session_id, state)
    
    return response

def get_session_info(session_id: str) -> Dict[str, Any]:
    """
    Get current session state.
    
    Returns: formatted_api_response
    """
    from streamlit_app.backend_integration import get_current_state
    
    # Get state from existing backend
    state = get_current_state(session_id)
    
    # Format for API
    response = format_api_response(session_id, state)
    
    return response
```

---

### File 3: `api_server.py` (FastAPI Application)

This is the main API server:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api_models import (
    StartSessionRequest, 
    StudentResponseRequest,
    SessionResponse
)
from api_integration import (
    create_teaching_session,
    process_student_input,
    get_session_info
)
import traceback

# Create FastAPI app
app = FastAPI(
    title="Adaptive Teaching Agent API",
    description="REST API for Android app to interact with the teaching agent",
    version="1.0.0"
)

# Enable CORS for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Teaching Agent API",
        "version": "1.0.0"
    }

@app.post("/api/session/start", response_model=SessionResponse)
async def start_session(request: StartSessionRequest):
    """
    Start a new teaching session.
    
    Creates a new session for the specified simulation and returns
    the initial teacher message and simulation state.
    """
    try:
        session_id, response = create_teaching_session(request.simulation_id)
        return response
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create session: {str(e)}"
        )

@app.post("/api/session/{session_id}/respond", response_model=SessionResponse)
async def send_response(session_id: str, request: StudentResponseRequest):
    """
    Send a student response and get teacher's reply.
    
    Processes the student's input through the teaching agent and returns
    the teacher's response with updated simulation state.
    """
    try:
        response = process_student_input(session_id, request.student_response)
        return response
        
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found"
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process response: {str(e)}"
        )

@app.get("/api/session/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """
    Get current session state.
    
    Retrieves the complete current state of a session.
    Useful for recovery after app restart or network issues.
    """
    try:
        response = get_session_info(session_id)
        return response
        
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found"
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get session: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## REST API Best Practices

### 1. Resource-Based URLs

URLs should represent **resources** (nouns), not actions (verbs):

```
✅ Good (RESTful):
   /api/session/{id}              # Session is a resource
   /api/session/{id}/respond      # Action on that resource
   /api/simulations               # Collection of resources

❌ Bad (Not RESTful):
   /api/get_session               # Verb in URL
   /api/sendResponse              # camelCase + verb
   /api/createNewSession          # Too verbose, has verb
```

### 2. HTTP Methods Match Semantics

Use the right HTTP method for the operation:

| Method | Purpose | Example | Idempotent? |
|--------|---------|---------|-------------|
| GET | Retrieve data | Get session state | Yes |
| POST | Create resource or send data | Start session, send message | No |
| PUT | Update entire resource | Replace entire session | Yes |
| PATCH | Update part of resource | Update one field | Yes |
| DELETE | Remove resource | End session | Yes |

**Our Usage:**
```
GET    /api/session/{id}          # Retrieve (safe, no changes)
POST   /api/session/start          # Create new resource
POST   /api/session/{id}/respond   # Send data (not idempotent)
```

### 3. Hierarchical URL Structure

URLs should show relationships:

```
/api                               # API namespace
  /session                         # Resource collection
    /start                         # Action to create
    /{session_id}                  # Specific resource
      (GET)                        # Get that session
      /respond                     # Action on that session
```

### 4. Consistent Response Format

All responses follow the same structure:

```json
{
  "session_id": "...",      // Always include context
  "simulation": {...},      // Grouped related data
  "concepts": {...},        // Clear naming
  "teacher_message": {...}, // Nested objects for structure
  "learning_state": {...}   // Status information
}
```

### 5. Proper Status Codes

```
200 OK              # Success
201 Created         # Resource created
400 Bad Request     # Invalid input
404 Not Found       # Resource doesn't exist
500 Server Error    # Internal error
```

### 6. API Versioning

Include version in URL for future compatibility:

```
/api/v1/session/start      # Version 1
/api/v2/session/start      # Future version 2
```

Currently we use `/api/` but can add `/v1/` if needed.

---

## Alternative Designs Considered

### Option A: Simpler (Single Endpoint)

**Design:**
```
POST /api/chat
  - If no session_id in body → create new session
  - If session_id in body → continue existing session
```

**Pros:**
- Only 1 endpoint to document
- Simpler for very basic clients

**Cons:**
- Less clear what operation is happening
- Mixes creation and continuation logic
- Harder to add different features later
- Not RESTful (single endpoint doing multiple things)

**Verdict:** ❌ Not recommended - sacrifices clarity for brevity

---

### Option B: More Granular

**Design:**
```
POST   /api/session                          # Create new
GET    /api/session/{id}                     # Get state
POST   /api/session/{id}/message             # Send message
GET    /api/session/{id}/concepts            # Get concepts
GET    /api/session/{id}/simulation          # Get simulation URL
PATCH  /api/session/{id}/parameters          # Change params
DELETE /api/session/{id}                     # End session
GET    /api/simulations                      # List available
```

**Pros:**
- Very explicit - each operation has its own endpoint
- Follows REST conventions strictly
- Easy to add permissions per endpoint

**Cons:**
- Too many endpoints for current needs
- More API calls needed from client
- Overhead of multiple HTTP requests
- Overkill for our use case

**Verdict:** ❌ Over-engineered for current requirements

---

### Option C: WebSocket (Real-time Bidirectional)

**Design:**
```
ws://api/session/{id}
  Client → Server: {"action": "message", "content": "..."}
  Server → Client: {"type": "teacher_response", "content": "..."}
  Server → Client: {"type": "param_change", "data": {...}}
```

**Pros:**
- True real-time bidirectional communication
- Lower latency for rapid exchanges
- Can push updates to client without polling

**Cons:**
- More complex to implement and debug
- Requires persistent connection (battery drain on mobile)
- Harder to test with standard tools
- Overkill - teaching is not real-time chat
- WebSocket connections can be blocked by firewalls

**Verdict:** ❌ Unnecessary complexity for our use case

---

### Option D: GraphQL

**Design:**
```
POST /graphql
{
  query {
    session(id: "abc123") {
      teacherMessage
      simulation { url, params }
      concepts { title, description }
    }
  }
}
```

**Pros:**
- Client requests exactly what it needs
- Single endpoint for all queries
- Strongly typed schema

**Cons:**
- Requires GraphQL knowledge (learning curve)
- More setup complexity
- Overkill for simple CRUD operations
- Our responses are already well-structured

**Verdict:** ❌ Too complex for current needs

---

### **✅ Our Choice: 3 RESTful Endpoints**

**Why This Is Best:**

1. ✅ **Matches your existing functions** directly
   - `create_new_session()` → `/api/session/start`
   - `send_student_response()` → `/api/session/{id}/respond`
   - `get_current_state()` → `/api/session/{id}`

2. ✅ **Simple enough** for Android dev to understand immediately

3. ✅ **Complete enough** to handle all scenarios:
   - Start new session
   - Ongoing conversation
   - Error recovery

4. ✅ **Follows REST standards** that most developers know

5. ✅ **Easy to test** with curl, Postman, or Python

6. ✅ **Room to grow** - can add more endpoints later without breaking existing

---

## Installation Requirements

### New Dependencies

Add to `requirements_api.txt`:

```txt
# FastAPI and Server
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3

# For testing
httpx==0.26.0           # Async HTTP client for testing
requests==2.31.0        # Simple HTTP client
```

### Installation Commands

```bash
# Install API dependencies
pip install -r requirements_api.txt

# Or install individually
pip install fastapi uvicorn pydantic httpx requests
```

### Verify Installation

```bash
# Check FastAPI version
python -c "import fastapi; print(fastapi.__version__)"

# Check Uvicorn version
python -c "import uvicorn; print(uvicorn.__version__)"
```

---

## Testing Strategy

### Phase 1: Start the Server

**Terminal 1 - Run FastAPI Server:**
```bash
cd /path/to/simulation_to_concept_version3_github

# Start server with auto-reload (for development)
uvicorn api_server:app --reload --port 8000

# Server will output:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [xxxxx] using StatReload
# INFO:     Started server process [xxxxx]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

**Server is now running!** It will automatically reload when you change code.

---

### Phase 2: Test with curl Commands

**Terminal 2 - Send Requests:**

#### Test 1: Health Check
```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "status": "online",
  "service": "Teaching Agent API",
  "version": "1.0.0"
}
```

---

#### Test 2: Start New Session
```bash
curl -X POST http://localhost:8000/api/session/start \
  -H "Content-Type: application/json" \
  -d '{
    "simulation_id": "simple_pendulum"
  }'
```

**Expected Response:**
```json
{
  "session_id": "thread_abc123",
  "simulation": {
    "id": "simple_pendulum",
    "title": "Time & Pendulums",
    "html_url": "https://...",
    "current_params": {"length": 5, "number_of_oscillations": 10}
  },
  "teacher_message": {
    "text": "Hi friend! Today we're going to explore pendulums...",
    ...
  },
  ...
}
```

**Save the session_id** for next requests!

---

#### Test 3: Send Student Response
```bash
# Replace {session_id} with actual ID from previous response
curl -X POST http://localhost:8000/api/session/{session_id}/respond \
  -H "Content-Type: application/json" \
  -d '{
    "student_response": "I think it swings faster?"
  }'
```

**Expected Response:**
```json
{
  "session_id": "thread_abc123",
  "simulation": {
    "current_params": {"length": 8, "number_of_oscillations": 10},
    "param_change": {
      "parameter": "length",
      "before": 5,
      "after": 8,
      ...
    }
  },
  "teacher_message": {
    "text": "Not quite, friend. Actually, a longer pendulum swings SLOWER...",
    ...
  },
  ...
}
```

---

#### Test 4: Get Session State
```bash
curl http://localhost:8000/api/session/{session_id}
```

**Expected Response:**
```json
{
  "session_id": "thread_abc123",
  "simulation": {...},
  "concepts": {...},
  ...
}
```

---

### Phase 3: Test with Python Script

Create `test_api_client.py`:

```python
"""
Test client for Teaching Agent API
Simulates how Android app will interact with the API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def pretty_print(data):
    """Print JSON nicely"""
    print(json.dumps(data, indent=2))

def test_complete_session():
    """Test a complete teaching session"""
    
    print("\n" + "="*60)
    print("TEST: Complete Teaching Session")
    print("="*60)
    
    # Step 1: Start new session
    print("\n1. Starting new session...")
    response = requests.post(
        f"{BASE_URL}/api/session/start",
        json={"simulation_id": "simple_pendulum"}
    )
    
    if response.status_code != 200:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    session_id = data["session_id"]
    
    print(f"✅ Session created: {session_id}")
    print(f"📝 Teacher says: {data['teacher_message']['text'][:100]}...")
    print(f"🔗 Simulation URL: {data['simulation']['html_url'][:80]}...")
    
    # Step 2: Send first response
    print("\n2. Sending student response...")
    time.sleep(1)  # Simulate human thinking time
    
    response = requests.post(
        f"{BASE_URL}/api/session/{session_id}/respond",
        json={"student_response": "I think it swings faster?"}
    )
    
    if response.status_code != 200:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    
    print(f"📝 Teacher says: {data['teacher_message']['text'][:100]}...")
    
    if data['simulation'].get('param_change'):
        print("⚙️ Parameters changed:")
        change = data['simulation']['param_change']
        print(f"   {change['parameter']}: {change['before']} → {change['after']}")
        print(f"   Reason: {change['reason']}")
    
    print(f"📊 Understanding: {data['learning_state']['understanding_level']}")
    
    # Step 3: Get session state
    print("\n3. Retrieving session state...")
    response = requests.get(f"{BASE_URL}/api/session/{session_id}")
    
    if response.status_code != 200:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    print(f"✅ Session state retrieved")
    print(f"📊 Exchange count: {data['learning_state']['exchange_count']}")
    print(f"🎯 Current concept: {data['concepts']['current_concept']['title']}")
    
    print("\n" + "="*60)
    print("✅ All tests passed!")
    print("="*60)

if __name__ == "__main__":
    test_complete_session()
```

**Run the test:**
```bash
python test_api_client.py
```

---

### Phase 4: Interactive API Documentation

FastAPI automatically generates interactive documentation!

**Open in browser:**
```
http://localhost:8000/docs
```

**Features:**
- See all endpoints with descriptions
- Try endpoints directly from browser
- See request/response schemas
- No need for curl or Postman!

**Alternative docs:**
```
http://localhost:8000/redoc
```

---

### Phase 5: Test with httpie (Optional - Prettier Output)

If you want nicer formatting than curl:

**Install httpie:**
```bash
pip install httpie
```

**Use it:**
```bash
# Health check
http localhost:8000/

# Start session
http POST localhost:8000/api/session/start simulation_id=simple_pendulum

# Send response
http POST localhost:8000/api/session/abc123/respond student_response="I think faster"

# Get state
http localhost:8000/api/session/abc123
```

**Output is colored and formatted automatically!**

---

## Questions to Consider

Before we implement, please think about these questions:

### 1. Session Management

**Question:** Should we store sessions in memory or database?

**Option A: Memory (Current - MemorySaver)**
- ✅ Simple, no database needed
- ✅ Fast
- ❌ Sessions lost if server restarts
- ❌ Doesn't scale to multiple servers

**Option B: Database (Redis, PostgreSQL)**
- ✅ Persistent across restarts
- ✅ Can scale to multiple servers
- ❌ More complex setup
- ❌ Slower (network calls)

**My Recommendation:** Start with Memory for development/testing, move to database for production.

---

### 2. Response Format

**Question:** Does the JSON format match what your Android developer needs?

We're following the format in `sample_api_responses.json` you created. Should we:
- Keep it as-is?
- Add more fields?
- Remove some fields?
- Change naming?

---

### 3. Error Handling

**Question:** What should happen when things go wrong?

**Scenarios:**
1. Invalid simulation_id provided → Return 400 with list of valid IDs?
2. Session_id not found → Return 404 with helpful message?
3. LangGraph throws error → Return 500 with generic message (hide internals)?

**My Recommendation:** Clear error messages for development, generic for production.

---

### 4. CORS Configuration

**Question:** Will Android app need CORS headers?

**Current:** Allow all origins (`*`) - fine for development

**Production:** Should restrict to:
```python
allow_origins=[
    "https://your-android-app-domain.com",
    "http://localhost:3000"  # for web testing
]
```

---

### 5. Authentication

**Question:** Should API require authentication?

**Current:** No authentication - anyone can access

**Options:**
- API Keys in headers
- JWT tokens
- OAuth2

**My Recommendation:** Start without auth for simplicity, add later if needed.

---

### 6. Rate Limiting

**Question:** Should we limit how many requests a client can make?

**Examples:**
- 100 requests per minute per IP
- 1000 requests per day per student_id

**My Recommendation:** Add later if abuse becomes an issue.

---

### 7. Testing Tools Preference

**Question:** What do you want to use for testing?

**Options:**
a) **curl** - Works everywhere, simple
b) **httpie** - Prettier output, easier syntax
c) **Python requests** - Most like real client
d) **FastAPI /docs** - Interactive browser UI
e) **All of the above**

**My Recommendation:** Start with FastAPI `/docs` (easiest), then Python script (most realistic).

---

### 8. Deployment

**Question:** Where will this API be hosted?

**Options:**
- Local development only
- Cloud server (AWS, GCP, Azure)
- Heroku, Railway, Render (easier)
- Docker container

**Different hosting needs different setup.**

---

## Next Steps

Once you've reviewed this document and thought about the questions:

1. **Let me know if anything is unclear** - I'll explain in more detail

2. **Answer the questions** (or tell me to decide)

3. **We'll implement** the FastAPI integration together

4. **We'll test** with two terminals to verify everything works

5. **Document** any Android-specific requirements

---

## Summary

**What We're Building:**
- REST API with 3 endpoints
- Bridges Android app to your LangGraph teaching agent
- JSON request/response format
- Easy to test and debug

**Why This Design:**
- Matches your existing backend functions
- Simple enough to implement quickly
- Complete enough for all scenarios
- Follows industry standards
- Easy to extend later

**Ready to proceed when you are!** 🚀
