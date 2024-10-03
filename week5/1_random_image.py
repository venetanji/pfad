from PIL import Image
import numpy as np

img_dimensions = {
    "low": 0,
    "high": 256,
    "size": (512, 512, 3),
    "dtype": np.uint8
}

data = np.random.randint(**img_dimensions)
img = Image.fromarray(data, 'RGB')
img.show()