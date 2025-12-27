"""
    Date written: 12/26/2025 at 6:04 PM
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, SmallInteger, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Building(Base):
    __tablename__ = "building"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False) 
    
    name = Column(String(100), nullable=False, unique=True)
    room_capacity = Column(SmallInteger, nullable=False)
    
    # one-to-many relationship with Department
    departments = relationship(
        "Department",
        back_populates="building",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    
    # one-to-many relationship with Room
    rooms = relationship(
        "Room",
        back_populates="building",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
            