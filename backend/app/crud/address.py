from sqlalchemy.orm import Session
from app.db_models import Address
from app.models import AddressCreate, AdressUpdate

def create_address(db: Session, address: AddressCreate, user_id: int):
    db_address = Address(
        street=address.street,
        number=address.number,
        zip_code=address.zip_code,
        province_id=address.province_id,
        city_id=address.city_id,
        neighborhood_id=address.neighborhood_id,
        user_id=user_id
    )
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_address(db: Session, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()

def get_addresses_by_user(db: Session, user_id: int):
    return db.query(Address).filter(Address.user_id == user_id).all()

def update_address(db: Session, db_address: Address, data: AdressUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_address, field, value)
    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db: Session, db_address: Address):
    db.delete(db_address)
    db.commit()