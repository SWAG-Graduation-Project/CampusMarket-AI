from fastapi import APIRouter, UploadFile, Depends

from app.core.dependencies import validate_images
from app.schemas.product_analysis import ProductAnalysisResponse

router = APIRouter()


@router.post("/analyze-product", response_model=ProductAnalysisResponse)
async def analyze_product(
    files: list[UploadFile] = Depends(validate_images),
):
    """상품 이미지 분석 후 카테고리, 상품명, 색상, 상태, 설명 반환 (최대 5장)"""
    # TODO: call product_analysis_service
    raise NotImplementedError
