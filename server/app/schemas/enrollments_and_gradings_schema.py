"""
    Date Written: 12/28/2025 at 3:39 PM
"""

from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from app.schemas.generic_schema import GenericResponse
from app.models.enums.academic_structure_state import *
from app.models.enums.enrollment_and_grading_state import EnrollmentStatus

class UpdateEnrollmentStatusSchema(BaseModel):
    status: EnrollmentStatus
    enrollment_ids: List[str]


class EnrollmentResponseSchema(BaseModel):
    enrollment_id: str
    student_id: str
    class_section_id: str
    term_id: str
    program_id: str
    enrollment_status: EnrollmentStatus
    section_code: str
    course_code: str
    title: str
    units: int
    day_of_week: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    room_code: Optional[str] = None
    semester_period: SemesterPeriod
    academic_year_start: int
    academic_year_end: int
    program_code: Optional[str] = None
    student_name: Optional[str] = None
    assigned_professor: Optional[str] = None
    request_log: Optional[GenericResponse] = None
    
    class Config:
        from_attributes = True
        
        
class SemesterTermResponseSchema(BaseModel):
    """For term based on semester period"""
    id: str
    created_at: datetime
    academic_year_start: int = Field(gt=1999, lt=3001)  # e.g. 2025
    academic_year_end: int = Field(gt=1999, lt=3001) # e.g. 2026
    enrollment_start: datetime
    enrollment_end: datetime
    semester_period: SemesterPeriod # FIRST | SECOND | SUMMER
    status: TermStatus # DRAFT | OPEN | CLOSED | ARCHIVED
    request_log: Optional[GenericResponse] = None
    
    class Config:
        from_attributes= True
        

class AllowedEnrollSectionResponseSchema(BaseModel):
    class_section_id: str
    course_code: str
    title: str
    units: int
    section_code: str
    day_of_week: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    room_code: Optional[str] = None
    assigned_professor: Optional[str] = None
    
    class Config:
        from_attributes = True
    