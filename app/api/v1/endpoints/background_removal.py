from fastapi import APIRouter, UploadFile, Depends

from app.core.dependencies import validate_images
from app.schemas.background_removal import BackgroundRemovalResponse

router = APIRouter()


@router.post("/remove-background", response_model=BackgroundRemovalResponse)
async def remove_background(
    files: list[UploadFile] = Depends(validate_images),
):
    """배경 제거 후 투명 PNG 반환 (최대 5장)"""
    # TODO: call background_removal_service
    raise NotImplementedError
