import io

from PIL import Image


def bytes_to_pil(image_bytes: bytes) -> Image.Image:
    return Image.open(io.BytesIO(image_bytes))


def bytes_list_to_pil(images_bytes: list[bytes]) -> list[Image.Image]:
    return [bytes_to_pil(b) for b in images_bytes]
