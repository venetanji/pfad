from qdrant_store import vectorstore
from langchain_classic.tools.retriever import create_retriever_tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_from_student_handbook",
    "Retrieve information from the official polyu student handbook",
)

tools = [retriever_tool]
llm = ChatOpenAI(model="qwen/qwen3-4b-2507", base_url="http://localhost:1234/v1", api_key="ollama")
graph = create_agent(llm, tools=tools)
config = {"configurable": {"thread_id": "1"}}

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