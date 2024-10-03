import streamlit as st

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    msg = "I'm sorry, I don't understand. Can you rephrase that?"

    st.chat_message("assistant").write(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    