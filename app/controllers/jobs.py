import logging

from sqlalchemy.orm import Session

from app.dependencies import get_or_404
from app.models import Job, Question
from app.schemas import JobCreate

logger = logging.getLogger(__name__)


def create_job(db: Session, job_data: JobCreate) -> Job:
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


def list_jobs(db: Session) -> list[Job]:
    return db.query(Job).all()


def get_job(db: Session, job_id: int) -> Job:
    return get_or_404(db, Job, job_id, "Job not found")


def delete_job(db: Session, job_id: int) -> None:
    job = get_or_404(db, Job, job_id, "Job not found")
    db.delete(job)
    db.commit()
    logger.info("Deleted job %d", job_id)
