from sqlalchemy.orm import Session
from app.db_models import Job, JobInvitation, Address
from app.models import JobCreate, JobUpdate

def create_job(db: Session, job: JobCreate, user_id: int):
    db_job = Job(
        user_id=user_id,
        category_id=job.category_id,
        address_id=job.address_id,
        description=job.description,
        is_private=job.is_private,
        status="open"
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    for tech_id in job.technician_ids:
        db.add(JobInvitation(job_id=db_job.id, technician_id=tech_id))
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()

def get_jobs_by_user(db: Session, user_id: int):
    return db.query(Job).filter(Job.user_id == user_id).all()

def get_open_jobs(db: Session):
    return db.query(Job).filter(Job.status == "open", Job.is_private == False).all()

def get_invited_job_ids(db: Session, technician_id: int):
    invitations = db.query(JobInvitation).filter(
        JobInvitation.technician_id == technician_id
    ).all()
    return [inv.job_id for inv in invitations]

def update_job(db: Session, db_job: Job, data: JobUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_job, field, value)
    db.commit()
    db.refresh(db_job)
    return db_job

def delete_job(db: Session, db_job: Job):
    db.delete(db_job)
    db.commit()

def get_matching_open_jobs(db: Session, technician):
    category_ids = [tc.category_id for tc in technician.categories]
    neighborhood_ids = [wz.neighborhood_id for wz in technician.work_zones]

    if not category_ids or not neighborhood_ids:
        return []

    return db.query(Job).join(Address, Job.address_id == Address.id).filter(
        Job.status == "open",
        Job.is_private == False,
        Job.category_id.in_(category_ids),
        Address.neighborhood_id.in_(neighborhood_ids)
    ).all()