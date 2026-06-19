from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ServiceCategoryCreate, ServiceCategoryUpdate, ServiceCategoryPublic
from app.crud import category as crud_category
from app.routers.auth import get_current_user, require_admin
from app.db_models import User

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=ServiceCategoryPublic)
def create(category: ServiceCategoryCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return crud_category.create_category(db, category)

@router.get("/", response_model=list[ServiceCategoryPublic])
def list_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_category.get_categories(db)

@router.get("/{category_id}", response_model=ServiceCategoryPublic)
def get(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = crud_category.get_category(db, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    return category

@router.put("/{category_id}", response_model=ServiceCategoryPublic)
def update(category_id: int, data: ServiceCategoryUpdate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    category = crud_category.get_category(db, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    return crud_category.update_category(db, category, data)

@router.delete("/{category_id}")
def delete(category_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    category = crud_category.get_category(db, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    crud_category.delete_category(db, category)
    return {"ok": True}