from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True,nullable=False)
    is_technician = Column(Boolean, default=False)
    phone = Column(String)
    hashed_password = Column(String,nullable=False)

    addresses = relationship("Address", back_populates="user")
    technicians = relationship("Technician", back_populates="user")

class Address(Base):
    __tablename__="addresses"

    id=Column(Integer, primary_key=True, index=True)
    street=Column(String,nullable=False)
    number=Column(Integer,nullable=False)
    zip_code=Column(String,nullable=False)

    user_id=Column(Integer, ForeignKey("users.id"), nullable=False)

    province_id = Column(Integer, ForeignKey("provinces.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    neighborhood_id = Column(Integer, ForeignKey("neighborhoods.id"))

    user=relationship("User",back_populates="addresses")

    province = relationship("Province")
    city = relationship("City")
    neighborhood = relationship("Neighborhood")

class Province(Base):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    cities = relationship("City", back_populates="province")
    
class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    province_id = Column(Integer, ForeignKey("provinces.id"))

    province = relationship("Province", back_populates="cities")
    neighborhoods = relationship("Neighborhood", back_populates="city")

class Neighborhood(Base):
    __tablename__ = "neighborhoods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="neighborhoods")


class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    technicians = relationship("TechnicianCategory", back_populates="category")

class Technician(Base):
    __tablename__ = "technicians"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    description = Column(String)
    rating = Column(Float, default=0)

    user = relationship("User")

    categories = relationship("TechnicianCategory", back_populates="technician")

    work_zones = relationship("TechnicianWorkZone", back_populates="technician")

class TechnicianCategory(Base):
    __tablename__ = "technician_categories"

    id = Column(Integer, primary_key=True)
    technician_id = Column(Integer, ForeignKey("technicians.id"))
    category_id = Column(Integer, ForeignKey("service_categories.id"))

    is_validated = Column(Boolean, default=False)
    certification_path = Column(String)  # futuro: PDF, imagen, etc

    technician = relationship("Technician", back_populates="categories")
    category = relationship("ServiceCategory",back_populates="technicians")

class TechnicianWorkZone(Base):
    __tablename__ = "technician_work_zones"

    id = Column(Integer, primary_key=True)
    technician_id = Column(Integer, ForeignKey("technicians.id"))
    neighborhood_id = Column(Integer, ForeignKey("neighborhoods.id"))

    technician = relationship("Technician", back_populates="work_zones")
    neighborhood = relationship("Neighborhood")



class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("service_categories.id"))

    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="open")

    user = relationship("User")
    category = relationship("ServiceCategory")
    quotes = relationship("Quote", back_populates="job")


class Quote(Base):
    __tablename__='quotes'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    technician_id = Column(Integer, ForeignKey("technicians.id"))

    description = Column(String)
    price = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="sent")

    job = relationship("Job", back_populates="quotes")
    technician = relationship("Technician")
    review = relationship("Review", back_populates="quote", uselist=False)




    

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey("quotes.id"), unique=True)

    rating = Column(Integer)
    comment = Column(String)

    quote = relationship("Quote", back_populates="review")