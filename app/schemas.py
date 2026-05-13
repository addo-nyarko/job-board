from pydantic import BaseModel, EmailStr, Field
from typing import Union

from app.enums import QuestionType


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    type: QuestionType
    scoring: dict


class QuestionOut(BaseModel):
    id: int
    text: str
    type: QuestionType

    model_config = {"from_attributes": True}


class JobCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1, max_length=100)
    customer: str = Field(..., min_length=1, max_length=100)
    job_name: str = Field(..., min_length=1, max_length=200)
    questions: list[QuestionCreate] = Field(..., min_length=1)


class JobOut(BaseModel):
    id: int
    title: str
    description: str
    location: str
    customer: str
    job_name: str
    questions: list[QuestionOut]

    model_config = {"from_attributes": True}


class AnswerCreate(BaseModel):
    question_id: int
    response: Union[str, list[str]]


class ApplicationCreate(BaseModel):
    candidate_name: str = Field(..., min_length=1, max_length=100)
    candidate_email: EmailStr
    answers: list[AnswerCreate] = Field(..., min_length=1)


class AnswerOut(BaseModel):
    question_id: int
    response: Union[str, list[str]]

    model_config = {"from_attributes": True}


class ApplicationOut(BaseModel):
    id: int
    candidate_name: str
    candidate_email: str
    score: float
    answers: list[AnswerOut]

    model_config = {"from_attributes": True}
