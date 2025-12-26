"""
    Date written: 12/22/2025 at 12:29 PM
"""

from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Enum, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.enums.academic_structure_state import CourseOfferingStatus


class CourseOffering(Base):
    __tablename__ = "course_offering" 

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    status = Column(Enum(CourseOfferingStatus), default=CourseOfferingStatus.PENDING, nullable=False)
    
    term_id = Column(String(36), ForeignKey("term.id"), nullable=False)
    curriculum_course_id = Column(String(36), ForeignKey("curriculum_course.id"), nullable=False)
    
    # one-to-many relationship with ClassSection
    class_sections = relationship(
        "ClassSection",
        back_populates="course_offering",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # many-to-one relationship with Term
    term = relationship(
        "Term",
        back_populates="course_offerings",
        uselist=False
    )
    
    
    # many-to-one relationship with CurriculumCourse
    curriculum_course = relationship(
        "CurriculumCourse",
        back_populates="course_offerings",
        uselist=False
    )
    
    
    # One CurriculumCourse can only be offered once per Term
    __table_args__ = (
        UniqueConstraint(
            "curriculum_course_id",
            "term_id",
            name="uq_course_offering_curriculum_course_term"
        ),
    )

    