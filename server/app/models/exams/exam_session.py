"""
    Date written: 12/10/2025 at 8:49 PM
"""

import uuid
from sqlalchemy import Column, ForeignKey, String
from app.db.base import Base
from sqlalchemy.orm import relationship


class ExamSession(Base):
    __tablename__ = "exam_session"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # foreign keys
    exam_id = Column(String(36), ForeignKey("exam.id"), unique=True, nullable=False)
    student_id = Column(String(36), ForeignKey("student.id"), unique=True, nullable=False)
    professor_id = Column(String(36), ForeignKey("professor.id"), nullable=False)
    
    
    # many-to-one relationship with Exam
    exam = relationship(
        "Exam",
        back_populates="exam_sessions",
        uselist=False
    )
    
    
    # many-to-one relationship with Student
    student = relationship(
        "Student",
        back_populates="exam_sessions",
        uselist=False
    )
    
    
    # many-to-one relationship with Professor
    professor = relationship(
        "Professor",
        back_populates="exam_sessions",
        uselist=False
    )
    
    
    # one-to-many relationship with CheatingIncident
    cheating_incidents = relationship(
        "CheatingIncident",
        back_populates="exam_session",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    