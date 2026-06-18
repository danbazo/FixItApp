from xml.dom import NotFoundErr
from sqlalchemy.orm import Session
from app.db_models import User,Technician,TechnicianCategory,TechnicianWorkZone
from app.models import TechnicianCreate,TechnicianUpdate

def create_tech(db: Session, technician: TechnicianCreate, user_id: int):

    db_user = db.get(User, user_id)

    if not db_user:
        raise NotFoundErr("User not found")


    if db_user.is_technician:
        raise ValueError("User already has technician profile")
    
    db_tech = Technician(
        user_id=db_user.id,
        description=technician.description,

    )
    db_user.is_technician=True
    db.add(db_tech)
    db.commit()
    db.refresh(db_tech)

    for category_id in technician.categories_ids:
        db.add(
            TechnicianCategory(
                technician_id=db_tech.id,
                category_id=category_id
            )
        )

    for neighborhood_id in technician.work_zones_ids:
        db.add(
            TechnicianWorkZone(
                technician_id=db_tech.id,
                neighborhood_id=neighborhood_id
            )
        )

    db.commit()
    db.refresh(db_tech)

    return db_tech

def get_tech(db: Session, tech_id: int):
    return db.query(Technician).filter(Technician.id == tech_id).first()

def get_tech_user(db: Session, user_id:int):
    return db.query(Technician).filter(Technician.user_id == user_id).first()

def get_techs(db: Session):
    return db.query(Technician).all()

def update_tech(db: Session, db_tech: Technician, data: TechnicianUpdate):
    payload = data.model_dump(exclude_unset=True)

    
    if "description" in payload:
        db_tech.description = payload["description"]

    
    if "categories_ids" in payload:
        db.query(TechnicianCategory).filter(
            TechnicianCategory.technician_id == db_tech.id
        ).delete()

        for category_id in payload["categories_ids"]:
            db.add(
                TechnicianCategory(
                    technician_id=db_tech.id,
                    category_id=category_id
                )
            )

    
    if "work_zones_ids" in payload:
        db.query(TechnicianWorkZone).filter(
            TechnicianWorkZone.technician_id == db_tech.id
        ).delete()

        for neighborhood_id in payload["work_zones_ids"]:
            db.add(
                TechnicianWorkZone(
                    technician_id=db_tech.id,
                    neighborhood_id=neighborhood_id
                )
            )

    db.commit()
    db.refresh(db_tech)
    return db_tech


def delete_tech(db: Session, tech_id: int):

    db_tech=db.get(Technician, tech_id)
    if not db_tech:
        raise NotFoundErr("Technician not found")
    db_user=db.get(User,db_tech.user_id)

    db_user.is_technician=False

    db.delete(db_tech)
    db.commit()

def delete_tech_user(db: Session, user_id: int):
    db_user=db.get(User,user_id)

    if not db_user.is_technician:
        raise NotFoundErr("User is not technician")

    db_tech=db.query(Technician).filter(Technician.user_id == user_id).first()
    
    if not db_tech:
        raise NotFoundErr("Technician not found")
        
    db_user.is_technician=False

    db.delete(db_tech)
    db.commit()
