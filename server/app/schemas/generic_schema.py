"""
    Date Written: 12/21/2025 at 2:13 PM
"""

from pydantic import BaseModel
from datetime import datetime

class GenericResponse(BaseModel):
    """
        To format response for generic requests:
            - approving user
            - CRUD operation
    """
    success: bool
    requested_at: datetime
    requested_by: str | None = None

    class Config: 
        from_attributes = True

