"""
    Date written: 12/10/2025 at 8:49 PM
"""

import uuid
from sqlalchemy import Column, ForeignKey, String
from app.db.base import Base
from sqlalchemy.orm import relationship


class CheatingIncident(Base):
    __tablename__ = "cheating_incident"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # foreign keys
    exam_session_id = Column(String(36), ForeignKey("exam_session.id"), unique=True, nullable=False)
    reviewed_by_id = Column(String(36), ForeignKey("base_user.id"), unique=True, nullable=False)
     
    # many-to-one relationship with ExamSession
    exam_session = relationship(
        "ExamSession",
        back_populates="cheating_incidents",
        uselist=False
    )
    
    
    # many-to-one relationship with BaseUser
    reviewed_by = relationship(
        "BaseUser",
        back_populates="reviewed_by",
        uselist=False
    )
    