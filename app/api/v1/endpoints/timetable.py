from fastapi import APIRouter, File, UploadFile

from app.core.dependencies import validate_image
from app.schemas.timetable import TimetableResponse
from app.services.timetable_service import parse_timetable

router = APIRouter()


@router.post("/parse-timetable", response_model=TimetableResponse, summary="시간표 이미지 파싱")
async def parse_timetable_endpoint(
    file: UploadFile = File(...),
):
    """시간표 이미지 분석 후 수업명, 요일, 시작/끝 시간, 강의실 반환"""
    await validate_image(file)
    image_bytes = await file.read()
    return await parse_timetable(image_bytes, file.content_type)
