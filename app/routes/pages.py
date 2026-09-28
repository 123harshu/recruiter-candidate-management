from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import candidate_service


router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def render_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    candidates = candidate_service.query_candidates(db)

    counts = {
        "Applied": 0,
        "Screening": 0,
        "Interview": 0,
        "Offer": 0,
        "Hired": 0,
    }

    for candidate in candidates:
        stage = candidate["current_stage"]

        if stage in counts:
            counts[stage] += 1

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "candidates": candidates,
            "counts": counts,
        },
    )


@router.get("/candidates/new", response_class=HTMLResponse)
def render_add_candidate_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="candidate_form.html",
        context={
            "request": request,
        },
    )


@router.get("/candidates/{candidate_id}", response_class=HTMLResponse)
def render_candidate_detail(
    candidate_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    candidate = candidate_service.get_candidate(db, candidate_id)

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found",
        )

    return templates.TemplateResponse(
        request=request,
        name="candidate_detail.html",
        context={
            "request": request,
            "candidate": candidate,
        },
    )
