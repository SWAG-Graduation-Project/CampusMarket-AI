from fastapi import APIRouter, File, UploadFile

from app.schemas.timetable import TimetableResponse

router = APIRouter()


@router.post("/parse-timetable", response_model=TimetableResponse, summary="시간표 이미지 파싱")
async def parse_timetable(
    file: UploadFile = File(...),
):
    """시간표 이미지 분석 후 수업명, 요일, 시작/끝 시간, 강의실 반환"""
    # TODO: call timetable_service
    raise NotImplementedError
