
import torch
import numpy as np
from diffusers import AudioLDM2Pipeline, DPMSolverMultistepScheduler
import pyaudio

pipeline = AudioLDM2Pipeline.from_pretrained(
    "cvssp/audioldm2-music", torch_dtype=torch.float16
)
pipeline.to("cuda")
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
    pipeline.scheduler.config
)
pipeline.enable_model_cpu_offload()

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=16000, output=True)

while True:
    prompt = input("Give me a song description: ")
    audios = pipeline(prompt, 
            num_inference_steps=200,
            audio_length_in_s=60
        ).audios
    for audio in audios:
        stream.write(audio.astype(np.float32))
