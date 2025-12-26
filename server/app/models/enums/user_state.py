"""
    Date written: 12/7/2025 at 2:49 PM
"""

from enum import Enum

class UserRole(str, Enum):
    ADMINISTRATOR = "Administrator"
    REGISTRAR = "Registrar"
    DEAN = "Dean"
    PROGRAM_CHAIR = "Program Chair"
    PROFESSOR = "Professor"
    STUDENT = "Student"
    
    
class UserStatus(str, Enum):
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PENDING = "Pending"
    
    
class UserGender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    
    
class ProfessorStatus(str, Enum):
    ACTIVE = "ACTIVE"
    NOT_ACTIVE = "NOT_ACTIVE"
    SUSPENDED = "SUSPENDED"
    ON_LEAVE = "ON_LEAVE"
    