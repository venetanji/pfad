import streamlit as st
import ollama


st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Ollama")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = ollama.chat(model="llama3.1", messages=st.session_state.messages, stream=True)
    msg = ""

    def stream_response():
        global msg
        for chunk in response:
            part = chunk['message']['content']
            msg += part
            yield part

    
    st.chat_message("assistant").write(stream_response)
    st.session_state.messages.append({"role": "assistant", "content": msg})
