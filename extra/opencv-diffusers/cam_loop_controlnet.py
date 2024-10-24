from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, LCMScheduler, AutoencoderTiny
import numpy as np
import torch
import cv2
from PIL import Image

# load control net and stable diffusion v1-5
controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "lykon/dreamshaper-8-lcm", controlnet=controlnet, torch_dtype=torch.float16, safety_checker = None
)
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.vae = AutoencoderTiny.from_pretrained("madebyollin/taesd").to(device="cuda", dtype=torch.float16)
#pipe.enable_model_cpu_offload()
pipe.to("cuda")
pipe.unet.to(memory_format=torch.channels_last)
# speed up diffusion process with faster scheduler and memory optimization

width = 640
height = 480
seed = 1231412
prompt = "cg, pixar, animation, 3d, character, design, concept, art, illustration, drawing, painting, digital"
negative_prompt = "realistic, portrait, photography, photo, human, face, people"

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# create a window and make it fullscreen on the second display
#cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


# Run the stream infinitely
while True:
    
    ret, frame = cap.read()
    canny = cv2.Canny(frame, 100, 200)
    canny = canny[:, :, None]
    canny = np.concatenate([canny, canny, canny], axis=2)
    cv2.imshow("frame", np.array(frame))
    canny = Image.fromarray(canny)
    generator = torch.manual_seed(0)
    print("Generating image")
    x_output = pipe(prompt,
                    num_inference_steps=4, 
                    generator=generator, 
                    image=canny,
                    guidance_scale=1.2).images[0]
    cv2.imshow("Image",np.array(x_output) )
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()