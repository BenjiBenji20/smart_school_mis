"""
    Date written: 12/12/2025 at 11:51 AM
"""

from sqlalchemy import Column, ForeignKey, String
from app.models.users.registrar import Registrar


class PendingRegistrar(Registrar):
    __tablename__ = "pending_registrar"
    
    id = Column(String(36), ForeignKey("registrar.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "pending_registrar"
    }