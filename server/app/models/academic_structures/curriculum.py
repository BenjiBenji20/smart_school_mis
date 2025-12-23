"""
    Date written: 12/22/2025 at 12:44 PM
"""

from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, SmallInteger, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.enums.academic_structure_state import CurriculumStatus


class Curriculum(Base):
    __tablename__ = "curriculum"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    title = Column(String(100), nullable=False) # e.g. BSIT Curriculum 2025–2029
    effective_from = Column(SmallInteger, nullable=False)  # e.g. 2025
    effective_to = Column(SmallInteger, nullable=True)     # e.g. 2029 (nullable if ongoing)
    status = Column(Enum(CurriculumStatus), nullable=False) # DRAFT | ACTIVE | RETIRED
    
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
    