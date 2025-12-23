"""
    Date written: 12/10/2025 at 8:49 PM
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base

 
class Department(Base):
    __tablename__ = "department"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    title = Column(String(100), nullable=False)
    department_code = Column(String(10), nullable=True)
    description = Column(String(255), nullable=True)
    
    # one-to-one relationship with Dean 
    dean = relationship(
        "Dean",
        back_populates="department",
        uselist=False
    ) 
    
    
    # one-to-many relationship with Program
    programs = relationship(
        "Program",
        back_populates="department",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with Professor
    professors = relationship(
        "Professor",
        back_populates="department",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with Announcement
    announcements = relationship(
        "Announcement",
        foreign_keys="Announcement.department_audience_id",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    