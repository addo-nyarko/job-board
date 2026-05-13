import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_or_404
from app.models import Job, Question
from app.schemas import JobCreate, JobOut

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/", response_model=JobOut, status_code=201)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    job = Job(
        title=job_data.title,
        description=job_data.description,
        location=job_data.location,
        customer=job_data.customer,
        job_name=job_data.job_name,
    )
    db.add(job)
    db.flush()

    for q in job_data.questions:
        question = Question(
            text=q.text,
            type=q.type.value,
            scoring=q.scoring,
            job_id=job.id,
        )
        db.add(question)

    db.commit()
    db.refresh(job)
    logger.info("Created job %d: %s", job.id, job.title)
    return job


@router.get("/", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Job, job_id, "Job not found")


@router.delete("/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = get_or_404(db, Job, job_id, "Job not found")
    db.delete(job)
    db.commit()
    logger.info("Deleted job %d", job_id)
