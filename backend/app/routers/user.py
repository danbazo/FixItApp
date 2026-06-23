from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserCreate, UserPublic, UserUpdate, ChangePassword,TechnicianCreate,TechnicianUpdate, TechnicianPublic
from app.crud import user as crud_user
from app.crud import technician as crud_tech
from app.routers.auth import get_current_user
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
    return user

@router.get("/", response_model=list[UserPublic])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_user.get_users(db)

@router.put("/{user_id}", response_model=UserPublic)
def update(user_id: int, data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return crud_user.update_user(db, user, data)

@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    crud_user.delete_user(db, user)
    return {"ok": True}


@router.post("/{user_id}/change-password")
def change_password_endpoint(
    user_id: int,
    data: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = crud_user.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        crud_user.change_password(db, user, data)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    return {"message": "Password updated successfully"}



#create technitian

@router.post("/{user_id}/technician", response_model=TechnicianPublic)
def create_tech(user_id:int, technician: TechnicianCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user=crud_user.get_user(db,user_id)
    if not user:
        raise HTTPException(404, "User not found")
    try:
        new_tech = crud_tech.create_tech(db, technician, user_id)
        return to_public_dict(new_tech)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}/technician", response_model=TechnicianPublic)
def get_tech(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    technician = crud_tech.get_tech_user(db, user_id)
    if not technician:
        raise HTTPException(404, "Technician not found")
    return to_public_dict(technician)

@router.delete("/{user_id}/technician")
def delete_tech(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user=crud_user.get_user(db,user_id)

    if not user:
        raise HTTPException(404, "User not found")
    crud_tech.delete_tech_user(db, user_id)
    return {"ok": True}
