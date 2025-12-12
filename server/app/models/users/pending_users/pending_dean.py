"""
    Date written: 12/12/2025 at 11:51 AM
"""

from sqlalchemy import Column, ForeignKey, String
from app.models.users.dean import Dean


class PendingDean(Dean):
    __tablename__ = "pending_dean"
    
    id = Column(String(36), ForeignKey("dean.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "pending_dean"
    }