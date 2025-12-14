"""
    Date written: 12/10/2025 at 8:49 PM
"""

import uuid
from sqlalchemy import Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class Enrollment(Base):
    __tablename__ = "enrollment"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # foreign keys
    student_id = Column(String(36), ForeignKey("student.id"), nullable=False)
    class_section_id = Column(String(36), ForeignKey("class_section.id"), nullable=False)

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


    # many-to-one relationship with ClassSection
    class_section = relationship(
        "ClassSection",
        back_populates="enrollments",
        uselist=False
    )
    
    __table_args__ = (
        UniqueConstraint('student_id', 'class_section_id', name='uq_student_section'),
    )
    