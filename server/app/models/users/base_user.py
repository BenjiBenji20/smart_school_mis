"""
    Date written: 12/7/2025 at 2:49 PM
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, func
from app.db.base import Base
from app.models.enums.user_state import UserRole, UserStatus

class BaseUser(Base):
    __tablename__ = "base_user"
    
    # metadata
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # personal details
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=False)
    suffix = Column(String(4), nullable=True)
    age = Column(Integer, default=18, nullable=False)
    complete_address = Column(String(255), nullable=False)
    
    # account details
    email = Column(String(100), nullable=False, unique=True, index=True)
    cellphone_number = Column(String(13), nullable=False)
    password_hash = Column(String(100), nullable=False)
    
    # photo storage info
    filename = Column(String, nullable=True)
    file_url = Column(String, nullable=True)  # CDN or storage URL
    file_size = Column(Integer, nullable=True)  # Size in bytes
    mime_type = Column(String, nullable=True)  # image/jpeg, image/png
    
    # profile photo metadata
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # account security
    failed_attempts = Column(Integer, default=0, nullable=False)
    banned_until = Column(DateTime(timezone=True), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)
    
    # university individuality 
    # discriminator
    role = Column(Enum(UserRole), nullable=False)
    # [Approved, Rejected, Pending]
    status = Column(Enum(UserStatus), default=UserStatus.PENDING, nullable=False)
    
    __mapper_args__ = {
        "polymorphic_on": role
    }
    