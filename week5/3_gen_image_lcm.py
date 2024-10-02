from diffusers import AutoPipelineForText2Image, LCMScheduler
import torch

model = 'lykon/dreamshaper-8-lcm'
pipe = AutoPipelineForText2Image.from_pretrained(model, torch_dtype=torch.float16)
pipe.to("cuda")
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)

while True:
    prompt = input("Type a prompt and press enter to generate an image:\n>>> ")
    images = pipe(prompt, num_inference_steps=8, guidance_scale=1.5).images
    images[0].show()
