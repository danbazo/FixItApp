from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CertificationCreate, CertificationPublic
from app.crud import certification as crud_cert
from app.crud import technician as crud_tech
from app.routers.auth import get_current_user
from app.db_models import User

router = APIRouter(prefix="/technicians", tags=["Certifications"])

@router.post("/{technician_id}/certifications", response_model=CertificationPublic)
def add_certification(
    technician_id: int,
    certification: CertificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tech = crud_tech.get_tech(db, technician_id)
    if not tech:
        raise HTTPException(404, "Technician not found")
    if tech.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    return crud_cert.create_certification(db, certification, technician_id)

@router.get("/{technician_id}/certifications", response_model=list[CertificationPublic])
def list_certifications(
    technician_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tech = crud_tech.get_tech(db, technician_id)
    if not tech:
        raise HTTPException(404, "Technician not found")
    return crud_cert.get_certifications(db, technician_id)

@router.delete("/{technician_id}/certifications/{cert_id}")
def delete_certification(
    technician_id: int,
    cert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tech = crud_tech.get_tech(db, technician_id)
    if not tech:
        raise HTTPException(404, "Technician not found")
    if tech.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    try:
        crud_cert.delete_certification(db, cert_id)
    except ValueError:
        raise HTTPException(404, "Certification not found")
    return {"ok": True}