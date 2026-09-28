import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routes import candidates, pages

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Recruiter Candidate Management API",
    description="ATS-style Candidate Tracking, Search, and Audit Trail Application",
    version="1.0.0"
)

# Static files setup
os.makedirs("app/static/css", exist_ok=True)
os.makedirs("app/static/js", exist_ok=True)
os.makedirs("data", exist_ok=True)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include Routers
app.include_router(candidates.router)
app.include_router(pages.router)


@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint for automated testing and monitoring."""
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected server error occurred.", "details": str(exc)}
    )