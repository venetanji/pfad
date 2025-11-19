import asyncio
import streamlit as st
from bot import graph

# Initialize session state for chatbot
if "messages" not in st.session_state:
    st.session_state["config"] = {"configurable": {"thread_id": "1"}}
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

def chatbot():
    st.title("💬 Chatbot")
    st.caption("🚀 A Streamlit chatbot with an mcp tool for image generation")

    # Display chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        async def run_agent(prompt_text: str):
            responses = []
            async for event in graph.astream({"messages": st.session_state.messages}, config=st.session_state["config"]):
                handled = False
                for value in event.values():
                    for last_message in value["messages"]:
                        responses.append(last_message)
                        handled = True
                        break
                    if handled:
                        break
            return responses

        agent_messages = asyncio.run(run_agent(prompt))

        for last_message in agent_messages:
            if last_message.type == "ai":
                if last_message.tool_calls:
                    st.session_state.messages.append({"role": "system", "content": f"Tool call: {last_message.tool_calls}"})
                    st.chat_message("assistant").text(f"🔧 Tool call: {last_message.tool_calls}")
                else:
                    st.session_state.messages.append({"role": "assistant", "content": last_message.content})
                    st.chat_message("assistant").write(last_message.content)
            elif last_message.type == "tool":
                st.session_state.messages.append({"role": "system", "content": f"Tool response: {last_message.content}"})
                st.chat_message("assistant").text(f"⚙️ Tool response: {last_message.content}")
    
chatbot_page = st.Page(chatbot, title="💬 Chatbot")
pg = st.navigation([chatbot_page])
pg.run()