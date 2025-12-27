"""
    Date written: 12/26/2025 at 6:04 PM
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, SmallInteger, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Room(Base):
    __tablename__ = "room"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False) 
    
    room_code = Column(String(10), unique=True, nullable=True)
    capacity = Column(SmallInteger, nullable=False) # student capacity

    # foreign keys
    building_id = Column(ForeignKey("building.id"), nullable=False)
    
    # many-to-one relationship with Building
    building = relationship(
        "Building",
        back_populates="rooms",
        uselist=False
    )
    
    
    # one-to-many relationship with ClassSchedule
    class_schedules = relationship(
        "ClassSchedule",
        back_populates = "room",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
            