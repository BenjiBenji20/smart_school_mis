"""
    Date written: 12/26/2025 at 5:41 PM
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, SmallInteger, String, Time
from sqlalchemy.orm import relationship, validates

from app.db.base import Base


class ClassSchedule(Base):
    __tablename__ = "class_schedule"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False) 
    
    day_of_week = Column(SmallInteger, nullable=False)  # 1=Mon, 7=Sun
    # day of week must not less than 1 (monday) or greater than 7 (sunday)
    @validates("day_of_week")
    def validate_day_of_week(self, key, value):
        if value > 7 or value < 1:
            raise ValueError(f"Invalid day schedule: {value}")
        return value
    
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # foreign keys
    class_section_id = Column(ForeignKey("class_section.id"), nullable=False)
    room_id = Column(ForeignKey("room.id"), nullable=True)
    
    # many-to-one relationship with ClassSection
    class_section = relationship(
        "ClassSection",
        back_populates="class_schedules",
        uselist=False
    )

    
    # many-to-one relationship with Room
    room = relationship(
        "Room",
        back_populates="class_schedules",
        uselist=False
    )
        