"""
    Date written: 12/10/2025 at 8:49 PM
"""

from datetime import datetime, timezone
import uuid 
from sqlalchemy import Column, DateTime, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Course(Base):
    __tablename__ = "course"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    title = Column(String(100), unique=True, nullable=False)
    course_code = Column(String(10), unique=True, nullable=True)
    units = Column(SmallInteger, nullable=False)
    description = Column(String(255), nullable=True)
    
    
    # one-to-many relationship with Task
    tasks = relationship(
        "Task",
        back_populates="course",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with Exam
    exams = relationship(
        "Exam",
        back_populates="course",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with CurriculumCourse
    curriculum_courses = relationship(
        "CurriculumCourse",
        back_populates="course",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with CourseOffering
    course_offerings = relationship(
        "CourseOffering",
        back_populates="course",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    UniqueConstraint("course_code")
