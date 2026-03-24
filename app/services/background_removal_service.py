import base64
import io

from PIL import Image
from rembg import new_session, remove

_MAX_SIDE = 1024  # 리사이즈 기준 긴 변 최대 픽셀
_WEBP_QUALITY = 85

_session = new_session()  # 모델 최초 로드 후 재사용


def _resize(img: Image.Image) -> Image.Image:
    """긴 변이 _MAX_SIDE를 초과하면 비율 유지하며 축소"""
    w, h = img.size
    if max(w, h) <= _MAX_SIDE:
        return img
    scale = _MAX_SIDE / max(w, h)
    return img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)


async def remove_backgrounds(image_data: list[tuple[bytes, str]]) -> list[str]:
    """각 이미지에서 배경 제거 후 base64 WebP 목록 반환"""
    results_b64: list[str] = []

    for image_bytes, _ in image_data:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = _resize(img)

        # 배경 제거 (PIL Image 반환)
        result_img = remove(img, session=_session).convert("RGBA")
        buf = io.BytesIO()
        result_img.save(buf, format="WEBP", quality=_WEBP_QUALITY)

        results_b64.append(base64.b64encode(buf.getvalue()).decode())

    return results_b64
