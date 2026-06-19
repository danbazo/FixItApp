from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AddressCreate, AdressUpdate, AddressPublic
from app.crud import address as crud_address
from app.routers.auth import get_current_user
from app.db_models import User

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.post("/", response_model=AddressPublic)
def create(address: AddressCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_address.create_address(db, address, current_user.id)

@router.get("/", response_model=list[AddressPublic])
def list_my_addresses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_address.get_addresses_by_user(db, current_user.id)

@router.get("/{address_id}", response_model=AddressPublic)
def get(address_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    address = crud_address.get_address(db, address_id)
    if not address:
        raise HTTPException(404, "Address not found")
    if address.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")
    return address

@router.put("/{address_id}", response_model=AddressPublic)
def update(address_id: int, data: AdressUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    address = crud_address.get_address(db, address_id)
    if not address:
        raise HTTPException(404, "Address not found")
    if address.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")
    return crud_address.update_address(db, address, data)

@router.delete("/{address_id}")
def delete(address_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    address = crud_address.get_address(db, address_id)
    if not address:
        raise HTTPException(404, "Address not found")
    if address.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")
    crud_address.delete_address(db, address)
    return {"ok": True}