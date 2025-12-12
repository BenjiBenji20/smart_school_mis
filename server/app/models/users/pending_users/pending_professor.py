"""
    Date written: 12/12/2025 at 11:51 AM
"""

from sqlalchemy import Column, ForeignKey, String
from app.models.users.professor import Professor


class PendingProfessor(Professor):
    __tablename__ = "pending_professor"
    
    id = Column(String(36), ForeignKey("professor.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "pending_professor"
    }