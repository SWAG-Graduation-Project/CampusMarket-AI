from pydantic import BaseModel


class ClassEntry(BaseModel):
    name: str | None = None
    day: str          # 예: "월", "화", "수", "목", "금", "토", "일"
    start_time: str   # 예: "09:00" (24시간제)
    end_time: str     # 예: "10:30" (24시간제)
    location: str | None = None


class TimetableResponse(BaseModel):
    classes: list[ClassEntry]
    count: int
