from pydantic import BaseModel
from enum import Enum


class ProductCondition(str, Enum):
    UNOPENED = "미개봉"
    BEST = "최상"
    GOOD = "양호"
    NORMAL = "보통"


class ProductAnalysisResponse(BaseModel):
    main_category: str
    sub_category: str
    product_name: str
    color: str
    condition: ProductCondition
    description: str  # 3~5문장
