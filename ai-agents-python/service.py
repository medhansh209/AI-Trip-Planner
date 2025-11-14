# service.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from tripPipeline import plan_trip_pipeline
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')


app = FastAPI(title="AI Trip Planner Agents Service")

# ✅ Request body model
class TripRequest(BaseModel):
    origin: Optional[str] = None
    destination: str
    budget: int
    travelers: int
    interests: List[str] = []
    days: Optional[int] = 3

@app.post("/plan-trip")
def plan_trip(req: TripRequest):
    """Run full AI trip planning pipeline."""
    user_input = req.dict()
    print("Received:", user_input)

    try:
        result = plan_trip_pipeline(user_input, use_llm=False)
        return {
            "status": "success",
            "input": user_input,
            "final_itinerary": result["final_itinerary"],
            "optimized_results": result["optimized_results"],
            "research_results": result["research_results"],
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def root():
    return {"message": "AI Trip Planner Python Service is running 🚀"}
