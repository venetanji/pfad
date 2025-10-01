from diffusers import DiffusionPipeline


import torch

model = "runwayml/stable-diffusion-v1-5"

# Load the model and move it to the GPU if available
# torch_dtype=torch.float16 is optional, but helps with performance and memory usage
# remove torch_dtype=torch.float16 if you want to run on CPU only
pipe = DiffusionPipeline.from_pretrained(model, torch_dtype=torch.float16)

# change to mps if on Mac with Apple Silicon, for example:
# device = "mps" if torch.backends.mps.is_available() else "cpu"
# pipe.to(device)
pipe.to("cuda" if torch.cuda.is_available() else "cpu")

while True:
    prompt = input("Type a prompt and press enter to generate an image:\n>>> ")
    
    # Generate the image, for options see:
    # https://huggingface.co/docs/diffusers/en/api/pipelines/stable_diffusion/text2img
    images = pipe(prompt, num_inference_steps=20).images
    
    images[0].show()
