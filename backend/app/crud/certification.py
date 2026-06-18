from sqlalchemy.orm import Session
from app.db_models import TechnicianCertification
from app.models import CertificationCreate

def create_certification(db: Session, certification: CertificationCreate, technician_id: int):
    db_cert = TechnicianCertification(
        technician_id=technician_id,
        category_id=certification.category_id,
        name=certification.name,
        institution=certification.institution,
        year=certification.year,
        is_validated=False
    )
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert

def get_certifications(db: Session, technician_id: int):
    return db.query(TechnicianCertification).filter(
        TechnicianCertification.technician_id == technician_id
    ).all()

def get_certification(db: Session, cert_id: int):
    return db.query(TechnicianCertification).filter(
        TechnicianCertification.id == cert_id
    ).first()

def delete_certification(db: Session, cert_id: int):
    db_cert = get_certification(db, cert_id)
    if not db_cert:
        raise ValueError("Certification not found")
    db.delete(db_cert)
    db.commit()