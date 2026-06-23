from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TechnicianCreate,TechnicianUpdate, TechnicianPublic
from app.crud import technician as crud_tech
from app.crud import user as crud_user
from app.routers.auth import get_current_user
from app.db_models import User
from app.crud.technician import to_public_dict

router = APIRouter(prefix="/technicians", tags=["Technicians"])

@router.get("/match", response_model=list[TechnicianPublic])
def match_technicians(
    category_id: int,
    neighborhood_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    technicians = crud_tech.get_matching_technicians(db, category_id, neighborhood_id)
    return [to_public_dict(t) for t in technicians]

@router.get("/{tech_id}", response_model=TechnicianPublic)
def get_tech(tech_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    technician = crud_tech.get_tech(db, tech_id)
    if not technician:
        raise HTTPException(404, "Technician not found")
    return to_public_dict(technician)

@router.get("/", response_model=list[TechnicianPublic])
def list_techs(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    technicians = crud_tech.get_techs(db)
    return [to_public_dict(t) for t in technicians]

@router.patch("/{tech_id}", response_model=TechnicianPublic)
def update_tech(tech_id: int, data: TechnicianUpdate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    technician = crud_tech.get_tech(db, tech_id)
    if not technician:
        raise HTTPException(404, "Technician not found")
    if technician.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    updated = crud_tech.update_tech(db, technician, data)
    return to_public_dict(updated)

@router.delete("/{tech_id}")
def delete_tech(tech_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    technician = crud_tech.get_tech(db, tech_id)
    if not technician:
        raise HTTPException(404, "Technician not found")
    if technician.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    crud_tech.delete_tech(db, technician)
    return {"ok": True}

