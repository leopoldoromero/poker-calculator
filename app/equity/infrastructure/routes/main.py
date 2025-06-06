from fastapi import APIRouter
from app.equity.infrastructure.routes.post_calculate_equity import post_calculate_equity

api_router = APIRouter()

api_router.include_router(post_calculate_equity.router)