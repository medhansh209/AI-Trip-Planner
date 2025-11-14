// agents/bridge.js
import axios from "axios";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

// ✅ Python FastAPI base URL (from .env)
const PYTHON_BASE_URL = process.env.PYTHON_BASE_URL || "http://127.0.0.1:5001";

/**
 * Call Python FastAPI's /plan-trip endpoint
 * @param {Object} tripData - Trip request payload
 * @returns {Object} Python response (itinerary, optimization, research)
 */
export const callPythonTripPlanner = async (tripData) => {
  try {
    console.log("🌉 Sending data to Python service:", tripData);

    const response = await axios.post(`${PYTHON_BASE_URL}/plan-trip`, tripData, {
      headers: { "Content-Type": "application/json" },
      timeout: 30000, // 30s timeout
    });

    console.log("✅ Received response from Python service");
    return response.data;
  } catch (error) {
    console.error("❌ Error calling Python service:", error.message);

    // Handle specific error cases
    if (error.code === "ECONNREFUSED") {
      return { status: "error", message: "Cannot connect to Python backend. Make sure FastAPI is running." };
    }
    if (error.code === "ETIMEDOUT") {
      return { status: "error", message: "Python service request timed out." };
    }

    return { status: "error", message: error.message || "Unknown error occurred." };
  }
};
