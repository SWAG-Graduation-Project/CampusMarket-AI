from pydantic import BaseModel


class ClassEntry(BaseModel):
    name: str
    day: str        # 예: "월", "화", "수", "목", "금"
    start_time: str  # 예: "09:00"
    end_time: str    # 예: "10:30"
    location: str


class TimetableResponse(BaseModel):
    classes: list[ClassEntry]
    count: int
