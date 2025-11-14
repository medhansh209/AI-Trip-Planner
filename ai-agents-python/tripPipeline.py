from agents import research_agent, OptimizerAgent, GeneratorAgent

def plan_trip_pipeline(user_input: dict, use_llm: bool = False, openai_api_key: str = None) -> dict:
    """
    Master pipeline for AI Trip Planner
    """

    try:
        print(" Step 1: Running Research Agent...")
        research_results = research_agent(user_input)
        print(" Research Agent output keys:", list(research_results.keys()) if research_results else "None")

        if not research_results:
            return {
                "error": "Research Agent returned no data",
                "research_results": {},
                "optimized_results": {},
                "final_itinerary": {}
            }

        print("\n Step 2: Running Optimizer Agent...")
        optimizer = OptimizerAgent()
        optimized_results = optimizer.optimize_itinerary(research_results)
        print(" Optimizer output keys:", list(optimized_results.keys()) if optimized_results else "None")
        print(optimized_results)

        if not optimized_results or not optimized_results.get("optimized_plan"):
            return {
                "error": "Optimizer Agent failed",
                "research_results": research_results,
                "optimized_results": {},
                "final_itinerary": {}
            }

        print("\n Step 3: Running Generator Agent...")
        generator = GeneratorAgent(use_llm=use_llm, openai_api_key=openai_api_key)
        final_output = generator.generate_itinerary(optimized_results)
        print(" Generator output keys:", list(final_output.keys()) if final_output else "None")
        print(final_output)

        if not final_output:
            return {
                "error": "Generator Agent failed",
                "research_results": research_results,
                "optimized_results": optimized_results,
                "final_itinerary": {}
            }

        print("\n Trip planning pipeline completed successfully!")

        return {
            "input": user_input,
            "research_results": research_results,
            "optimized_results": optimized_results,
            "final_itinerary": final_output
        }

    except Exception as e:
        print(f" Pipeline crashed: {e}")
        return {
            "error": str(e),
            "research_results": {},
            "optimized_results": {},
            "final_itinerary": {}
        }
