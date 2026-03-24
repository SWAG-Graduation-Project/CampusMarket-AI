from fastapi import APIRouter

from app.api.v1.endpoints import background_removal, product_analysis, timetable

router = APIRouter()

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
