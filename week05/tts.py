import streamlit as st
from st_audiorec import st_audiorec
import torch
import uuid
import requests


device = "cuda" if torch.cuda.is_available() else "cpu"

if text := st.text_input("Enter text to convert to speech", "Hello, how are you?"):
    tmp_file = f'samples/tmp{uuid.uuid1()}.wav'
    response = requests.post(
        f"http://localhost:8000/tts",
        params={"text": text},
        stream=True,
    )

    with open(tmp_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    st.audio(tmp_file, format='audio/wav')
