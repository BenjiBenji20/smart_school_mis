"""
    Date written: 12/22/2025 at 1:12 PM
"""

import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Term(Base):
    __tablename__ = "term"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
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
    