"""
    Date written: 12/10/2025 at 8:49 PM
"""

import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Department(Base):
    __tablename__ = "department"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # foreign keys
    dean_id = Column(String(36), ForeignKey("dean.id"), nullable=True)
    
    # one-to-one relationship with Dean 
    dean = relationship(
        "Dean",
        back_populates="department",
        foreign_keys="Dean.department_id",
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
    
    
    # one-to-many relationship with ClassSection
    class_sections = relationship(
        "ClassSection",
        back_populates="department",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    