from fastapi import APIRouter
from app.equity.infrastructure.routes.post_calculate_equity import post_calculate_equity
from app.equity.infrastructure.routes.v1.hand_vs_hand import calculate_hand_vs_hand
from app.equity.infrastructure.routes.v1.hand_vs_range import calculate_hand_vs_range
from app.equity.infrastructure.routes.v1.range_vs_range import calculate_range_vs_range

api_router = APIRouter()

api_router.include_router(post_calculate_equity.router)

api_router.include_router(calculate_hand_vs_hand.router)
api_router.include_router(calculate_hand_vs_range.router)
api_router.include_router(calculate_range_vs_range.router)