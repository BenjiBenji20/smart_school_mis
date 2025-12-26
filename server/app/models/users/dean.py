"""
    Date written: 12/7/2025 at 2:49 PM
"""
 
from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from app.models.users.base_user import BaseUser
from app.models.enums.user_state import DeanStatus, UserRole

class Dean(BaseUser):
    __tablename__ = "dean"
    
    id = Column(String(36), ForeignKey("base_user.id"), primary_key=True)
    dean_status = Column(Enum(DeanStatus), default=DeanStatus.ACTIVE, nullable=False)
    
    # foreign keys
    department_id = Column(String(36), ForeignKey("department.id"), nullable=True)
    
    # one-to-one with Department relationship
    department = relationship(
        "Department",
        back_populates="dean",
        uselist=False,
        post_update=True
    )
    
    
    # one-to-many with Announcement relationship
    announcements = relationship(
        "Announcement",
        back_populates="author",
        foreign_keys="Announcement.author_id",
        cascade="all, delete-orphan"
    )
    
    __mapper_args__ = {
        "polymorphic_identity": UserRole.DEAN,
    }
    