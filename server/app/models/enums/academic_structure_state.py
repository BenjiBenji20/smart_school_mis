"""
    Date written: 12/23/2025 at 10:08 AM
"""

from enum import Enum


class CurriculumStatus(str, Enum):
    DRAFT = "Draft"
    ACTIVE = "Active"
    RETIRED = "Retired"
