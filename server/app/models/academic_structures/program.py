"""
    Date written: 12/10/2025 at 6:05 PM
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from app.db.base import Base
from sqlalchemy.orm import relationship


class Program(Base):
    __tablename__ = "program"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    title = Column(String(100), nullable=False)
    program_code = Column(String(10), nullable=True)
    description = Column(String(255), nullable=True)
    
  
    # foreign keys
    department_id = Column(String(36), ForeignKey("department.id"), nullable=True)
    
    # many-to-one relationship with Department
    department = relationship(
        "Department",
        back_populates="programs",
        uselist=False
    )
    
    
    # one-to-one relationship with ProgramChair
    program_chair = relationship(
        "ProgramChair",
        back_populates="program",
        uselist=False,
        post_update=True
    )
     
    
    # one-to-many relationship with Student
    students = relationship(
        "Student",
        back_populates="program",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with Curriculum
    curriculums = relationship(
        "Curriculum",
        back_populates="program",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with Announcement
    announcements = relationship(
        "Announcement",
        foreign_keys="Announcement.program_audience_id",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    