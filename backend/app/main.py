from unicodedata import category

from fastapi import Body, FastAPI

from app.database import engine, Base

from app import db_models

from app.routers import user, auth, certification, technician, category, address, job

app=FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(technician.router)
app.include_router(certification.router)
app.include_router(category.router)
app.include_router(address.router)
app.include_router(job.router)


@app.get("/health")
def health():
    return {"status": "ok"}

Base.metadata.create_all(bind=engine)