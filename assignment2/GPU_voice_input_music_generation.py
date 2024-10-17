import torch
import numpy as np
from diffusers import AudioLDM2Pipeline, DPMSolverMultistepScheduler
import pyaudio
import speech_recognition as sr

# loading AudioLDM2 model
pipeline = AudioLDM2Pipeline.from_pretrained(
    "cvssp/audioldm2-music", torch_dtype=torch.float16
)
pipeline.to("cuda")
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
    pipeline.scheduler.config
)
pipeline.enable_model_cpu_offload()

# initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=16000, output=True)

# initialize voice recognition
recognizer = sr.Recognizer()

try:
    while True:
        # capture voice from microphone
        with sr.Microphone() as source:
            print("Please describe the song (or say 'exit' to quit): ")
            audio_input = recognizer.listen(source)

            try:
                # transform voice into text
                prompt = recognizer.recognize_google(audio_input)
                print(f"You said: {prompt}")
                if prompt.lower() == "exit":# a way to exit the loop
                    break
            except sr.UnknownValueError:# for dealing with failure voice recognition
                print("Sorry, I did not understand that. Please try again.")
                continue

        # use LDM generate music
        audios = pipeline(prompt, num_inference_steps=100, audio_length_in_s=60).audios

        # play the generated audio
        for audio in audios:
            stream.write(audio.astype(np.float32))

finally:
    # close the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()
