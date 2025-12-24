"""
    Date written: 12/23/2025 at 10:08 AM
"""

from enum import Enum


class CurriculumStatus(str, Enum):
    DRAFT = "Draft"
    ACTIVE = "Active"
    RETIRED = "Retired"
    
    
class SemesterPeriod(str, Enum):
    FIRST = "FIRST"
    SECOND = "SECOND"
    SUMMER = "SUMMER"

    
class TermStatus(str, Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


class CourseOfferingStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    CANCELLED = "CANCELLED"
