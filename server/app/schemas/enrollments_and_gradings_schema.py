"""
    Date Written: 12/28/2025 at 3:39 PM
"""

from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from app.schemas.generic_schema import GenericResponse
from app.models.enums.academic_structure_state import *
from app.schemas.base_user_schema import StudentResponseSchema
from app.models.enums.enrollment_and_grading_state import EnrollmentStatus
from app.schemas.academic_structure_schema import ClassSectionResponseSchema, TermResponseSchema

class UpdateEnrollmentStatusSchema(BaseModel):
    status: EnrollmentStatus
    enrollment_ids: List[str]


class EnrollmentResponseSchema(BaseModel):
    status: EnrollmentStatus
    student: StudentResponseSchema
    class_section_details: ClassSectionResponseSchema
    term: TermResponseSchema

    request_log: GenericResponse | None = None


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
    