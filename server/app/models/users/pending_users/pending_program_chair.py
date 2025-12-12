"""
    Date written: 12/12/2025 at 11:51 AM
"""

from sqlalchemy import Column, ForeignKey, String
from app.models.users.program_chair import ProgramChair


class PendingProgramChair(ProgramChair):
    __tablename__ = "pending_program_chair"
    
    id = Column(String(36), ForeignKey("program_chair.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "pending_program_chair"
    }