import os
import base64
from PIL import Image
import io

DEFAULT_IMAGES = {
    "Black garbage": "garbagebag.jpg",
    "Green bin": "compost.jpg",
    "Light blue box": "lightblue.jpg",
    "Dark blue box": "darkblue.jpg",
}

BIN_FILENAMES = {
    "Black garbage": "garbagebag.jpg",
    "Green bin": "compost.jpg",
    "Light blue box": "lightblue.jpg",
    "Dark blue box": "darkblue.jpg",
}

def load_image_as_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception:
        # If file not found or can't open, return a transparent pixel (or any small default)
        # This is a 1x1 px transparent PNG
        transparent_pixel = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQ"
            "ImWNgYAAAAAMAASsJTYQAAAAAElFTkSuQmCC"
        )
        return transparent_pixel

def get_bin_image_base64(bin_type, user_id):
    user_path = os.path.join("user_images", user_id, BIN_FILENAMES[bin_type])
    if os.path.exists(user_path):
        return load_image_as_base64(user_path)
    elif os.path.exists(DEFAULT_IMAGES[bin_type]):
        return load_image_as_base64(DEFAULT_IMAGES[bin_type])
    else:
        # If neither exist, return placeholder
        return load_image_as_base64(None)
    
def get_all_bin_images(user_id):
    return {k: get_bin_image_base64(k, user_id) for k in DEFAULT_IMAGES.keys()}


def fixed_size_image(b64_string, size=(200, 200)):
    image_data = base64.b64decode(b64_string)
    image = Image.open(io.BytesIO(image_data))
    image = image.convert("RGB")         # Always use RGB to avoid errors
    image = image.resize(size, Image.LANCZOS)  # Resize to exact size (e.g., 200x200)
    output = io.BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()
