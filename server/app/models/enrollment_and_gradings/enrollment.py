"""
    Date written: 12/10/2025 at 8:49 PM
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums.enrollment_and_grading_state import EnrollmentStatus


class Enrollment(Base):
    __tablename__ = "enrollment"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    status = Column(
        Enum(EnrollmentStatus, name="enrollment_status", create_type=False),
        default=EnrollmentStatus.PENDING,
        nullable=False,
        name="status"
    )

    # foreign keys
    student_id = Column(String(36), ForeignKey("student.id"), nullable=False)
    class_section_id = Column(String(36), ForeignKey("class_section.id"), nullable=False)
    term_id = Column(String(36), ForeignKey("term.id"), nullable=False)

    # one-to-one relationship with StudentGrade
    student_grade = relationship(
        "StudentGrade",
        back_populates="enrollment",
        uselist=False
    )

  
    # many-to-one relationship with Student
    student = relationship(
        "Student",
        back_populates="enrollments",
        uselist=False
    )
    
    
    # many-to-one relationship with Term
    term = relationship(
        "Term",
        back_populates="enrollments",
        uselist=False
    )


    # many-to-one relationship with ClassSection
    class_section = relationship(
        "ClassSection",
        back_populates="enrollments",
        uselist=False
    )
    
    __table_args__ = (
        UniqueConstraint('student_id', 'class_section_id', 'term_id', name='uq_student_section'),
    )
    