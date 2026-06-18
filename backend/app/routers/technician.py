from sys import prefix
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TechnicianCreate,TechnicianUpdate, TechnicianPublic
from app.crud import technician as crud_tech
from app.crud import user as crud_user

router = APIRouter(prefix="/technicians", tags=["Technicians"])


@router.get("/{tech_id}", response_model=TechnicianPublic)
def get_tech(tech_id: int, db: Session = Depends(get_db)):
    technician = crud_tech.get_tech(db, tech_id)
    if not technician:
        raise HTTPException(404, "Technician not found")
    return technician

@router.get("/", response_model=list[TechnicianPublic])
def list_techs(db: Session = Depends(get_db)):
    return crud_tech.get_techs(db)

@router.patch("/{tech_id}", response_model=TechnicianPublic)
def update_tech(tech_id: int, data: TechnicianUpdate, db: Session = Depends(get_db)):
    technician = crud_tech.get_tech(db, tech_id)
    if not technician:
        raise HTTPException(404, "Technician not found")
    return crud_tech.update_tech(db, technician, data)

@router.delete("/{tech_id}")
def delete_tech(tech_id: int, db: Session = Depends(get_db)):
    technician = crud_tech.get_tech(db, tech_id)
    if not technician:
        raise HTTPException(404, "Technician not found")
    crud_tech.delete_tech(db, technician)
    return {"ok": True}
