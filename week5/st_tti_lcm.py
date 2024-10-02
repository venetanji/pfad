import streamlit as st
import torch
from diffusers import AutoPipelineForText2Image, LCMScheduler

if "pipeline" not in st.session_state:
    model = 'lykon/dreamshaper-8-lcm'
    pipe = AutoPipelineForText2Image.from_pretrained(model, torch_dtype=torch.float16)
    pipe.to("cuda")
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    st.session_state["pipeline"] = pipe

if "images" not in st.session_state:
    st.session_state["images"] = []


if prompt := st.text_input("Prompt"):
    with st.spinner("Generating..."):
        images = st.session_state["pipeline"](prompt, num_inference_steps=8, guidance_scale=2, num_images_per_prompt=1).images
        print(images)
        for image in images:
            st.session_state["images"].append(image)

for img in st.session_state["images"][::-1]:
    st.image(img)