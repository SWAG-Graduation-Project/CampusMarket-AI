import json

from fastapi import HTTPException, status
from google.genai import types

from app.constants.categories import CATEGORY_MAP
from app.core.gemini_client import get_client
from app.schemas.product_analysis import ProductAnalysisResponse, ProductCondition

_PROMPT = """
주어진 상품 이미지들을 분석하여 아래 JSON 형식으로만 응답하세요. 다른 텍스트는 포함하지 마세요.

사용 가능한 카테고리:
{categories}

{{
  "main_category": "위 목록 중 대카테고리명",
  "sub_category": "위 목록 중 소카테고리명",
  "product_name": "상품명",
  "color": "대표 색상 단어 (예: 검정, 흰색, 네이비)",
  "condition": "미개봉 또는 최상 또는 양호 또는 보통",
  "description": "상품 설명 3~5문장"
}}
"""


def _build_prompt() -> str:
    categories_text = "\n".join(
        f"- {main}: {', '.join(subs)}" for main, subs in CATEGORY_MAP.items()
    )
    return _PROMPT.format(categories=categories_text)


def _parse_response(text: str) -> dict:
    # Gemini가 ```json ... ``` 블록으로 감싸는 경우 제거
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


async def analyze_product(image_data: list[tuple[bytes, str]]) -> ProductAnalysisResponse:
    client = get_client()

    contents: list = [_build_prompt()]
    for image_bytes, mime_type in image_data:
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))

    response = await client.aio.models.generate_content(
        model="gemini-3-flash-preview",
        contents=contents,
    )

    data = _parse_response(response.text)

    try:
        return ProductAnalysisResponse(
            main_category=data["main_category"],
            sub_category=data["sub_category"],
            product_name=data["product_name"],
            color=data["color"],
            condition=ProductCondition(data["condition"]),
            description=data["description"],
        )
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Gemini 응답에 필수 항목이 누락되었습니다: {e}",
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Gemini가 유효하지 않은 상태값을 반환했습니다.",
        )
