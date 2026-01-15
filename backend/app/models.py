
from typing import Optional,  List

from pydantic import BaseModel, EmailStr, Field

from enum import Enum

from datetime import datetime


class JobStatus(str, Enum):
    open = "open"
    quoted="quoted"
    assigned="assigned"
    in_progress = "in_progress"
    finished = "finished"
    cancelled = "cancelled"


class QuoteStatus(str, Enum):
    sent = "sent"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"




#Core Models

class AddressBase(BaseModel):
    street:str
    number:int
    zip_code:str
    province_id:int
    city_id:int
    neighborhood_id:int

class AddressCreate(AddressBase):
    pass

class AdressUpdate(BaseModel):
    street:Optional[str]=None
    number:Optional[int]=None
    zip_code:Optional[str]=None
    province_id:Optional[int]=None
    city_id:Optional[int]=None
    neighborhood_id:Optional[int]=None
    


class AddressPublic(AddressBase):
    id:int

    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    
    first_name: str
    last_name:str
    email:EmailStr
    is_technician:bool=False
    phone:str

class UserCreate(UserBase):
    password:str=Field(min_length=8)

class UserUpdate(BaseModel):
    first_name: Optional[str]=None
    last_name:Optional[str]=None
    email:Optional[EmailStr]=None
    phone:Optional[str]=None
    is_technician:Optional[bool]=None

class ChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)

class UserPublic(UserBase):
    id: int
    #created_at: datetime
    addresses: list[AddressPublic]=[]

    model_config = {"from_attributes": True}



class ServiceCategoryBase(BaseModel):
    name: str
    description: str
    requires_certification: bool = False


class ServiceCategoryCreate(ServiceCategoryBase):
    pass


class ServiceCategoryUpdate(BaseModel):
    name: Optional[str]=None
    description: Optional[str]=None
    requires_certification: Optional[bool] = None   


class ServiceCategoryPublic(ServiceCategoryBase):
    id: int

    model_config = {"from_attributes": True}



class TechnicianBase(BaseModel):
    description:str
    
class TechnicianCreate(TechnicianBase):
    work_zones_ids: list[int]
    categories_ids: list[int]

class TechnicianUpdate(BaseModel):
    description:Optional[str]=None
    work_zones_ids: Optional[list[int]]=None
    categories_ids: Optional[list[int]]=None

class TechnicianPublic(TechnicianBase):
    id:int
    user_id: int
    work_zones_ids:list[int]
    categories_ids:list[int]
    rating:float
    model_config = {"from_attributes": True}


class JobBase(BaseModel):
    description:str
    category_id:int

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    description:Optional[str]=None
    category_id:Optional[int]=None

class JobPublic(JobBase):
    id:int
    user_id:int
    status:JobStatus
    model_config = {"from_attributes": True}



class QuoteBase(BaseModel):
    description:str
    price:float

class QuoteCreate(QuoteBase):
    pass

class QuoteUpdate(BaseModel):
    description:Optional[str]=None
    price:Optional[float]=None

class QuotePublic(QuoteBase):
    id:int
    job_id:int
    tech_id:int
    status:QuoteStatus

    model_config = {"from_attributes": True}


class ReviewBase(BaseModel):
    rating:int=Field(ge=1, le=5)
    comment:Optional[str]

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating:Optional[int]=Field(default=None, ge=1, le=5)
    comment:Optional[str]

class ReviewPublic(ReviewBase):
    id:int
    quote_id: int

    model_config = {"from_attributes": True}