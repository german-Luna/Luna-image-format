from PIL import Image
from LIF import LIF

# Example: Create a sample PIL image
sample_image = Image.open("luna.jpg")

# Example: Save the PIL image using LIF format
lif_instance = LIF()
lif_instance.from_pil_image(sample_image)
lif_instance.write('example.lif')

# Example: Open the saved LIF file, convert to PIL image, and display
opened_lif = LIF()
opened_lif.open('example.lif')
reconstructed_image = opened_lif.to_pil_image()
reconstructed_image.show()
