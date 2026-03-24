from fastapi import APIRouter, File, UploadFile

from app.core.dependencies import validate_images
from app.schemas.product_analysis import ProductAnalysisResponse
from app.services.product_analysis_service import analyze_product

router = APIRouter()


@router.post("/analyze-product", response_model=ProductAnalysisResponse, summary="상품 이미지 분석")
async def analyze_product_endpoint(
    files: list[UploadFile] = File(...),
):
    """상품 이미지 분석 후 카테고리, 상품명, 색상, 상태, 설명 반환 (최대 5장)"""
    await validate_images(files)
    image_bytes_list = [await f.read() for f in files]
    return await analyze_product(image_bytes_list)
