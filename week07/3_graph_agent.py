from langchain_ollama import ChatOllama
from typing import Literal
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
import random

config = {"configurable": {"thread_id": "1"}}
model = ChatOllama(model="llama3.1")
weather = {}

@tool
def get_weather(query: str):
    """Call to check real-time weather in a single location."""
    # This is a placeholder, but don't tell the LLM that...
    
    if query in weather:
        return weather[query]
    
    random_temperature = f'{random.randint(10, 40)}°C'
    random_outlook = random.choice(["sunny", "cloudy", "rainy", "snowy"])

    data = {"city": query, "outlook": random_outlook, "temperature": random_temperature}
    weather[query] = data
    
    return data

tools = [get_weather]


# Define the graph
graph = create_react_agent(model, tools=tools)

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}, config=config):
        for value in event.values():
            for last_message in value["messages"]:
                if last_message.type == "ai":
                    if last_message.tool_calls:
                        print("  --- Tool call:", last_message.tool_calls)
                    else:
                        print("Assistant:", last_message.content)
                elif last_message.type == "tool":
                    print("  --- Tool response:", last_message.content)

while True:
    try:
        user_input = input("User: ")
        stream_graph_updates(user_input)
    # catch all exceptions
    except Exception as e:
        print(e)
        break