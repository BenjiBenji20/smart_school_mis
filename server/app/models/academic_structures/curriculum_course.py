"""
    Date written: 12/22/2025 at 12:51 PM
"""

import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class CurriculumCourse(Base):
    __tablename__ = "curriculum_course"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # foreign keys
    curriculum_id = Column(String(36), ForeignKey("curriculum.id"), nullable=True)
    course_id = Column(String(36), ForeignKey("course.id"), nullable=True)
    
    
    # many-to-one relationship with Curriculum
    curriculum = relationship(
        "Curriculum",
        back_populates="curriculum_courses",
        uselist=False
    ) 
    
    
    # many-to-one relationship with Course
    course = relationship(
        "Course",
        back_populates="curriculum_courses",
        uselist=False
    ) 
    