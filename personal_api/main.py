"""Application entry point.

Creates the FastAPI app, initialises the database (tables + seed data),
registers routers, CORS middleware and global error handlers.

Run:        uvicorn main:app --reload
Windows:    double-click run.bat
"""
import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from database import Base, engine
from init_db import seed_initial_data
from routes import auth, contact, education, profile, projects, services, skills

# ── 1. Create tables and seed the first admin + sample content ───────────
Base.metadata.create_all(bind=engine)
seed_initial_data()

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Personal backend API serving profile, skills, projects, education, "
        "services and contact messages. Public endpoints are open; "
        "management endpoints require admin authentication."
    ),
    version="1.0.0",
    docs_url="/docs",    # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# ── 2. CORS — controlled by the CORS_ORIGINS environment variable ────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# ── 3. Register all routers ───────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(education.router)
app.include_router(services.router)
app.include_router(contact.router)


# ── 4. Consistent error responses ────────────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Pydantic validation failures return 422 with field-level details."""
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": jsonable_encoder(exc.errors())},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all: log the real error, never leak internals to the client."""
    logging.getLogger("uvicorn.error").exception(
        "Unhandled error on %s %s", request.method, request.url.path
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/", tags=["Health"])
def root():
    """Simple health check / API index."""
    return {"name": settings.APP_NAME, "status": "ok", "docs": "/docs"}
