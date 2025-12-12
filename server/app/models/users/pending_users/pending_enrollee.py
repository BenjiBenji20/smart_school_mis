"""
    Date written: 12/10/2025 at 8:49 PM
"""

from sqlalchemy import Column, ForeignKey, String
from app.models.users.student import Student


class PendingEnrollee(Student):
    __tablename__ = "pending_enrollee"
    
    id = Column(String(36), ForeignKey("student.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "pending_enrollee"
    }