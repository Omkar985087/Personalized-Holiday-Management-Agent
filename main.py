
import os
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

graph_builder=StateGraph(HolidayState)

graph_builder.add_node("travel_planner",travel_planner)
graph_builder.add_edge(START,"travel_planner")
graph_builder.add_edge("travel_planner",END)

graph=graph_builder.compile()

initial_state={
    "destination":"Tokyo",
    "interests": "Anime, Japanese food, and local culture",
    "days":3,
    "itinerary":""
}

result=graph.invoke(initial_state)

print(result["itinerary"])

