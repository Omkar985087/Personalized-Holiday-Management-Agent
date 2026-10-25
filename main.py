
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict
load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3
)

def HolidayState(TypeDict):
    destination:str
    interests:str
    days:int
    itinerary: str
    
