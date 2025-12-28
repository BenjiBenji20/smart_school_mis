"""
    Date written: 12/7/2025 at 2:49 PM
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Date, ForeignKey, SmallInteger, String

from app.models.users.base_user import BaseUser
from app.models.enums.user_state import UserRole

class Student(BaseUser): 
    __tablename__ = "student"
    
    id = Column(String(36), ForeignKey("base_user.id"), primary_key=True)
    # foreign keys
    program_id = Column(String(36), ForeignKey("program.id"), nullable=True)

    last_school_attended = Column(String(255), nullable=True)
    program_enrolled_date = Column(Date, nullable=True)
    year_level = Column(SmallInteger, default=1, nullable=False) # default (1) first year when first approved
     
    # many-to-one relationship with Program
    program = relationship(
        "Program",
        back_populates="students",
        uselist=False
    )
    
    
    # one-to-many relationship with Enrollement
    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    
    # one-to-many relationship with TaskSubmission
    task_submissions = relationship(
        "TaskSubmission",
        back_populates="student",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with ExamSession
    exam_sessions = relationship(
        "ExamSession",
        back_populates="student",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    __mapper_args__ = {
        "polymorphic_identity": UserRole.STUDENT,
    }
    