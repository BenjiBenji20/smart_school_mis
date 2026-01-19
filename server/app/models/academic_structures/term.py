"""
    Date written: 12/22/2025 at 1:12 PM
"""

from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.enums.academic_structure_state import SemesterPeriod, TermStatus


class Term(Base):
    __tablename__ = "term"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    academic_year_start = Column(SmallInteger, nullable=False)  # e.g. 2025
    academic_year_end = Column(SmallInteger, nullable=False)    # e.g. 2026
    
    enrollment_start = Column(DateTime(timezone=True), nullable=False)
    enrollment_end = Column(DateTime(timezone=True), nullable=False)

    # FIRST | SECOND | SUMMER
    semester_period = Column(Enum(SemesterPeriod), default=SemesterPeriod.FIRST, nullable=False)
    # DRAFT | OPEN | CLOSED | ARCHIVED
    status = Column(Enum(TermStatus), default=TermStatus.DRAFT, nullable=False)

    
    # one-to-many relationship with CourseOffering
    course_offerings = relationship(
        "CourseOffering",
        back_populates="term",
        uselist=True
    )
    
    
    # one-to-many relationship with Enrollment
    enrollments = relationship(
        "Enrollment",
        back_populates="term",
        uselist=True
    )
    
    
    # enforce 1 semester period in academic year
    __table_args__ = (
        UniqueConstraint(
            "academic_year_start",
            "semester_period",
            name="unique_term_per_year_semester"
        ),
    )
    