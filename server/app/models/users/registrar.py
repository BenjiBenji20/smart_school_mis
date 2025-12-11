"""
    Date written: 12/7/2025 at 2:49 PM
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String
from app.models.users.base_user import BaseUser

class Registrar(BaseUser):
    __tablename__ = "registrar"
    
    id = Column(String(36), ForeignKey("base_user.id"), primary_key=True)


    # one-to-many relationship with Announcement
    announcements = relationship(
        "Announcement",
        back_populates="author",
        foreign_keys="Announcement.author_id",
        cascade="all, delete-orphan",
    )

    __mapper_args__ = {
        "polymorphic_identity": "registrar",
    }
