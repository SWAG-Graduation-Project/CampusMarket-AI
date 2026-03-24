from fastapi import APIRouter, File, UploadFile

from app.core.dependencies import validate_images
from app.schemas.background_removal import BackgroundRemovalResponse
from app.services.background_removal_service import remove_backgrounds

router = APIRouter()


@router.post("/remove-background", response_model=BackgroundRemovalResponse, summary="상품 이미지 배경 제거")
async def remove_background_endpoint(
    files: list[UploadFile] = File(...),
):
    """배경 제거 후 투명 PNG 반환 (최대 5장)"""
    await validate_images(files)
    image_data = [(await f.read(), f.content_type) for f in files]
    images = await remove_backgrounds(image_data)
    return BackgroundRemovalResponse(images=images, count=len(images))
