
import json
import re
from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

from tools import search_places, find_attraction

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3
)


class HolidayState(TypedDict):
    destination: str
    interests: str
    days: int
    budget: str
    travel_style: str
    location: str
    attractions: list[dict]
    itinerary: str
    is_valid: bool
    retry_count: int


def research_places(state: HolidayState):
    destination = state["destination"]

    try:
        locations = search_places(destination)

        if not locations:
            print("Destination lookup returned no results.")
            return {"location": "", "attractions": []}

        location = locations[0]

        attractions = find_attraction(
            float(location["longitude"]),
            float(location["latitude"])
        )

        if attractions is None:
            attractions = []

        print(f"Destination researched: {destination}")
        print(f"Retrieved attractions: {len(attractions)}")

        return {
            "location": location["name"],
            "attractions": attractions
        }

    except Exception as error:
        print(f"Research failed: {error}")
        return {"location": "", "attractions": []}


def travel_planner(state: HolidayState):
    attractions = state["attractions"]

    if attractions:
        places_context = json.dumps(
            attractions,
            ensure_ascii=False,
            indent=2
        )
    else:
        places_context = (
            "No verified attractions were retrieved. "
            "Suggest suitable places, but do not claim "
            "they were verified by the research tool."
        )

    budget = state.get("budget", "Moderate")
    travel_style = state.get("travel_style", "Balanced")

    prompt = f"""
    You are a professional travel planner.

    Create an itinerary for EXACTLY {state['days']} days
    in {state['destination']}.

    User interests: {state['interests']}
    Budget preference: {budget}
    Travel style: {travel_style}

    Research results:
    {places_context}

    Requirements:
    1. Include exactly {state['days']} days.
    2. Use headings exactly like ## Day 1, ## Day 2, etc.
    3. Include morning, afternoon, and evening activities every day.
    4. Include food recommendations every day.
    5. Prioritize researched attractions when relevant.
    6. Do not claim opening hours have been verified.
    7. Avoid unnecessary repetition.
    8. Tailor recommendations to a {budget} budget.
    9. Pace activities for a {travel_style} travel style.
    10. Return Markdown.
    """

    response = model.invoke(prompt)
    return {"itinerary": response.content}


def validate_itinerary(state: HolidayState):
    itinerary = state["itinerary"]

    day_numbers = re.findall(
        r"(?im)^\s{0,3}#{1,6}\s+\**Day\s+(\d+)\b",
        itinerary
    )

    unique_days = set(day_numbers)
    expected_days = state["days"]

    is_valid = (
        len(day_numbers) == expected_days
        and len(unique_days) == expected_days
        and unique_days == {
            str(i) for i in range(1, expected_days + 1)
        }
    )

    print(f"Expected days: {expected_days}")
    print(f"Detected days: {sorted(unique_days)}")
    print(f"Valid itinerary: {is_valid}")

    return {"is_valid": is_valid}


def retry_planner(state: HolidayState):
    return {"retry_count": state["retry_count"] + 1}


def route_after_validation(state: HolidayState):
    if state["is_valid"]:
        return "finish"

    if state["retry_count"] < 2:
        return "retry"

    print("Maximum retries reached.")
    return "finish"


graph_builder = StateGraph(HolidayState)

graph_builder.add_node("research_places", research_places)
graph_builder.add_node("travel_planner", travel_planner)
graph_builder.add_node("validate_itinerary", validate_itinerary)
graph_builder.add_node("retry_planner", retry_planner)

graph_builder.add_edge(START, "research_places")
graph_builder.add_edge("research_places", "travel_planner")
graph_builder.add_edge("travel_planner", "validate_itinerary")

graph_builder.add_conditional_edges(
    "validate_itinerary",
    route_after_validation,
    {
        "retry": "retry_planner",
        "finish": END
    }
)

graph_builder.add_edge("retry_planner", "travel_planner")

graph = graph_builder.compile()


def plan_holiday(
    destination: str,
    interests: str,
    days: int,
    budget: str = "Moderate",
    travel_style: str = "Balanced",
) -> dict:
    """Invoke the LangGraph workflow and return the final state dict.

    Parameters
    ----------
    destination : str
        City or region the user wants to visit.
    interests : str
        Comma-separated interests (e.g. "food, nature, history").
    days : int
        Number of trip days (1–30).
    budget : str
        One of "Budget-friendly", "Moderate", or "Luxury".
    travel_style : str
        One of "Relaxed", "Balanced", or "Packed".

    Returns
    -------
    dict
        The final HolidayState produced by the graph.
    """
    initial_state: HolidayState = {
        "destination": destination,
        "interests": interests or "Local culture and sightseeing",
        "days": days,
        "budget": budget,
        "travel_style": travel_style,
        "location": "",
        "attractions": [],
        "itinerary": "",
        "is_valid": False,
        "retry_count": 0,
    }

    result = graph.invoke(initial_state)
    return result


if __name__ == "__main__":
    destination = input("Enter your destination: ").strip()
    interests = input(
        "Enter your interests (e.g., anime, food, nature): "
    ).strip()

    while True:
        try:
            days = int(input("How many days is your trip? "))

            if days < 1 or days > 30:
                print("Please enter a duration between 1 and 30 days.")
                continue

            break
        except ValueError:
            print("Please enter a valid whole number.")

    result = plan_holiday(destination, interests, days)

    print("\n" + "=" * 50)
    print("YOUR PERSONALIZED HOLIDAY ITINERARY")
    print("=" * 50)
    print(result["itinerary"])
