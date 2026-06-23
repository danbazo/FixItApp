from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import JobCreate, JobUpdate, JobPublic, JobPublicLimited
from app.crud import job as crud_job
from app.crud import technician as crud_tech
from app.routers.auth import get_current_user
from app.db_models import User, Job

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobPublic)
def create(job: JobCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_job.create_job(db, job, current_user.id)

@router.get("/mine", response_model=list[JobPublic])
def list_my_jobs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_job.get_jobs_by_user(db, current_user.id)

@router.get("/feed", response_model=list[JobPublicLimited])
def job_feed(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    technician = crud_tech.get_tech_user(db, current_user.id)
    if not technician:
        raise HTTPException(403, "Only technicians can view the job feed")

    matching_jobs = crud_job.get_matching_open_jobs(db, technician)
    invited_ids = crud_job.get_invited_job_ids(db, technician.id)
    invited_jobs = db.query(Job).filter(Job.id.in_(invited_ids)).all() if invited_ids else []

    seen_ids = set()
    result = []
    for j in matching_jobs + invited_jobs:
        if j.id not in seen_ids:
            seen_ids.add(j.id)
            result.append(_to_limited(j))
    return result

def _to_limited(job: Job) -> JobPublicLimited:
    return JobPublicLimited(
        id=job.id,
        description=job.description,
        category_id=job.category_id,
        status=job.status,
        neighborhood_name=job.address.neighborhood.name
    )

@router.get("/{job_id}", response_model=JobPublic)
def get(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = crud_job.get_job(db, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if job.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    return job

@router.put("/{job_id}", response_model=JobPublic)
def update(job_id: int, data: JobUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = crud_job.get_job(db, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if job.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    return crud_job.update_job(db, job, data)

@router.delete("/{job_id}")
def delete(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = crud_job.get_job(db, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if job.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    crud_job.delete_job(db, job)
    return {"ok": True}