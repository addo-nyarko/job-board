from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import jobs as jobs_controller
from app.dependencies import get_db
from app.schemas import JobCreate, JobOut

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/", response_model=JobOut, status_code=201)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    return jobs_controller.create_job(db, job_data)


@router.get("/", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    return jobs_controller.list_jobs(db)


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return jobs_controller.get_job(db, job_id)


@router.delete("/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    jobs_controller.delete_job(db, job_id)
