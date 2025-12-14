"""
    Date written: 12/10/2025 at 8:49 PM
"""

import uuid
from sqlalchemy import Column, ForeignKey, String
from app.db.base import Base
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "task"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # foreign keys
    course_id = Column(String(36), ForeignKey("course.id"), nullable=True)
    class_section_id = Column(String(36), ForeignKey("class_section.id"), nullable=True)
    professor_id = Column(String(36), ForeignKey("professor.id"), nullable=True)
    
    
    # many-to-one relationship with Course
    course = relationship(
        "Course",
        back_populates="tasks",
        uselist=False
    )
    
    
    # many-to-one relationship with ClassSection
    class_section  = relationship(
        "ClassSection",
        back_populates="tasks",
        uselist=False
    )
    
    
    # many-to-one relationship with Professor
    professor = relationship(
        "Professor",
        back_populates="tasks",
        uselist=False
    )
    
     
    # one-to-many relationship with TaskSubmission
    task_submissions = relationship(
        "TaskSubmission",
        back_populates="task",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    