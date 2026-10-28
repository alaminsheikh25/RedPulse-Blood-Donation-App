from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.models import *  # noqa: F401,F403 ensure metadata
from app.api.routes import auth, donors, requests, hospitals, donations, inventory, appointments, campaigns, notifications, reports, matches
from app.schemas.common import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=settings.log_level)
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = settings.api_v1_prefix
app.include_router(auth.router, prefix=api_prefix)
app.include_router(donors.router, prefix=api_prefix)
app.include_router(requests.router, prefix=api_prefix)
app.include_router(hospitals.router, prefix=api_prefix)
app.include_router(donations.router, prefix=api_prefix)
app.include_router(inventory.router, prefix=api_prefix)
app.include_router(appointments.router, prefix=api_prefix)
app.include_router(campaigns.router, prefix=api_prefix)
app.include_router(notifications.router, prefix=api_prefix)
app.include_router(reports.router, prefix=api_prefix)
app.include_router(matches.router, prefix=api_prefix)


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health() -> HealthResponse:
    from datetime import datetime, timezone

    return HealthResponse(status="ok", version=settings.app_version, timestamp=datetime.now(timezone.utc))
