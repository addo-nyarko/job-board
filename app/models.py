from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(100), nullable=False)
    customer = Column(String(100), nullable=False)
    job_name = Column(String(200), nullable=False)

    questions = relationship("Question", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    type = Column(String(20), nullable=False)
    scoring = Column(JSON, nullable=False)

    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    job = relationship("Job", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String(100), nullable=False)
    candidate_email = Column(String(200), nullable=False)
    score = Column(Float, default=0.0)

    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    job = relationship("Job", back_populates="applications")
    answers = relationship("Answer", back_populates="application", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    response = Column(JSON, nullable=False)

    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    question = relationship("Question", back_populates="answers")

    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    application = relationship("Application", back_populates="answers")
