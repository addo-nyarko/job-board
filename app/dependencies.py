from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_or_404(db: Session, model, record_id: int, detail: str = "Not found"):
    instance = db.query(model).filter(model.id == record_id).first()
    if not instance:
        raise HTTPException(status_code=404, detail=detail)
    return instance
