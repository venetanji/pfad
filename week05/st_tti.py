import streamlit as st
from diffusers import DiffusionPipeline
import torch

if "pipeline" not in st.session_state:
    model = "runwayml/stable-diffusion-v1-5"
    st.session_state["pipeline"] = DiffusionPipeline.from_pretrained(model, torch_dtype=torch.float16)
    # change to mps if on Mac with Apple Silicon
    st.session_state["pipeline"].to("cuda" if torch.cuda.is_available() else "cpu")

if prompt := st.text_input("Prompt"):
    with st.spinner("Generating..."):
        img = st.session_state["pipeline"](prompt)
        st.image(img[0], use_container_width=True)