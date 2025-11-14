// routes/planRoute.js
import express from "express";
import { callPythonTripPlanner } from "../agents/bridge.js";

const router = express.Router();

router.post("/", async (req, res) => {
  try {
    console.log("📨 Received Input:", req.body);

    const userInput = {
      origin: req.body.origin || "",
      destination: req.body.destination || "",
      budget: Number(req.body.budget) || 0,
      travelers: Number(req.body.travelers || req.body.travellers || req.body.people || req.body.count),
      interests: req.body.interests
        ? req.body.interests.split(",").map(i => i.trim())
        : [],
      date: req.body.date || new Date().toISOString()
    };

    // Call Python
    const pythonResponse = await callPythonTripPlanner(userInput);
    console.log("🔍 Python Full Response:", pythonResponse);

    const itineraryBlock = pythonResponse.final_itinerary || {};

    console.log("🟦 DATA SENT TO EJS:", {
      input: userInput,
      trips: pythonResponse.final_itinerary,
      generatedText: itineraryBlock.text,
      generatedSummary: itineraryBlock.summary
    });

  return res.render("planTrip", {
    input: userInput,

    // There is NO trips array from python → so send optimized plan as trips
    trips: pythonResponse.optimized_results?.optimized_plan || [],

    // Show AI-generated itinerary
    generatedText: pythonResponse.final_itinerary?.text || "",
    generatedSummary: pythonResponse.final_itinerary?.summary || "",

    // Send hotels
    hotels: pythonResponse.research_results?.hotels || [],

    // Send flights
    flights: pythonResponse.research_results?.flights || [],

    // Send activities
    activities: pythonResponse.research_results?.activities || [],

    error: null
  });


  } catch (err) {
    console.error("❌ ERROR:", err.message);

    return res.render("planTrip", {
      input: req.body,
      trips: [],
      generatedText: "",
      generatedSummary: "",
      optimized: null,
      research: null,
      error: "Error connecting to Python service"
    });
  }
});

export default router;
