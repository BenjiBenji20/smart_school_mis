"""
    Date written: 12/10/2025 at 8:49 PM
"""

import uuid 
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Course(Base):
    __tablename__ = "course"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    program_id = Column(String(36), ForeignKey("program.id"), nullable=False)
    
    # many-to-one relationship with Program
    program = relationship(
        "Program",
        back_populates="courses",
        uselist=False
    )
    
    
    # one-to-many relationship with ClassSection
    class_sections = relationship(
        "ClassSection",
        back_populates="course",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
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
    