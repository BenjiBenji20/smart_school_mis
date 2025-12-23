"""
    Date written: 12/22/2025 at 12:51 PM
"""

from datetime import datetime, timezone
import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class CurriculumCourse(Base):
    __tablename__ = "curriculum_course"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    year_level = Column(SmallInteger, nullable=False)
    semester = Column(SmallInteger, nullable=False)
    is_required = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint(
            "curriculum_id", "course_id",
            name="uq_curriculum_course"
        ),
    )
    
    # foreign keys
    curriculum_id = Column(String(36), ForeignKey("curriculum.id"), nullable=True)
    course_id = Column(String(36), ForeignKey("course.id"), nullable=True)
    
    
    # many-to-one relationship with Curriculum
    curriculum = relationship(
        "Curriculum",
        back_populates="curriculum_courses",
        uselist=False
    ) 
    
    
    # many-to-one relationship with Course
    course = relationship(
        "Course",
        back_populates="curriculum_courses",
        uselist=False
    ) 
    