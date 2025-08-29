import streamlit as st
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Ollama")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=st.session_state.messages,
        stream=True,
    )

    msg = ""

    def stream_response():
        global msg
        for chunk in response:
            print(chunk)
            part = chunk.choices[0].delta.content
            if part:
                msg += part
                yield part

    
    st.chat_message("assistant").write_stream(stream_response)
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
