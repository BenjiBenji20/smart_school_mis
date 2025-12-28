"""
    Date written: 12/28/2025 at 3:00 PM
"""

from enum import Enum

class EnrollmentStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    