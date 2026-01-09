
from typing import Optional,  List

from pydantic import BaseModel, EmailStr, Field

from enum import Enum


class JobStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    finished = "finished"
    cancelled = "cancelled"


class QuoteStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"




#Core Models

class Address(BaseModel):
    id:int
    street:str
    number:int
    zip_code:str
    neihborhood:str
    city:str
    province:str 


class User(BaseModel):
    id: int
    first_name: str
    last_name:str
    email:EmailStr
    is_technitian:bool=False
    addresses:Optional[List[Address]]=[]
    phone:str
    

class ServiceCategory(BaseModel):
    id: int
    name: str
    description:str
    requires_certification:bool=False
    validated:bool=False
    

class Technitian(BaseModel):
    id: int
    user: User
    description:str
    categories: List[ServiceCategory]
    work_zones: List[str]
    rating:float=Field(ge=0, le=5)

class Job(BaseModel):
    id:int
    client:User
    description:str
    category: ServiceCategory
    status: JobStatus=JobStatus.open

class Quote(BaseModel):
    id:int
    job: Job
    technitian:Technitian
    description:str
    price:float
    status:QuoteStatus=QuoteStatus.pending

class Review(BaseModel):
    id:int
    quote: Quote
    rating: float=Field(ge=0, le=5)
    comment:Optional[str]
