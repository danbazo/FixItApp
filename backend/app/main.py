from fastapi import Body, FastAPI,status,HTTPException,Response, Depends

from app.db_models import User, Address, Province, City, Neighborhood, Job, Quote, Review, Technician, ServiceCategory, TechnicianCategory, TechnicianWorkZone

from app.database import engine, Base

from app import db_models

from app.routers import user

app=FastAPI()

app.include_router(user.router)

@app.get("/health")
def health():
    return {"status": "ok"}

Base.metadata.create_all(bind=engine)