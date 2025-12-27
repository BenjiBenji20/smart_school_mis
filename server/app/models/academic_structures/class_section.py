"""
    Date written: 12/10/2025 at 8:49 PM
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, Enum, ForeignKey, SmallInteger, String, UniqueConstraint
from app.db.base import Base
from sqlalchemy.orm import relationship

from app.models.academic_structures.professor_class_section import ProfessorClassSection
from app.models.enums.academic_structure_state import ClassSectionStatus


class ClassSection(Base):
    __tablename__ = "class_section"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False) 
    
    section_code = Column(String(10), nullable=False)
    room_number = Column(SmallInteger, nullable=True) 
    student_capacity = Column(SmallInteger, nullable=False)
    time_schedule = Column(String(50), nullable=True)
    status = Column(Enum(ClassSectionStatus), default=ClassSectionStatus.CLOSE, nullable=False)
    
    # foreign keys
    course_offering_id = Column(String(36), ForeignKey("course_offering.id"), nullable=False)
    
    
    # many-to-one relationship with CourseOffering
    course_offering = relationship(
        "CourseOffering",
        back_populates="class_sections"
    )


    professor_links = relationship(
        "ProfessorClassSection",
        back_populates="class_section",
        cascade="all, delete-orphan"
    )


    # many-to-many relationship with Professor
    professors = relationship(
        "Professor",
        secondary="professor_class_section",
        viewonly=True
    )


    # one-to-many relationship with Enrollment
    enrollments = relationship(
        "Enrollment",
        back_populates="class_section",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with Task
    tasks = relationship(
        "Task",
        back_populates="class_section",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with Exam
    exams = relationship(
        "Exam",
        back_populates="class_section",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with ClassSchedule
    class_schedules = relationship(
        "ClassSchedule",
        back_populates="class_section",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one section code can only be there per course offering
    __table_args__ = (
        UniqueConstraint(
            "section_code",
            "course_offering_id",
            name="uq_class_section_section_code_course_offering",
        ),
    )
    