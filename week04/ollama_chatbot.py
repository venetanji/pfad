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
    
    response = ollama.chat(model="llama3.2", messages=st.session_state.messages)


    msg = response['message']['content']
    st.chat_message("assistant").write(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
