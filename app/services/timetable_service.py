import asyncio
import json
from collections import defaultdict

from fastapi import HTTPException, status
from google.genai import types
from pydantic import ValidationError

from app.core.gemini_client import DEFAULT_MODEL, get_client
from app.schemas.timetable import ClassEntry, TimetableResponse

_PROMPT = """
한국의 대학교 앱 '에브리타임' 시간표 이미지입니다. 시간표 격자 안에 있는 모든 수업을 추출하여 JSON 배열로만 응답하세요.

- 요일: 월/화/수/목/금/토/일
- 시간: 24시간제 HH:MM (오후 1시=13:00), 대부분 00분, 15분, 30분, 45분 단위로 존재.
- 장소: 수업명 아래 강의실 번호, 없으면 null
- 격자 바깥 텍스트는 무시

[
  {{
    "name": "수업명 또는 null",
    "day": "요일",
    "start_time": "HH:MM",
    "end_time": "HH:MM",
    "location": "강의실 또는 null"
  }}
]
"""

_GEMINI_TIMEOUT = 120.0


def _to_minutes(t: str) -> int:
    try:
        h, m = map(int, t.split(":"))
        return h * 60 + m
    except (ValueError, AttributeError):
        return 0


def _from_minutes(mins: int) -> str:
    return f"{mins // 60:02d}:{mins % 60:02d}"


def _resolve_conflicts(classes: list[ClassEntry]) -> list[ClassEntry]:
    # 요일별로 분리 후 시작 시간 순 정렬
    by_day: dict[str, list[ClassEntry]] = defaultdict(list)
    for c in classes:
        by_day[c.day].append(c)

    result = []
    for day_classes in by_day.values():
        day_classes.sort(key=lambda c: _to_minutes(c.start_time))
        resolved: list[ClassEntry] = []
        for cls in day_classes:
            if not resolved:
                resolved.append(cls)
                continue

            prev = resolved[-1]
            prev_end = _to_minutes(prev.end_time)
            cls_start = _to_minutes(cls.start_time)
            cls_end = _to_minutes(cls.end_time)

            if cls_start < prev_end:
                # 겹침: start를 이전 수업 종료 시간으로 조정
                if prev_end < cls_end:
                    cls = cls.model_copy(update={"start_time": _from_minutes(prev_end)})
                    resolved.append(cls)
                # prev_end >= cls_end 이면 완전히 포함 → 해당 항목 제거
            else:
                resolved.append(cls)

        result.extend(resolved)

    return result


def _parse_response(text: str) -> list[dict]:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Gemini 응답을 파싱할 수 없습니다. 다시 시도해주세요.",
        )


async def parse_timetable(image_bytes: bytes, mime_type: str) -> TimetableResponse:
    client = get_client()

    contents = [
        _PROMPT,
        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
    ]

    try:
        response = await asyncio.wait_for(
            client.aio.models.generate_content(
                model=DEFAULT_MODEL,
                contents=contents,
            ),
            timeout=_GEMINI_TIMEOUT,
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Gemini API 응답 시간이 초과되었습니다. 다시 시도해주세요. (제한: 60초)",
        )

    raw_list = _parse_response(response.text)

    try:
        classes = [ClassEntry(**item) for item in raw_list]
    except (KeyError, ValueError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Gemini 응답에 누락되거나 잘못된 항목이 있습니다: {e}",
        )

    classes = _resolve_conflicts(classes)

    return TimetableResponse(classes=classes, count=len(classes))
