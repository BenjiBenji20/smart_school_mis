"""
    Date written: 12/10/2025 at 8:49 PM
"""

import uuid
from sqlalchemy import Column, ForeignKey, String
from app.db.base import Base
from sqlalchemy.orm import relationship


class Exam(Base):
    __tablename__ = "exam"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # foreign keys
    course_id = Column(String(36), ForeignKey("course.id"), nullable=False)
    class_section_id = Column(String(36), ForeignKey("class_section.id"), nullable=True) 
    professor_id = Column(String(36), ForeignKey("professor.id"), nullable=False)
    
    
    # many-to-one relationship with Course
    course = relationship(
        "Course",
        back_populates="exams",
        uselist=False
    ) 
    
    
    # many-to-one relationship with ClassSection
    class_section = relationship(
        "ClassSection",
        back_populates="exams",
        uselist=False
    )
    
    
    # many-to-one relationship with Professor
    professor = relationship(
        "Professor",
        back_populates="exams",
        uselist=False
    )
    
    
    # one-to-many relationship with ExamSession
    exam_sessions = relationship(
        "ExamSession",
        back_populates="exam",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    