
import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3
)

class HolidayState(TypedDict):
    destination:str
    interests:str
    days:int
    itinerary: str
    is_valid:bool
    retry_count:int
    
def travel_planner(state:HolidayState):
    prompt = f"""
    Plan a {state['days']}-day trip to {state['destination']}.

    User interests: {state['interests']}

    Create a day-by-day itinerary with:
    - Morning activities
    - Afternoon activities
    - Evening activities
    - Food recommendations
    """
    
    response=model.invoke(prompt)
    
    return {"itinerary": response.content}

def validate_itinerary(state:HolidayState):
    itinerary=state["itinerary"]
    
    day_numbers = re.findall(
        r"(?im)^\s{0,3}#{1,6}\s*(?:\*\*)?Day\s+(\d+)\b",
        itinerary
    )
    
    unique_days=set(day_numbers)
    expected_days=state["days"]
    
    is_valid=(
        len(day_numbers)==expected_days
        and len(unique_days)==expected_days
        and unique_days == {str(i) for i in range(1, expected_days + 1)}
    )
    
    print(f"Expected days: {expected_days}")
    print(f"Detected days: {sorted(unique_days)}")
    print(f"Valid itinerary: {is_valid}")

    return {"is_valid": is_valid}
    
    
    
graph_builder=StateGraph(HolidayState)

graph_builder.add_node("travel_planner",travel_planner)
graph_builder.add_node("validate_itinerary",validate_itinerary)

graph_builder.add_edge(START, "travel_planner")

graph_builder.add_edge("travel_planner", "validate_itinerary")


def route_after_validation(state:HolidayState):
    if state["is_valid"]:return END
    return "travel_planner"

graph_builder.add_conditional_edges(
    "validate_itinerary",
    route_after_validation
)

graph=graph_builder.compile()

initial_state = {
    "destination": "Tokyo",
    "interests": "Anime, Japanese food, and local culture",
    "days": 7,
    "itinerary": "",
    "is_valid": False,
    "retry_count": 0
}


result=graph.invoke(initial_state)

print(result["itinerary"])

