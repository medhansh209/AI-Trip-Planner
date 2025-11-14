from typing import Dict, Any
from .optimizer_agent import OptimizerAgent

# ✅ use the new, non-deprecated LangChain import
try:
    from langchain_community.chat_models import ChatOpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


class GeneratorAgent:
    """
    Generator Agent for AI Trip Planner
    -----------------------------------
    Converts optimized plan JSON into a human-readable itinerary.
    Optionally enhances output using an LLM (like GPT via LangChain).
    """

    def __init__(self, use_llm: bool = False, openai_api_key: str = None):
        self.use_llm = use_llm and LANGCHAIN_AVAILABLE
        self.openai_api_key = openai_api_key

        if self.use_llm:
            # Setup LangChain LLM (e.g., GPT-4 or GPT-3.5)
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                openai_api_key=openai_api_key
            )
            self.template = PromptTemplate(
    input_variables=["plan"],
    template=(
        "You are a senior professional travel planner. Your task is to convert the optimized "
        "itinerary JSON below into a polished, well-structured, formal travel plan.\n\n"
        
        "Here is the itinerary data to convert:\n{plan}\n\n"

        "Please follow these formatting and writing rules:\n\n"

        "---- GENERAL WRITING GUIDELINES ----\n"
        "• Use a formal, professional tone throughout.\n"
        "• Do not use emojis, icons, or decorative symbols.\n"
        "• Keep descriptions concise, clear, and informative.\n"
        "• Use standard Markdown formatting with headings, numbered lists, and bullet points.\n"
        "• Do not repeat information unnecessarily.\n\n"

        "---- STRUCTURE REQUIREMENTS ----\n"
        "The final itinerary must follow this structure exactly:\n\n"

        "1. Main Title: 'Travel Itinerary'\n\n"

        "2. Section: 'Flight Recommendation' (ONLY if flight data is available)\n"
        "   - Airline name\n"
        "   - Departure → Arrival\n"
        "   - Price\n"
        "   - Duration\n\n"

        "3. Section: 'Hotel Recommendation' (ONLY if hotel data is available)\n"
        "   - Hotel name\n"
        "   - Rating\n"
        "   - Price per night\n"
        "   - Location or distance if provided\n\n"

        "4. For each day, create a section titled: 'Day X'\n"
        "   - Begin each day with a one-sentence summary of the day's focus.\n"
        "   - Provide a numbered list of activities for that day.\n"
        "   - Each activity should include a short (2–3 line) professional description.\n"
        "   - End each day with a short closing note or practical suggestion.\n\n"

        "5. Section: 'Budget Summary'\n"
        "   - Total estimated cost from the JSON\n"
        "   - Mention what is included (activities, hotel nights if applicable)\n"
        "   - Add a brief, practical suggestion on how to stay within budget\n\n"

        "---- STYLE REQUIREMENTS ----\n"
        "• Use headings (##) for major sections.\n"
        "• Use numbered lists for activities.\n"
        "• Use bullet points only inside descriptive sections.\n"
        "• No emojis or emotional language.\n"
        "• Ensure the final document looks like a professional report.\n\n"

        "Generate the final itinerary now."
    ),
)
            self.chain = LLMChain(llm=self.llm, prompt=self.template)

    # ------------------------------------------------------------

    def generate_itinerary(self, optimized_output: Dict[str, Any]) -> Dict[str, Any]:
        """Convert optimized itinerary into readable text."""
        optimized_plan = optimized_output.get("optimized_plan", [])
        final_text = ""

        # Fallback if plan is empty
        if not optimized_plan:
            return {
                "text": "No itinerary found. Please provide valid optimized data.",
                "summary": None,
            }

        # --- Option 1: Without LLM (plain text)
        if not self.use_llm:
            lines = [" **Your Optimized Travel Itinerary**\n"]
            for day_plan in optimized_plan:
                lines.append(f"### Day {day_plan['day']}")
                lines.append(f"**Places to Visit:** {', '.join(day_plan['places'])}")
                lines.append(f" Total Time: {day_plan['total_time']} hrs")
                lines.append(f" Total Cost: ₹{day_plan['total_cost']}")
                lines.append("---")
            final_text = "\n".join(lines)
            summary = "Optimized itinerary successfully generated (text-based)."

        # --- Option 2: With LLM (narrative)
        else:
            plan_text = str(optimized_output)
            final_text = self.chain.run(plan=plan_text)
            summary = "Detailed itinerary generated using LLM."

        return {
            "text": final_text,
            "score": optimized_output.get("score", 0),
            "summary": summary,
        }

    # ------------------------------------------------------------

    def run_pipeline(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """(Optional) Run Optimizer + Generator together."""
        optimizer = OptimizerAgent()
        optimized = optimizer.optimize_itinerary(user_input)
        return self.generate_itinerary(optimized)
