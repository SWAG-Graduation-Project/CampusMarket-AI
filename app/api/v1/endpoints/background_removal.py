from fastapi import APIRouter, File, UploadFile

from app.core.dependencies import validate_images
from app.schemas.background_removal import BackgroundRemovalResponse

router = APIRouter()


@router.post("/remove-background", response_model=BackgroundRemovalResponse, summary="상품 이미지 배경 제거")
async def remove_background(
    files: list[UploadFile] = File(...),
):
    """배경 제거 후 투명 PNG 반환 (최대 5장)"""
    await validate_images(files)
    # TODO: call background_removal_service
    raise NotImplementedError
