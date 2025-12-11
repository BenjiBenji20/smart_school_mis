"""
    Date written: 12/10/2025 at 6:05 PM
"""

import uuid
from sqlalchemy import Column, ForeignKey, String
from app.db.base import Base
from sqlalchemy.orm import relationship


class Program(Base):
    __table_name__ = "program"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # foreign keys
    program_chair_id = Column(String(36), ForeignKey("program_chair.id"), nullable=True)    
    department_id = Column(String(36), ForeignKey("department.id"), nullable=True)
    
    # one-to-one relationship with ProgramChair
    program_chair = relationship(
        "ProgramChair",
        back_populates="program",
        foreign_keys="ProgramChair.program_id",
        uselist=False
    )
    
    
    # many-to-one relationship with Department
    department = relationship(
        "Department",
        back_populates="programs",
        uselist=False
    )
     
    
    # one-to-many relationship with Student
    students = relationship(
        "Student",
        back_populates="program",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with Course
    courses = relationship(
        "Course",
        back_populates="program",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with Course
    class_sections = relationship(
        "ClassSection",
        back_populates="program",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    