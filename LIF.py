import gzip
import json
from PIL import Image

class LIF:
    def _compress(self):
        self.image_data = gzip.compress(self.image_data)

    def _uncompress(self):
        try:
            self.image_data = gzip.decompress(self.image_data)
        except Exception as e:
            raise ValueError(f"Error decompressing data: {e}")

    def _read_image_data(self):
        try:
            self.image_data = json.loads(self.image_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON data: {e}")

    def _to_json(self):
        try:
            self.image_data = json.dumps(self.image_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error encoding to JSON: {e}")

    def open(self, path):
        try:
            self.image_data = open(path, 'rb').read()
            self._uncompress()
            self._read_image_data()

            self.meta_data = self.image_data.get('meta_data', {})
            self.pixel_data = self.image_data.get('pixels', {})

            if not isinstance(self.meta_data, dict) or not isinstance(self.pixel_data, dict):
                raise ValueError("Invalid data format")

        except Exception as e:
            raise ValueError(f"Error opening LIF file: {e}")

    def write(self, path):
        try:
            self.image_data = dict()

            self.image_data['meta_data'] = self.meta_data
            self._to_json()
            self.image_data = bytes(self.image_data)
            self._compress()

            open(path, "wb").write(self.image_data)

        except Exception as e:
            raise ValueError(f"Error writing LIF file: {e}")

        finally:
            del self.image_data
            del self.meta_data
            del self.pixel_data

    def from_pil_image(self, image: Image):
        try:
            pix = image.load()

            self.meta_data = dict()
            self.pixel_data = dict()

            width, height = image.size

            self.meta_data["size"] = (width, height)

            for x in range(width):
                current_row = self.pixel_data.get(str(x), [])
                for y in range(height):
                    rgba_value = pix[x, y][:3]
                    current_row.append(rgba_value)

        except Exception as e:
            raise ValueError(f"Error converting PIL image to LIF: {e}")

    def to_pil_image(self):
        try:
            width, height = self.meta_data.get("size", (0, 0))
            if width == 0 or height == 0:
                raise ValueError("Invalid image size in metadata")

            # Create a new PIL image with the specified size
            result_image = Image.new("RGB", (width, height))
            result_pixels = result_image.load()

            # Iterate through pixel data and set values in the new image
            for x in range(width):
                current_row = self.pixel_data.get(str(x), [])
                for y, rgba_value in enumerate(current_row):
                    result_pixels[x, y] = tuple(rgba_value) + (255,)

            return result_image

        except Exception as e:
            raise ValueError(f"Error converting LIF to PIL image: {e}")
