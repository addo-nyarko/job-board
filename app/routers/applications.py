from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import applications as applications_controller
from app.dependencies import get_db
from app.schemas import ApplicationCreate, ApplicationOut

router = APIRouter(tags=["Applications"])


@router.post("/jobs/{job_id}/apply", response_model=ApplicationOut, status_code=201)
def apply_to_job(job_id: int, app_data: ApplicationCreate, db: Session = Depends(get_db)):
    return applications_controller.apply_to_job(db, job_id, app_data)


@router.get("/applications/{application_id}", response_model=ApplicationOut)
def get_application(application_id: int, db: Session = Depends(get_db)):
    return applications_controller.get_application(db, application_id)


@router.get("/jobs/{job_id}/applications", response_model=list[ApplicationOut])
def list_applications_for_job(job_id: int, db: Session = Depends(get_db)):
    return applications_controller.list_applications_for_job(db, job_id)
