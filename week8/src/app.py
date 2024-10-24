import streamlit as st
from bot import graph

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Ollama")

if "messages" not in st.session_state:
    st.session_state["config"] = {"configurable": {"thread_id": "1"}}
    st.session_state["messages"] = [{"role": "S", "content": "You are a helpful assistant"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    for event in graph.stream({"messages": [("user", prompt)]}, config=st.session_state['config']):
        for value in event.values():
            for last_message in value["messages"]:
                if last_message.type == "ai":
                    if last_message.tool_calls:
                        st.session_state.messages.append({"role": "system", "content": f"Tool call: {last_message.tool_calls}"})
                        st.chat_message("C").write(f"Tool call: {last_message.tool_calls}")
                    else:
                        st.session_state.messages.append({"role": "assistant", "content": last_message.content})
                        st.chat_message("assistant").write(last_message.content)
                    break
                elif last_message.type == "tool":
                    st.session_state.messages.append({"role": "system", "content": f"Tool response: {last_message.content}"})
                    st.chat_message("T").write(f"Tool response: {last_message.content}")
                    break
