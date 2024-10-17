import torch
import numpy as np
from diffusers import AudioLDM2Pipeline, DPMSolverMultistepScheduler
import pyaudio
import speech_recognition as sr

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
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=16000, output=True) #chanels=1(单声道)

# 初始化语音识别 initialize speech recognition
recognizer = sr.Recognizer()# sr.Recognizer is the class of the speech_recognition library
#recognizer is an instance

try:
    while True:
        # capture voice input from microphone
        with sr.Microphone() as source:# use WITH to make sure the microphone will turn off when voice are already captured
            print("Hi! Please describe the song (or say 'bye' to quit): ")
            audio_input = recognizer.listen(source)

            try:# start infinit loop
                # transform voice into text
                prompt = recognizer.recognize_google(audio_input) #use Google Web Speech API
                print(f"You said: {prompt}")
                if prompt.lower() == "bye": # a way to exit the loop 
                    break
            except sr.UnknownValueError: #for dealing with failure voice recognition
                print("Sorry, I did not understand that. Please try again.")
                continue

        # generate audio (reduce the steps to generate faster in Mac)
        audios = pipeline(prompt, num_inference_steps=50, audio_length_in_s=10).audios

        # play the generated audio
        for audio in audios:
            stream.write(audio.astype(np.float32))

finally:
    # close the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()
