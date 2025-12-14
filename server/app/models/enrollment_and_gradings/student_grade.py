"""
    Date written: 12/10/2025 at 8:49 PM
"""

import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class StudentGrade(Base):
    __tablename__ = "student_grade"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # foreign keys
    enrollment_id = Column(String(36), ForeignKey("enrollment.id"), unique=True, nullable=False)
    encoded_by_id = Column(String(36), ForeignKey("professor.id"), nullable=False)
    
    
    # one-to-one relationship with StudentGrade
    enrollment = relationship( 
        "Enrollment",
        back_populates="student_grade",
        uselist=False
    )
    
     
    # many-to-one relationship with Professor
    professor = relationship(
        "Professor",
        back_populates="student_grades",
        uselist=False
    )
    