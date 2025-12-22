"""
    Date written: 12/22/2025 at 12:44 PM
"""

import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Curriculum(Base):
    __tablename__ = "curriculum"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # foreign keys
    program_id = Column(String(36), ForeignKey("program.id"), nullable=True)
    
    
    # many-to-one relationship with Program
    program = relationship(
        "Program",
        back_populates="curriculums",
        uselist=False
    ) 
    
    
    # one-to-many relationship with CurriculumCourse
    curriculum_courses = relationship(
        "CurriculumCourse",
        back_populates="curriculum",
        uselist=True
    ) 
    
    
    # one-to-many relationship with CourseOffering
    course_offerings = relationship(
        "CourseOffering",
        back_populates="curriculum",
        uselist=True
    ) 
    