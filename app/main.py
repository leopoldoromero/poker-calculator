from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.equity.infrastructure.routes.main import api_router
from app.config.app_config import ALLOWED_HOSTS, APPLICATION_TITLE, OPENAPI_PATH

app = FastAPI(
    title=APPLICATION_TITLE,
    openapi_url=OPENAPI_PATH,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

