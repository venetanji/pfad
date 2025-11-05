from qdrant_store import vectorstore
from langchain_classic.tools.retriever import create_retriever_tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
        # change model according to your setup
        model="qwen3:8b",
        # change port to 1234 for LMStudio
        base_url="http://localhost:11434/v1",
         # api key only needed for remote servers,
        # otherwise ignored by local setups
        api_key="ollama"
    )

# k is the number of relevant documents to retrieve, set to 2
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# the tool provided to the agent to search the student handbook
retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_from_student_handbook",
    "Retrieve information from the official polyu student handbook",
)

# tools need to be a list
tools = [retriever_tool]

# create the agent
graph = create_agent(llm, tools=tools)
config = {"configurable": {"thread_id": "1"}}


# simple REPL to interact with the agent
# run python pdf_bot.py in terminal to start
# press Ctrl+C to exit
# Note: this is not executed when the file is imported by handbook_app.py
if __name__ == "__main__":
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