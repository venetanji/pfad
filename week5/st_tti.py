import streamlit as st
from diffusers import DiffusionPipeline
import torch

if "pipeline" not in st.session_state:
    model = "runwayml/stable-diffusion-v1-5"
    st.session_state["pipeline"] = DiffusionPipeline.from_pretrained(model, torch_dtype=torch.float16)
    st.session_state["pipeline"].to("cuda")

if prompt := st.text_input("Prompt"):
    with st.spinner("Generating..."):
        img = st.session_state["pipeline"](prompt)
        st.image(img[0], use_column_width=True)