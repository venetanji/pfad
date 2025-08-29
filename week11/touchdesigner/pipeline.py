
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, LCMScheduler, AutoencoderTiny
import torch

class NdiPipeline:
    def __init__(self, 
                 width=512, 
                 height=512, 
                 seed=1231412, 
                 device="cuda", 
                 torch_dtype=torch.float16, 
                 model="lykon/dreamshaper-8-lcm",
                 controlnet="lllyasviel/sd-controlnet-canny",
                 vae="madebyollin/taesd",
                 guidance_scale=1.2,
                 prompt="cg, pixar, animation, 3d, character, design, concept, art, illustration, drawing, painting, digital"
    ):
        self.controlnet = ControlNetModel.from_pretrained(controlnet, torch_dtype=torch_dtype)
        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            model, controlnet=self.controlnet, torch_dtype=torch_dtype, safety_checker = None
        )
        pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
        pipe.vae = AutoencoderTiny.from_pretrained(vae).to(device=device, dtype=torch_dtype)
        #pipe.enable_model_cpu_offload()
        pipe.to(device)
        pipe.unet.to(memory_format=torch.channels_last)
        self.pipe = pipe

        self.guidance_scale = guidance_scale
        self.width = width
        self.height = height
        self.seed = seed
        self.prompt = prompt
    
    def generate(self, image):
        generator = torch.manual_seed(0)
        self.pipe(self.prompt,
                    num_inference_steps=4, 
                    generator=generator, 
                    image=image,
                    guidance_scale=self.guidance_scale).images[0]