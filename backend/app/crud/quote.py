from sqlalchemy.orm import Session
from app.db_models import Quote, QuoteLine, Job
from app.models import QuoteCreate, QuoteUpdate

def _calculate_total(lines) -> float:
    return sum(line.quantity * line.unit_price for line in lines)

def create_quote(db: Session, quote: QuoteCreate, job_id: int, technician_id: int):
    db_quote = Quote(
        job_id=job_id,
        technician_id=technician_id,
        description=quote.description,
        status="sent",
        total=0
    )
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)

    for line in quote.lines:
        db.add(QuoteLine(
            quote_id=db_quote.id,
            description=line.description,
            quantity=line.quantity,
            unit_price=line.unit_price
        ))
    db.commit()
    db.refresh(db_quote)

    db_quote.total = _calculate_total(db_quote.lines)
    db.commit()
    db.refresh(db_quote)
    return db_quote

def get_quote(db: Session, quote_id: int):
    return db.query(Quote).filter(Quote.id == quote_id).first()

def get_quotes_by_job(db: Session, job_id: int):
    return db.query(Quote).filter(Quote.job_id == job_id).all()

def get_quotes_by_technician(db: Session, technician_id: int):
    return db.query(Quote).filter(Quote.technician_id == technician_id).all()

def update_quote(db: Session, db_quote: Quote, data: QuoteUpdate):
    payload = data.model_dump(exclude_unset=True)

    if "description" in payload:
        db_quote.description = payload["description"]

    if "lines" in payload and payload["lines"] is not None:
        db.query(QuoteLine).filter(QuoteLine.quote_id == db_quote.id).delete()
        for line in payload["lines"]:
            db.add(QuoteLine(
                quote_id=db_quote.id,
                description=line["description"],
                quantity=line["quantity"],
                unit_price=line["unit_price"]
            ))
        db.commit()
        db.refresh(db_quote)
        db_quote.total = _calculate_total(db_quote.lines)

    db.commit()
    db.refresh(db_quote)
    return db_quote

def accept_quote(db: Session, db_quote: Quote, db_job: Job):
    db_quote.status = "accepted"
    db_job.status = "assigned"

    other_quotes = db.query(Quote).filter(
        Quote.job_id == db_job.id,
        Quote.id != db_quote.id
    ).all()
    for q in other_quotes:
        q.status = "rejected"

    db.commit()
    db.refresh(db_quote)
    return db_quote

def delete_quote(db: Session, db_quote: Quote):
    db.delete(db_quote)
    db.commit()