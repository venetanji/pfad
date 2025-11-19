import asyncio

from tools import tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    # change model according to your setup
    model="qwen/qwen3-4b-2507", 
    # change port to 1234 for LMStudio
    base_url="http://localhost:1234/v1",
    # api key only needed for remote servers,
    # otherwise ignored by local setups
    api_key="doesnotmatter"
)

# create the agent with tools
graph = create_agent(llm, tools=tools)
config = {"configurable": {"thread_id": "1"}}

# simple REPL to interact with the agent
# run python bot.py in terminal to start
# press Ctrl+C to exit
# Note: this is not executed when the file is imported by app.py
if __name__ == "__main__":
    async def stream_graph_updates(user_input: str):
        async for event in graph.astream({"messages": ("user", user_input)}, config=config):
            for value in event.values():
                for last_message in value["messages"]:
                    if last_message.type == "ai":
                        if last_message.tool_calls:
                            print("  --- Tool call:", last_message.tool_calls)
                        else:
                            print("Assistant:", last_message.content)
                    elif last_message.type == "tool":
                        print("  --- Tool response:", last_message.content)

    async def repl():
        while True:
            try:
                user_input = await asyncio.to_thread(input, "User: ")
                await stream_graph_updates(user_input)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break
            except Exception as e:
                print(e)
                break

    asyncio.run(repl())