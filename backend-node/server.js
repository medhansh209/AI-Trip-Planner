// import express from "express";
// import dotenv from "dotenv";
// import cors from "cors";
// import planRoute from "./routes/planRoute.js";


// dotenv.config();
// const app = express();
// app.use(cors());
// app.use(express.static("public"));

// app.set("view engine", "ejs");
// app.use(express.json());

// // ✅ Serve static files (like test.html)
// app.use(express.static("public"));

// app.get("/", async (req, res) => {
//     try {
//         // Pull trips from your database (or make a dummy array to test)
//         const trips = await Trip.find();  // ← replace with your model
    
//         res.render("index", { trips });   // ← VERY IMPORTANT
//     } catch (err) {
//         console.error(err);
//         res.render("index", { trips: [] });
//     }
// });


// // API routes
// app.use("/plan-trip", planRoute);

// const PORT = process.env.PORT || 8000;
// app.listen(PORT, () => console.log(`🚀 Node backend running on port ${PORT}`));


import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import planRoute from "./routes/planRoute.js";

dotenv.config();

const app = express();

// ---------------------------
// Middleware
// ---------------------------
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));   // ← VERY IMPORTANT
app.use(express.static("public"));                 // Serve /public folder

// ---------------------------
// View Engine
// ---------------------------
app.set("view engine", "ejs");

// ---------------------------
// HOME PAGE (renders index.ejs)
// ---------------------------
app.get("/", (req, res) => {
    res.render("index");     // No DB, no Trip model, no errors
});

// ---------------------------
// TRIP PLANNER ROUTE
// ---------------------------
app.use("/plan-trip", planRoute);

// ---------------------------
// START SERVER
// ---------------------------
const PORT = process.env.PORT || 8000;
app.listen(PORT, () => console.log(`🚀 Node backend running on port ${PORT}`));
