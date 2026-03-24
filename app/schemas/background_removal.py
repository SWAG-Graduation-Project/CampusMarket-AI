from pydantic import BaseModel


class BackgroundRemovalResponse(BaseModel):
    """누끼 따기 - base64 인코딩된 PNG 이미지 목록"""
    images: list[str]  # base64-encoded PNG (transparent background)
    count: int
