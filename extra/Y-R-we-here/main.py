from langchain_ollama import ChatOllama
from langchain_core.messages.ai import AIMessage

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
    base_url="http://ollama:11434"
    # other params...
)

with open("ideas.txt", "r") as file:
    ideas = file.read()

messages = [
    (
        "system",
        """You are a writing assistant AI. The user will provide a short outline of an essay.
Expand each concept in the sentence and generate an essay that is 500 words long.
        """,
    ),
    ("human", ideas),
]
ai_msg: AIMessage = llm.invoke(messages)
print(ai_msg)

with open("essay.txt", "w") as file:
    file.write(ai_msg.content)