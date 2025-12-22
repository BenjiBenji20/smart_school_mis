"""
    Date written: 12/22/2025 at 12:29 PM
"""

import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class CourseOffering(Base):
    __tablename__ = "course_offering" 

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    curriculum_id = Column(String(36), ForeignKey("curriculum.id"), nullable=True)
    term_id = Column(String(36), ForeignKey("term.id"), nullable=True)
    course_id = Column(String(36), ForeignKey("course.id"), nullable=True)
    
    # one-to-many relationship with ClassSection
    class_sections = relationship(
        "ClassSection",
        back_populates="course_offering",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # many-to-one relationship with Curriculum
    curriculum = relationship(
        "Curriculum",
        back_populates="course_offerings",
        uselist=False
    )
    
    
    # many-to-one relationship with Term
    term = relationship(
        "Term",
        back_populates="course_offerings",
        uselist=False
    )
    
    
    # many-to-one relationship with Course
    course = relationship(
        "Course",
        back_populates="course_offerings",
        uselist=False
    )
    