from fastapi import UploadFile, HTTPException, status

from app.core.config import settings

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


async def validate_image(file: UploadFile) -> UploadFile:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"지원하지 않는 파일 형식: {file.content_type}",
        )
    return file


async def validate_images(files: list[UploadFile]) -> list[UploadFile]:
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미지를 하나 이상 업로드",
        )
    if len(files) > settings.MAX_UPLOAD_IMAGES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"이미지는 최대 {settings.MAX_UPLOAD_IMAGES}개까지 업로드 가능",
        )
    for file in files:
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"지원하지 않는 파일 형식: {file.content_type}",
            )
    return files
