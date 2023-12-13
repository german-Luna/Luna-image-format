from PIL import Image
import numpy as np
from LIF import LIF

# Example: Create a sample PIL image
width, height = 100, 100
sample_image = Image.fromarray(np.random.randint(0, 256, size=(width, height, 3), dtype=np.uint8))

# Example: Save the PIL image using LIF format
lif_instance = LIF()
lif_instance.from_pil_image(sample_image)
lif_instance.write('example.lif')

# Example: Open the saved LIF file, convert to PIL image, and display
opened_lif = LIF()
opened_lif.open('example.lif')
reconstructed_image = opened_lif.to_pil_image()
reconstructed_image.show()
