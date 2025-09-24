import streamlit as st
from st_audiorec import st_audiorec
import torch
import uuid
import requests

device = "cuda" if torch.cuda.is_available() else "cpu"

"Record your voice to clone it"
recording = st_audiorec()

"Synthesize voice"
if text := st.text_input("Enter text to convert to speech"):
    
    options = {"text": text, "language": "en"}
    
    if recording:
        voice_file = f'samples/voice-{uuid.uuid1()}.wav'
        with open(voice_file, "wb") as f:
            f.write(recording)
        options['speaker_wav'] = voice_file

    response = requests.post(
        f"http://localhost:8000/generate_audio",
        json=options,
    )

    st.audio(response.json().get("file_path"), format='audio/wav')

