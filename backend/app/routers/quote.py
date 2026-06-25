from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import QuoteCreate, QuoteUpdate, QuotePublic
from app.crud import job as crud_job
from app.crud import technician as crud_tech
from app.crud import quote as crud_quote
from app.routers.auth import get_current_user
from app.db_models import User

router = APIRouter(prefix="/jobs/{job_id}/quotes", tags=["Quotes"])
my_quotes_router = APIRouter(prefix="/quotes", tags=["Quotes"])

@router.post("/", response_model=QuotePublic)
def create_quote(
    job_id: int,
    quote: QuoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = crud_job.get_job(db, job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    technician = crud_tech.get_tech_user(db, current_user.id)
    if not technician:
        raise HTTPException(403, "Only technicians can send quotes")

    if job.status != "open":
        raise HTTPException(400, "This job is no longer accepting quotes")

    return crud_quote.create_quote(db, quote, job_id, technician.id)

@router.get("/", response_model=list[QuotePublic])
def list_quotes(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = crud_job.get_job(db, job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    all_quotes = crud_quote.get_quotes_by_job(db, job_id)

    if job.user_id == current_user.id or current_user.is_admin:
        return all_quotes

    technician = crud_tech.get_tech_user(db, current_user.id)
    if technician:
        return [q for q in all_quotes if q.technician_id == technician.id]

    raise HTTPException(403, "Not authorized")

@router.get("/{quote_id}", response_model=QuotePublic)
def get_quote(
    job_id: int,
    quote_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = crud_job.get_job(db, job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    quote = crud_quote.get_quote(db, quote_id)
    if not quote or quote.job_id != job_id:
        raise HTTPException(404, "Quote not found")

    technician = crud_tech.get_tech_user(db, current_user.id)
    is_owner = job.user_id == current_user.id
    is_quote_author = technician and quote.technician_id == technician.id
    is_admin = current_user.is_admin

    if not (is_owner or is_quote_author or is_admin):
        raise HTTPException(403, "Not authorized")

    return quote

@router.put("/{quote_id}", response_model=QuotePublic)
def update_quote(
    job_id: int,
    quote_id: int,
    data: QuoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quote = crud_quote.get_quote(db, quote_id)
    if not quote or quote.job_id != job_id:
        raise HTTPException(404, "Quote not found")

    technician = crud_tech.get_tech_user(db, current_user.id)
    if not technician or quote.technician_id != technician.id:
        raise HTTPException(403, "Not authorized")

    if quote.status != "sent":
        raise HTTPException(400, "Cannot edit a quote that has been accepted or rejected")

    return crud_quote.update_quote(db, quote, data)

@router.post("/{quote_id}/accept", response_model=QuotePublic)
def accept_quote(
    job_id: int,
    quote_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = crud_job.get_job(db, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if job.user_id != current_user.id:
        raise HTTPException(403, "Only the job owner can accept a quote")

    quote = crud_quote.get_quote(db, quote_id)
    if not quote or quote.job_id != job_id:
        raise HTTPException(404, "Quote not found")
    if quote.status != "sent":
        raise HTTPException(400, "This quote is no longer available")

    return crud_quote.accept_quote(db, quote, job)

@router.delete("/{quote_id}")
def delete_quote(
    job_id: int,
    quote_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quote = crud_quote.get_quote(db, quote_id)
    if not quote or quote.job_id != job_id:
        raise HTTPException(404, "Quote not found")

    technician = crud_tech.get_tech_user(db, current_user.id)
    if not technician or quote.technician_id != technician.id:
        raise HTTPException(403, "Not authorized")

    if quote.status != "sent":
        raise HTTPException(400, "Cannot delete a quote that has been accepted or rejected")

    crud_quote.delete_quote(db, quote)
    return {"ok": True}

@my_quotes_router.get("/mine", response_model=list[QuotePublic])
def list_my_quotes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    technician = crud_tech.get_tech_user(db, current_user.id)
    if not technician:
        raise HTTPException(403, "Only technicians have quotes to list")

    return crud_quote.get_quotes_by_technician(db, technician.id)