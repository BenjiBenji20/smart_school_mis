"""
    Date written: 12/23/2025 at 10:08 AM
"""

from enum import Enum

# class DepartmentSelection(str, Enum):
#     CCS = "College of Computer Studies"
#     CBA = "College of Business Accountancy"
#     CRIM = "Criminology na may Motor Lang"


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


class ClassSectionStatus(str, Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    CANCELLED = "CANCELLED"
    
    
class EnrollmentStatus(str, Enum):
    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    CANCELLED = "CANCELLED"
