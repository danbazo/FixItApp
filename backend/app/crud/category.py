from sqlalchemy.orm import Session
from app.db_models import ServiceCategory
from app.models import ServiceCategoryCreate, ServiceCategoryUpdate

def create_category(db: Session, category: ServiceCategoryCreate):
    db_category = ServiceCategory(
        name=category.name,
        description=category.description,
        requires_certification=category.requires_certification
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    return db.query(ServiceCategory).filter(ServiceCategory.id == category_id).first()

def get_categories(db: Session):
    return db.query(ServiceCategory).all()

def update_category(db: Session, db_category: ServiceCategory, data: ServiceCategoryUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_category, field, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, db_category: ServiceCategory):
    db.delete(db_category)
    db.commit()