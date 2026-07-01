from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserCreate, UserPublic, UserUpdate, ChangePassword,TechnicianCreate,TechnicianUpdate, TechnicianPublic
from app.crud import user as crud_user
from app.crud import technician as crud_tech
from app.routers.auth import get_current_user, require_admin
from app.db_models import User
from app.crud.technician import to_public_dict

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserPublic)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.get("/{user_id}", response_model=UserPublic)
def get(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    if user.id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    return user

@router.get("/", response_model=list[UserPublic])
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return crud_user.get_users(db)

@router.put("/{user_id}", response_model=UserPublic)
def update(user_id: int, data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    if user.id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    return crud_user.update_user(db, user, data)

@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    if user.id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Not authorized")
    crud_user.delete_user(db, user)
    return {"ok": True}


@router.post("/{user_id}/change-password")
def change_password_endpoint(user_id: int, data: ChangePassword, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:
        crud_user.change_password(db, user, data)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    return {"message": "Password updated successfully"}
