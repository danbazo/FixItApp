from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CertificationCreate, CertificationPublic
from app.crud import certification as crud_cert
from app.crud import technician as crud_tech
from app.routers.auth import get_current_user
from app.db_models import User

router = APIRouter(prefix="/technicians/mine/certifications", tags=["Certifications"])

def _get_own_technician(db: Session, current_user: User):
    technician = crud_tech.get_tech_user(db, current_user.id)
    if not technician:
        raise HTTPException(403, "You don't have a technician profile")
    return technician

@router.post("/", response_model=CertificationPublic)
def add_certification(
    certification: CertificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    technician = _get_own_technician(db, current_user)
    return crud_cert.create_certification(db, certification, technician.id)

@router.get("/", response_model=list[CertificationPublic])
def list_certifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    technician = _get_own_technician(db, current_user)

    return crud_cert.get_certifications(db, technician.id)

@router.delete("/{cert_id}")
def delete_certification(
    cert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    technician = _get_own_technician(db, current_user)
    cert = crud_cert.get_certification(db, cert_id)
    if not cert or cert.technician_id != technician.id:
        raise HTTPException(404, "Certification not found")
    crud_cert.delete_certification(db, cert_id)
    return {"ok": True}