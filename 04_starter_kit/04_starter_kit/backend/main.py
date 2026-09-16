"""Point d'entrée FastAPI."""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from backend.config import settings
from backend.database import Base, engine
from backend.routers import chat, files

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# Création des tables au démarrage (en prod : Alembic recommandé)
Base.metadata.create_all(bind=engine)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.app_name,
    description="Starter kit IA - BA3 Dev HEH",
    version="0.1.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS strict (jamais "*" en prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log basique de chaque requête."""
    response = await call_next(request)
    logger.info("%s %s -> %d", request.method, request.url.path, response.status_code)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Capture les exceptions non gérées pour ne pas exposer les stack traces."""
    logger.exception("Erreur non gérée sur %s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Erreur interne du serveur"})


# Routers
app.include_router(chat.router)
app.include_router(files.router)


@app.get("/")
async def root():
    """Healthcheck."""
    return {
        "app": settings.app_name,
        "environment": settings.environment,
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Healthcheck pour monitoring."""
    return {"status": "healthy"}
