"""
    Date Written: 12/22/2025 at 4:36 PM
"""

from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.generic_schema import GenericResponse
from app.models.enums.academic_structure_state import CurriculumStatus

# ==============================================
# DEPARTMENT SCHEMAS
# ==============================================
class RegisterDepartmentRequestSchema(BaseModel):
    title: str = Field(..., max_length=100)
    department_code: str | None = None
    description: str | None = None


class RegisterDepartmentResponseSchema(BaseModel):
    id: str
    created_at: datetime
    title: str
    department_code: str
    description: str

    request_log: GenericResponse
    

# ==============================================
# PROGRAM SCHEMAS
# ==============================================
class RegisterProgramRequestSchema(BaseModel):
    title: str = Field(..., max_length=100)
    program_code: str | None = None
    description: str | None = None
    department_id: str | None = None


class RegisterProgramResponseSchema(BaseModel):
    id: str
    created_at: datetime
    title: str
    program_code: str
    description: str
    
    department_id: str

    request_log: GenericResponse


# ==============================================
# CURRICULUM SCHEMAS
# ==============================================
class RegisterCurriculumRequestSchema(BaseModel):
    title: str = Field(..., max_length=100)
    effective_from: int
    effective_to: int | None = None
    status: CurriculumStatus
    program_id: str = Field(..., max_length=36)
    
    
class RegisterCurriculumResponseSchema(BaseModel):
    id: str
    created_at: datetime
    title: str
    effective_from: int
    effective_to: int
    status: CurriculumStatus
    program_id: str
        
    request_log: GenericResponse


# ==============================================
# COURSE SCHEMAS
# ==============================================
class RegisterCourseRequestSchema(BaseModel):
    title: str = Field(..., max_length=100)
    course_code: str | None = None
    units: int
    description: str | None = None


class RegisterCourseResponseSchema(BaseModel):
    id: str
    created_at: datetime
    title: str
    course_code: str
    units: int
    description: str

    request_log: GenericResponse
    
    
# ==============================================
# CURRICULUMCOURSE SCHEMAS
# ==============================================    
class RegisterCurriculumCourseRequestSchema(BaseModel):
    year_level: int
    semester: int
    is_required: bool
    curriculum_id: str = Field(..., max_length=36)
    course_id: str = Field(..., max_length=36)
    
    
class RegisterCurriculumCourseResponseSchema(BaseModel):
    id: str
    created_at: datetime
    year_level: int
    semester: int
    is_required: bool
    curriculum_id: str
    course_id: str
    
    request_log: GenericResponse
    