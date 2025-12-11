"""
    Date written: 12/10/2025 at 8:49 PM
"""
 
import uuid
from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from app.models.users.base_user import BaseUser
from app.models.enums.user_role import UserRole

class Announcement(BaseUser):
    __tablename__ = "announcement"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # foreign keys
    author_id = Column(String(36), ForeignKey("base_user.id"), nullable=True)
    department_audience_id = Column(String(36), ForeignKey("department.id"), nullable=True)
    program_audience_id = Column(String(36), ForeignKey("program.id"), nullable=True)
    
    author_role = Column(Enum(UserRole), nullable=False)
    
    
    # many-to-one relationship with BaseUser (author, polymorphic)
    author = relationship(
        "BaseUser",
        foreign_keys=[author_id],
        uselist=False
    )

    
    # many-to-one relationship with Department
    department_audience = relationship(
        "Department",
        back_populates="announcements",
        uselist=False
    )
    
    
    # many-to-one relationship with Program
    program_audience = relationship(
        "Program",
        back_populates="announcements",
        uselist=False
    )
    