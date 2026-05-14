import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_or_404
from app.models import Answer, Application, Job
from app.schemas import ApplicationCreate
from app.services.scoring import calculate_score

logger = logging.getLogger(__name__)


def apply_to_job(db: Session, job_id: int, app_data: ApplicationCreate) -> Application:
    job = get_or_404(db, Job, job_id, "Job not found")

    valid_question_ids = {q.id for q in job.questions}
    for answer in app_data.answers:
        if answer.question_id not in valid_question_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Question {answer.question_id} does not belong to this job",
            )

    application = Application(
        candidate_name=app_data.candidate_name,
        candidate_email=app_data.candidate_email,
        job_id=job_id,
        score=0.0,
    )
    db.add(application)
    db.flush()

    for answer_data in app_data.answers:
        answer = Answer(
            response=answer_data.response,
            question_id=answer_data.question_id,
            application_id=application.id,
        )
        db.add(answer)

    db.flush()
    db.refresh(application)

    answers_as_dicts = [
        {"question_id": a.question_id, "response": a.response} for a in application.answers
    ]
    application.score = calculate_score(answers_as_dicts, job.questions)  # type: ignore[assignment]

    db.commit()
    db.refresh(application)
    logger.info(
        "Application %d submitted for job %d (score: %.1f)",
        application.id,
        job_id,
        application.score,
    )
    return application


def get_application(db: Session, application_id: int) -> Application:
    return get_or_404(db, Application, application_id, "Application not found")


def list_applications_for_job(db: Session, job_id: int) -> list[Application]:
    get_or_404(db, Job, job_id, "Job not found")
    return (
        db.query(Application)
        .filter(Application.job_id == job_id)
        .order_by(Application.score.desc())
        .all()
    )
