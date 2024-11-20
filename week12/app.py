import streamlit as st
from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper
from langchain_ollama import ChatOllama
from pathlib import Path
import pymupdf4llm
import uuid

import asyncio
import json

basefolder = Path(__file__).parent
comfyui_flows = basefolder / "workflows"
docs = basefolder / "documents"

if "comfy_api" not in st.session_state:
    st.session_state.comfy_api = ComfyApiWrapper("http://127.0.0.1:8188/")

if "ollama" not in st.session_state:
    st.session_state.ollama = ChatOllama(model="llama3.2")
    st.session_state.ollama_json = ChatOllama(model="llama3.2",format="json")

def comfyui():
    st.title("ComfyUI")
    st.write("Welcome to ComfyUI! A simple UI library for Streamlit.")

    workflows = [wf.name for wf in comfyui_flows.glob("*.json")]
    
    if selected_workflow := st.selectbox("Select a workflow", workflows):
        wf = ComfyWorkflowWrapper(comfyui_flows / selected_workflow)

    batch_size = st.slider("Batch Size", 1, 10, 2)

    if prompt := st.text_input("Prompt"):       
        wf.set_node_param("Empty Latent Image", "batch_size", batch_size)
        wf.set_node_param("positive", "text", prompt)
        
        get_image = st.session_state.comfy_api.queue_and_wait_images(wf, "Save Image")

        # queue your workflow for completion
        results = asyncio.run(get_image)
        for filename, image_data in results.items():
            st.image(image_data, caption=filename)

def structured_output():
    st.title("Structured Output")
    if pdf_file := st.file_uploader("Upload a PDF file", type=["pdf"]):
        filename = f"{uuid.uuid4()}.pdf"
        with open(docs / filename, "wb") as f:
            f.write(pdf_file.getvalue())

        md_text = pymupdf4llm.to_markdown(docs / filename)
        json_mode = st.checkbox("JSON Mode")
        
        if prompt := st.chat_input("Ask me stuff!"):
            prompt = f"{md_text}\n{prompt}"
            if json_mode:
                response = st.session_state.ollama_json.invoke(prompt)
                try:
                    response = json.loads(response.content)
                    st.write(response)
                except:
                    st.write(response)
            else:
                response = st.session_state.ollama.invoke(prompt)
                st.write(response.content)
    
comfyui_page = st.Page(comfyui, title="ComfyUI")
structured_output_page = st.Page(structured_output, title="Structured Output")
pg = st.navigation([comfyui_page, structured_output_page])
pg.run()