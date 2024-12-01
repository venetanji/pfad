from diffusers import DiffusionPipeline
import torch

model = "runwayml/stable-diffusion-v1-5"

pipe = DiffusionPipeline.from_pretrained(model)
pipe.to("cpu")

while True:
    prompt = input("Type a prompt and press enter to generate an image:\n>>> ")
    images = pipe(prompt, num_inference_steps=20).images
    images[0].show()
