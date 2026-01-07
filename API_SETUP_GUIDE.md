# FastAPI Teaching Agent - Setup Guide for Android Developer

## 📋 Overview
This guide will help you set up and test the FastAPI server that powers the teaching agent for the Android app.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or 3.12
- pip (Python package manager)
- Git
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
# .env file
GOOGLE_API_KEY=your_gemini_api_key_here
```

### Step 4: Start the API Server
```bash
uvicorn api_server:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 5: Test the API
Open a **new terminal** and run:
```bash
python test_api_client.py
```

If all tests pass ✅, the API is ready!

---

## 🔌 API Endpoints

### Base URL
- **Local Development**: `http://127.0.0.1:8000`
- **Android Emulator**: `http://10.0.2.2:8000`
- **Same WiFi Network**: `http://<YOUR_IP>:8000` (find IP with `ifconfig`)

### Available Endpoints

#### 1. Health Check
```http
GET /
```
**Response:**
```json
{
  "service": "Teaching Agent API",
  "version": "1.0.0",
  "status": "online",
  "available_simulations": ["simple_pendulum", "earth_rotation_revolution", "light_shadows"]
}
```

#### 2. List Simulations
```http
GET /api/simulations
```
**Response:**
```json
{
  "simulations": [
    {
      "id": "simple_pendulum",
      "title": "Time & Pendulums",
      "description": "...",
      "concepts_count": 2
    }
  ]
}
```

#### 3. Start Teaching Session
```http
POST /api/session/start
Content-Type: application/json

{
  "simulation_id": "simple_pendulum"
}
```

**Response (201 Created):**
```json
{
  "session_id": "api_session_abc123",
  "teacher_message": {
    "text": "Hey there! Have you ever been on a swing set...",
    "type": "question"
  },
  "simulation": {
    "id": "simple_pendulum",
    "title": "Time & Pendulums",
    "html_url": "https://...",
    "current_params": {"length": 5, "number_of_oscillations": 10}
  },
  "learning_state": {
    "understanding_level": "none",
    "exchange_count": 1,
    "concept_complete": false,
    "session_complete": false
  },
  "concepts": {
    "current_concept": {
      "id": "concept_1",
      "title": "Time Period of a Pendulum"
    },
    "current_index": 0,
    "total": 2
  }
}
```

#### 4. Send Student Response
```http
POST /api/session/{session_id}/respond
Content-Type: application/json

{
  "student_response": "I think it takes longer to swing"
}
```

**Response (200 OK):**
```json
{
  "session_id": "api_session_abc123",
  "teacher_message": {
    "text": "Exactly right! You've made a great observation...",
    "type": "feedback"
  },
  "simulation": {
    "html_url": "https://...",
    "current_params": {"length": 10, "number_of_oscillations": 10},
    "param_change": {
      "parameter": "length",
      "before": 5,
      "after": 10,
      "reason": "To demonstrate the effect of length on time period"
    }
  },
  "learning_state": {
    "understanding_level": "mostly",
    "exchange_count": 2,
    "concept_complete": false,
    "session_complete": false
  }
}
```

#### 5. Get Session State
```http
GET /api/session/{session_id}
```
Returns the same format as the "Send Student Response" endpoint.

---

## 📱 Android Integration Guide

### Connecting from Android Emulator
Use this base URL in your Android app:
```kotlin
val BASE_URL = "http://10.0.2.2:8000"
```

### Connecting from Physical Device (Same WiFi)
1. Find your computer's IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
   Example output: `192.168.1.23`

2. Start server with:
   ```bash
   uvicorn api_server:app --host 0.0.0.0 --port 8000
   ```

3. Use this base URL in Android:
   ```kotlin
   val BASE_URL = "http://192.168.1.23:8000"
   ```

### Sample Android HTTP Request (Retrofit)
```kotlin
interface TeachingAgentApi {
    @POST("/api/session/start")
    suspend fun startSession(@Body request: StartSessionRequest): SessionResponse
    
    @POST("/api/session/{sessionId}/respond")
    suspend fun sendResponse(
        @Path("sessionId") sessionId: String,
        @Body request: StudentResponseRequest
    ): SessionResponse
    
    @GET("/api/session/{sessionId}")
    suspend fun getSession(@Path("sessionId") sessionId: String): SessionResponse
}

data class StartSessionRequest(val simulation_id: String)
data class StudentResponseRequest(val student_response: String)
```

---

## 🧪 Testing the Teaching Agent

### Quick Verification Test
First, verify the API is working:
```bash
python test_api_client.py
```
If all tests pass ✅, proceed to full conversation testing.

---

### Method 1: Interactive Command Line Testing (Recommended)

**Step 1:** Start the server (Terminal 1)
```bash
uvicorn api_server:app --reload --port 8000
```

**Step 2:** Start interactive mode (Terminal 2)
```bash
python test_api_client.py --interactive
```

**Step 3:** Choose a simulation
```
Enter simulation ID: simple_pendulum
```

**Step 4:** Have a real conversation
The agent will ask questions and you respond naturally. Example:

```
Teacher: Hey there! Have you ever been on a swing set and noticed how it moves 
back and forth? [...] What do you predict will happen to the time it takes for 
one full swing? Will a longer swing take more time or less time?

You: I think it takes more time

Teacher: Exactly right! [...] Let me show you in the simulation. OBSERVE: 
Watch what happens when I make the pendulum longer...

You: Yes, I can see it's swinging slower now

Teacher: Great observation! [...] Can you EXPLAIN why a longer pendulum 
takes more time?

You: Maybe because it has to travel a longer distance?

Teacher: That's a good thought! [...] (continues teaching)
```

**Commands:**
- Type your responses naturally (as if you're a student)
- Type `state` to check your learning progress
- Type `quit` when done

**What to observe:**
- Teacher adapts to your answers (correct/wrong/partial)
- Parameters change in simulation when needed
- Progress through concepts (1 of 2, 2 of 2)
- Understanding levels change (none → partial → mostly → full)
- Session completes when all concepts taught

---

### Method 2: Browser Testing with Swagger UI

**Step 1:** Start the server
```bash
uvicorn api_server:app --reload --port 8000
```

**Step 2:** Open Swagger UI
```
http://localhost:8000/docs
```

**Step 3:** Test conversation flow manually

**a) Start a session:**
- Click `POST /api/session/start`
- Click "Try it out"
- Enter:
  ```json
  {
    "simulation_id": "simple_pendulum"
  }
  ```
- Click "Execute"
- **Copy the `session_id`** from response

**b) Send student responses:**
- Click `POST /api/session/{session_id}/respond`
- Click "Try it out"
- Paste your `session_id`
- Enter student response:
  ```json
  {
    "student_response": "I think it takes longer"
  }
  ```
- Click "Execute"
- Read teacher's response
- Repeat for full conversation

**c) Check progress:**
- Click `GET /api/session/{session_id}`
- Enter your `session_id`
- Click "Execute"
- See current learning state

---

### Method 3: Using curl (Command Line)

**Start a session:**
```bash
curl -X POST "http://localhost:8000/api/session/start" \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "simple_pendulum"}'
```

Copy the `session_id` from response, then:

**Send responses:**
```bash
curl -X POST "http://localhost:8000/api/session/{YOUR_SESSION_ID}/respond" \
  -H "Content-Type: application/json" \
  -d '{"student_response": "I think it takes more time"}'
```

**Check state:**
```bash
curl "http://localhost:8000/api/session/{YOUR_SESSION_ID}"
```

---

### Method 4: Postman/Insomnia

**Setup:**
1. Import these endpoints into Postman
2. Set base URL: `http://localhost:8000`
3. Create requests for each endpoint

**Conversation Flow:**
1. **POST** `/api/session/start` → Get `session_id`
2. **POST** `/api/session/{session_id}/respond` → Send student answer
3. Read teacher response
4. Repeat step 2 until session complete
5. **GET** `/api/session/{session_id}` → Check final state

---

## 🎓 Full Teaching Agent Experience

### What Happens During a Conversation

**1. Session Starts**
- Agent introduces the topic
- Sets initial simulation parameters
- Asks first question

**2. Agent Evaluates Your Response**
- Classifies response type (answer, question, observation)
- Assesses understanding level (none/partial/mostly/full)
- Checks if answer is correct

**3. Agent Adapts Teaching Strategy**
- **If correct**: Asks deeper "why" questions
- **If wrong**: Corrects and demonstrates with simulation
- **If stuck**: Provides scaffolding and simplifies
- **If improving**: Continues challenging

**4. Simulation Updates**
- When agent changes parameters, you'll see:
  ```json
  "param_change": {
    "parameter": "length",
    "before": 5,
    "after": 10,
    "reason": "To demonstrate the effect..."
  }
  ```
- Open the `html_url` to see the updated simulation

**5. Progress Through Concepts**
- Each simulation has 2-3 concepts
- Agent teaches one concept at a time
- `concept_complete: true` → moving to next concept
- `session_complete: true` → all concepts done

---

## 📊 Expected Conversation Patterns

### Simple Pendulum (2 concepts)

**Concept 1: Time Period**
- Teacher asks about relationship between length and swing time
- Demonstrates by changing pendulum length
- Student observes and explains
- ~4-6 exchanges

**Concept 2: Multiple Oscillations**
- Teacher introduces counting multiple swings
- Shows why multiple measurements are better
- Student understands measurement accuracy
- ~3-5 exchanges

**Total Session:** ~7-11 exchanges

### Earth Rotation & Revolution (3 concepts)

**Concept 1: Day/Night Cycle**
- Understanding rotation causes day/night
- ~4-6 exchanges

**Concept 2: Seasons**
- Understanding revolution + tilt causes seasons
- ~4-6 exchanges

**Concept 3: Year Length**
- Understanding orbital period
- ~3-5 exchanges

**Total Session:** ~11-17 exchanges

### Light & Shadows (3 concepts)

**Concept 1: Shadow Formation**
- How light creates shadows
- ~4-5 exchanges

**Concept 2: Shadow Direction**
- Light position affects shadow direction
- ~4-5 exchanges

**Concept 3: Shadow Length**
- Distance affects shadow size
- ~4-5 exchanges

**Total Session:** ~12-15 exchanges

---

## 🎯 Testing Checklist for Android Developer

Before integrating with Android app, test these scenarios:

### ✅ Basic Flow
- [ ] Start session with each simulation
- [ ] Send correct answers → agent asks deeper questions
- [ ] Send wrong answers → agent corrects and demonstrates
- [ ] Complete full conversation (all concepts)
- [ ] Check `session_complete: true` at end

### ✅ Parameter Changes
- [ ] Verify `param_change` appears in responses
- [ ] Load `html_url` to see updated simulation
- [ ] Confirm parameters match what agent said

### ✅ Understanding Progression
- [ ] Start at `understanding_level: "none"`
- [ ] Progress through `"partial"`, `"mostly"`, `"full"`
- [ ] See how agent adapts to each level

### ✅ Edge Cases
- [ ] Send very short answer → agent asks for elaboration
- [ ] Ask a question → agent answers it
- [ ] Send random text → agent guides back to topic
- [ ] Retrieve session state mid-conversation

### ✅ Multiple Simulations
- [ ] Test all 3 simulations
- [ ] Verify different concept counts
- [ ] Check simulation-specific content

---

## 🔍 Monitoring Responses

### Important Fields to Track

**Teacher Message:**
```json
"teacher_message": {
  "text": "...",  // Display this in chat
  "type": "question" | "feedback" | "explanation"
}
```

**Simulation State:**
```json
"simulation": {
  "html_url": "...",  // Load in WebView
  "current_params": {...},  // Current values
  "param_change": {...}  // If parameters changed
}
```

**Learning Progress:**
```json
"learning_state": {
  "understanding_level": "partial",  // Show progress indicator
  "exchange_count": 3,  // Message count
  "concept_complete": false,  // Moving to next concept?
  "session_complete": false  // End session?
}
```

**Concept Info:**
```json
"concepts": {
  "current_concept": {
    "title": "Time Period of a Pendulum"
  },
  "current_index": 0,  // 0-based
  "total": 2
}
```

---

## 🎯 Key Concepts for Android App

### 1. Session Management
- Each student conversation gets a unique `session_id`
- Store `session_id` to continue conversations
- Sessions persist in memory (lost on server restart)

### 2. Simulation Updates
- When `param_change` exists in response, update the WebView URL
- Load the new `html_url` to show updated simulation
- Display the `reason` to explain why parameters changed

### 3. Understanding Levels
- `none`: Student doesn't understand
- `partial`: Student has some understanding
- `mostly`: Student mostly understands
- `full`: Student fully understands

Use these to show progress indicators in your UI.

### 4. Progress Tracking
```json
"concepts": {
  "current_index": 0,
  "total": 2
}
```
Show "Concept 1 of 2" to track progress.

### 5. Session Completion
```json
"learning_state": {
  "concept_complete": true,
  "session_complete": false
}
```
- `concept_complete`: Current concept done, moving to next
- `session_complete`: All concepts done, end session

---

## 📂 Important Files

| File | Purpose |
|------|---------|
| `api_server.py` | Main FastAPI application with endpoints |
| `api_integration.py` | Bridge between FastAPI and teaching agent |
| `api_models.py` | Request/response data structures |
| `test_api_client.py` | Testing tool (shows how to use API) |
| `requirements_api.txt` | FastAPI dependencies |
| `FASTAPI_INTEGRATION_GUIDE.md` | Detailed technical documentation |

---

## ❓ Troubleshooting

### Server won't start
**Error**: `Address already in use`
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Then restart server
uvicorn api_server:app --reload --port 8000
```

### Tests fail with "Cannot connect"
- Make sure server is running in another terminal
- Check if port 8000 is accessible
- Try: `curl http://localhost:8000/`

### Android emulator can't reach server
- Use `http://10.0.2.2:8000` (not localhost)
- Check server is running with `--host 0.0.0.0`

### "Backend not available" error
- Check `.env` file has `GOOGLE_API_KEY`
- Make sure all dependencies installed
- Try: `python -c "from streamlit_app.backend_integration import is_backend_available; print(is_backend_available())"`

---