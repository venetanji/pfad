import streamlit as st

if prompt := st.chat_input():

    st.chat_message("user").write(prompt)