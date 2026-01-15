from sqlalchemy.orm import Session
from app.db_models import User
from app.models import UserCreate, UserUpdate, ChangePassword
from app.security import verify_password, hash_password

def create_user(db: Session, user: UserCreate):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        is_technician=user.is_technician,
        hashed_password=hash_password(user.password),
        )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, db_user: User, data: UserUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()

def change_password(db: Session, db_user: User, data: ChangePassword):
    if not verify_password(data.current_password, db_user.hashed_password):
        raise ValueError("Incorrect password")

    db_user.hashed_password = hash_password(data.new_password)
    db.commit()
    return True