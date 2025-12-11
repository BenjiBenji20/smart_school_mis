"""
    Date written: 12/10/2025 at 8:49 PM
"""

import uuid
from sqlalchemy import Column, ForeignKey, String
from app.db.base import Base
from sqlalchemy.orm import relationship

from app.models.academic_structures import professor_class_section


class ClassSection(Base):
    __tablename__ = "class_section"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # foreign keys
    course_id = Column(String(36), ForeignKey("course.id"), nullable=False)
    department_id = Column(String(36), ForeignKey("department.id"), nullable=False)
    program_id = Column(String(36), ForeignKey("program.id"), nullable=False)


    # many-to-one relationship with Course
    course = relationship(
        "Course",
        back_populates="class_sections",
        uselist=False
    )
     
    
    # many-to-one relationship with Department
    department = relationship(
        "Department",
        back_populates="class_sections",
        uselist=False
    )
    
    
    # many-to-one relationship with Program
    program = relationship(
        "Program",
        back_populates="class_sections",
        uselist=False 
    )


    # many-to-many relationship with Professor
    professors = relationship(
        "Professor",
        secondary=professor_class_section, # association table
        back_populates="class_sections",
        lazy="dynamic"
    )


    # one-to-many relationship with Enrollment
    enrollments = relationship(
        "Enrollment",
        back_populates="class_section",
        cascade="all, delete-orphan",
        lazy="dynamic"
    ) 
    