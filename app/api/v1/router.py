from fastapi import APIRouter, Depends

from app.api.v1.endpoints import background_removal, product_analysis, timetable
from app.core.dependencies import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])

router.include_router(
    background_removal.router,
    prefix="/images",
    tags=["Background Removal"],
)
router.include_router(
    product_analysis.router,
    prefix="/images",
    tags=["Product Analysis"],
)
router.include_router(
    timetable.router,
    prefix="/timetable",
    tags=["Timetable"],
)
