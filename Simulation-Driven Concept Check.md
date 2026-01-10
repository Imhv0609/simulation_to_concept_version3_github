# Simulation-Driven Concept Check

Reading the parameter changes from the html for an interactive Quiz based on Simulation. This enables students to explore simulations by adjusting parameters through gestures or controls, submit their final state, and receive immediate, rule-based evaluation with guided retries and concept reinforcement.

### Example Questions that need the student to change the parameters and explore:

* Change the parameters to have the Time period greater than 2 units. (current time period is 1 unit)  
* Change the parameters to have the partial Shadow/ lighter Shadow by changing the parameters.  
* Change the parameters to have the ph scale 7 and above.  
* Can you make the pendulum swing even slower without touching anything else?  
* Can you keep increasing pH? Does the change feel gradual or sudden?

### Student Interaction Flow:

Here the Students can drag the simulations through gestures or change the parameters using the Adjust option. Finally, they need to click on submit for submitting it. Evaluation of the parameters needs to happen just after submitting.

Student Interaction Flow chart:  
Adjust parameters (gesture / sliders)  
        ↓  
Observe metrics / visuals  
        ↓  
Click SUBMIT  
        ↓  
Evaluation triggered

### Evaluation and Socratic LLM Handling:

* Answer is Right 100% \-\> Acknowledge, celebrate and move on.  
* Answer is Partially right 50%+ \-\> Mention they have missed a piece, ask: do they want to retry once more. Again if the answer is wrong, then bring in the concept and missing piece. Ask them to retry. If again, wrong then summarize and conclude. Max retries 3\.  
* Answer is Wrong less than 50% \-\> Mention they are wrong but appreciate the efforts,ask: do they want to retry once more. Again if the answer is wrong, then bring in the concept and missing piece. Ask them to retry. If again, wrong then summarize and conclude. Max retires 3\.

### Reading the parameter changes from the html ui, recommended method:

HTML → Kotlin → FastAPI (HTTP)  
No need for websocket based hosting in Phase 1\.

### Sample FastAPI creation:

##### Type:

POST /evaluate

##### Request

{  
  "simulation\_id": "pendulum\_time\_period",  
  "attempt": 1,  
  "parameters": {  
    "time\_period": 2.3,  
    "length": 1.2,  
    "gravity": 9.8  
  }  
}

##### Sample FastAPI code:

from fastapi import FastAPI  
from pydantic import BaseModel

app \= FastAPI()

class EvalRequest(BaseModel):  
    simulation\_id: str  
    attempt: int  
    parameters: dict

@app.post("/evaluate")  
def evaluate(req: EvalRequest):  
    score \= 0.0

    if req.simulation\_id \== "pendulum\_time\_period":  
        if req.parameters.get("time\_period", 0\) \> 2:  
            score \= 1.0  
        elif req.parameters.get("time\_period", 0\) \> 1.5:  
            score \= 0.6  
        else:  
            score \= 0.3

    status \= (  
        "RIGHT" if score \== 1.0 else  
        "PARTIALLY\_RIGHT" if score \>= 0.5 else  
        "WRONG"  
    )

    return {  
        "score": score,  
        "status": status,  
        "allow\_retry": score \< 1.0  
    }

##### Sample cURL:

curl \-X POST http://localhost:8000/evaluate \\  
  \-H "Content-Type: application/json" \\  
  \-d '{  
    "simulation\_id": "pendulum\_time\_period",  
    "attempt": 1,  
    "parameters": {  
      "time\_period": 2.3  
    }  
  }'

##### Sample Response:

{  
  "score": 1.0,  
  "status": "RIGHT",  
  "allow\_retry": false  
}

