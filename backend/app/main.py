"""
AI Desktop Assistant — FastAPI Application Entrypoint
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings
from app.models.database import Base


# ── Database setup ───────────────────────────────────

engine = create_async_engine(settings.database_url, echo=True)


async def init_db():
    """Create all tables on startup (MVP — use Alembic in production)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ── App lifespan ─────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown logic."""
    await init_db()
    print("Database tables created")
    yield
    await engine.dispose()
    print("Database engine disposed")


# ── FastAPI app ──────────────────────────────────────

app = FastAPI(
    title="AI Desktop Assistant API",
    description="Backend API for the Autonomous AI Desktop Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ───────────────────────────────────────────

@app.get("/")
async def root():
    return {"message": "AI Desktop Assistant API is running", "status": "ok"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
