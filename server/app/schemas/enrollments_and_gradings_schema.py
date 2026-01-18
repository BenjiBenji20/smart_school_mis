"""
    Date Written: 12/28/2025 at 3:39 PM
"""

from typing import List
from pydantic import BaseModel

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
    