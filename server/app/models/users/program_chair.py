"""
    Date written: 12/7/2025 at 2:49 PM
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String
from app.models.users.base_user import BaseUser

class ProgramChair(BaseUser):
    __tablename__ = "program_chair"
    
    id = Column(String(36), ForeignKey("base_user.id"), primary_key=True)
    
    # foreign keys
    program_id = Column(String(36), ForeignKey("program.id"), nullable=True)
    
    # one-to-one relationship with Program
    program = relationship(
        "Program",
        back_populates="program_chair",
        foreign_keys="Program.program_chair_id",
        uselist=False
    )
    
    
    # one-to-many relationship with Announcement
    announcements = relationship(
        "Announcement",
        back_populates="author",
        foreign_keys="Announcement.author_id",
        cascade="all, delete-orphan",
    )
    
    __mapper_args__ = {
        "polymorphic_identity": "program_chair",
    }
