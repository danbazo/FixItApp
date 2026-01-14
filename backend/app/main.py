from fastapi import Body, FastAPI,status,HTTPException,Response, Depends

from app.db_models import User, Address, Province, City, Neighborhood, Job, Quote, Review, Technician, ServiceCategory, TechnicianCategory, TechnicianWorkZone



app=FastAPI()



@app.get("/health")
def health():
    return {"status": "ok"}

from app.database import engine, Base

from app import db_models

Base.metadata.create_all(bind=engine)