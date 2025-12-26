"""
    Date written: 12/7/2025 at 2:49 PM
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Enum, ForeignKey, String
from app.models.users.base_user import BaseUser
from app.models.academic_structures.professor_class_section import ProfessorClassSection
from app.models.enums.user_state import ProfessorStatus, UserRole

class Professor(BaseUser):
    __tablename__ = "professor"
     
    id = Column(String(36), ForeignKey("base_user.id"), primary_key=True)
    professor_status = Column(Enum(ProfessorStatus), default=ProfessorStatus.ACTIVE, nullable=False)
    
    # foreign keys
    department_id = Column(String(36), ForeignKey("department.id"), nullable=True)
    
    
    class_section_links = relationship(
        "ProfessorClassSection",
        back_populates="professor",
        cascade="all, delete-orphan"
    )
    
    
    # many-to-many relationship with ClassSection
    class_sections = relationship(
        "ClassSection",
        secondary="professor_class_section",
        viewonly=True
    )
    
    
    # many-to-one relationship with Department
    department = relationship(
        "Department",
        back_populates="professors",
        uselist=False
    )
     
    
    # one-to-many relationship with Task
    tasks = relationship(
        "Task",
        back_populates="professor",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )   
    
     
    # one-to-many relationship with Exam
    exams = relationship(
        "Exam",
        back_populates="professor",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
     
    
    # one-to-many relationship with StudentGrade
    student_grades = relationship(
        "StudentGrade",
        back_populates="professor",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with TaskSubmission
    task_submissions = relationship(
        "TaskSubmission",
        back_populates="professor",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with ExamSession
    exam_sessions = relationship(
        "ExamSession",
        back_populates="professor",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with Announcement
    announcements = relationship(
        "Announcement", 
        back_populates="author",
        foreign_keys="Announcement.author_id",
        cascade="all, delete-orphan",
    )
    
    __mapper_args__ = {
        "polymorphic_identity": UserRole.PROFESSOR
    }
    