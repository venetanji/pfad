import torch
import numpy as np
from diffusers import AudioLDM2Pipeline, DPMSolverMultistepScheduler
import pyaudio
import speech_recognition as sr
import streamlit as st

# Initialize streamlit app
st.title("A Music Generatorヽ(o´∀`)ﾉ♪♬ ")
st.write("ヾ(´〇`)ﾉ♪♪♪! Describe your mood to generate a little song, or press the button to record your voice")

# loading AudioLDM2 model
pipeline = AudioLDM2Pipeline.from_pretrained(
    "cvssp/audioldm2-music", torch_dtype=torch.float32  # use float32 instead of float16 for CPU
)
pipeline.to("cpu")  # execute in CPU

# deploy the scheduler（调度器）
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
    pipeline.scheduler.config
)

# initialize PyAudio 用于播放生成的音频 use for play the generated audio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=16000, output=True)  # 单声道

# 初始化语音识别 initialize speech recognition
recognizer = sr.Recognizer()

# Text input or voice input selector
input_method = st.radio("Choose input method pls(╭☞•́⍛•̀)╭☞:", ('Text', 'Microphone'))

if input_method == 'Text':
    prompt = st.text_input("Enter your song description:")
    if st.button("Generate Audio"):
        if prompt:
            st.write(f"Generating audio for: {prompt}")
            audios = pipeline(prompt, num_inference_steps=50, audio_length_in_s=10).audios

            # Play the generated audio
            for audio in audios:
                stream.write(audio.astype(np.float32))
            st.write("Audio generated and played successfully!")
        else:
            st.write("Please enter a prompt.")

else:
    st.write("Press 'Record' to use microphone input.")
    if st.button("Record"):
        with sr.Microphone() as source:
            st.write("Listening...")
            audio_input = recognizer.listen(source)
            try:
                prompt = recognizer.recognize_google(audio_input)
                st.write(f"You said: {prompt}")
                if prompt.lower() != "bye":
                    # generate audio
                    audios = pipeline(prompt, num_inference_steps=50, audio_length_in_s=10).audios

                    # Play the generated audio
                    for audio in audios:
                        stream.write(audio.astype(np.float32))
                    st.write("Audio generated and played successfully!")
            except sr.UnknownValueError:
                st.write("Sorry, I did not understand that. Please try again.")
                
# Final cleanup
def cleanup():
    stream.stop_stream()
    stream.close()
    p.terminate()