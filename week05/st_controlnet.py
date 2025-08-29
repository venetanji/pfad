import streamlit as st
import numpy as np
import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler


import cv2
from PIL import Image

if "pipeline" not in st.session_state:
    controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16
    )

    # speed up diffusion process with faster scheduler and memory optimization
    pipe.enable_model_cpu_offload()
    st.session_state["pipeline"] = pipe

def do_canny(image):
    image = np.array(image)
    # get canny image
    image = cv2.Canny(image, 100, 200)
    image = image[:, :, None]
    image = np.concatenate([image, image, image], axis=2)
    canny_image = Image.fromarray(image)

    return canny_image

if uploaded_file := st.file_uploader("Choose a file"):
    uploaded_file = Image.open(uploaded_file)
    canny_image = do_canny(uploaded_file)
    st.image(canny_image, use_column_width=True)
    if prompt := st.text_input("Prompt"):
        with st.spinner("Generating..."):
            image = st.session_state["pipeline"](prompt, image=canny_image, num_inference_steps=20).images[0]
            st.image(image, use_column_width=True)





