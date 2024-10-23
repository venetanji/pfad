import cv2
import numpy as np
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, LCMScheduler, AutoencoderTiny
import torch
from PIL import Image

controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "lykon/dreamshaper-8-lcm", controlnet=controlnet, torch_dtype=torch.float16, safety_checker = None
)
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.vae = AutoencoderTiny.from_pretrained("madebyollin/taesd").to(device="cuda", dtype=torch.float16)
pipe.to("cuda")
pipe.unet.to(memory_format=torch.channels_last)
prompt = "a futuristic building on mars, cg, pixar, animation, 3d, concept, art, illustration, drawing, painting, digital"

# Define the size of the window and the square
window_size = 500
square_size = 100

# Create a black image
image = np.zeros((window_size, window_size, 3), dtype=np.uint8)

# Define the center and the angle of rotation
center = (window_size // 2, window_size // 2)
angle = 0

while True:
    # Create a copy of the black image
    img_copy = image.copy()
    generator = torch.manual_seed(0)

    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Define the points of the square
    points = np.array([
        [center[0] - square_size // 2, center[1] - square_size // 2],
        [center[0] + square_size // 2, center[1] - square_size // 2],
        [center[0] + square_size // 2, center[1] + square_size // 2],
        [center[0] - square_size // 2, center[1] + square_size // 2]
    ])

    # Rotate the points
    rotated_points = cv2.transform(np.array([points]), rotation_matrix)[0]

    # Draw the square
    canny = cv2.polylines(img_copy, [np.int32(rotated_points)], isClosed=True, color=(255, 255, 255), thickness=2)
    canny = Image.fromarray(canny)
    # Show the image
    cv2.imshow('Rotating Square', img_copy)
    x_output = pipe(prompt,
                    num_inference_steps=4, 
                    generator=generator, 
                    image=canny,
                    guidance_scale=1.2).images[0]
    cv2.imshow("Image",np.array(x_output) )
    

    # Increment the angle
    angle += 1

    # Break the loop if 'q' is pressed
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the window
cv2.destroyAllWindows()