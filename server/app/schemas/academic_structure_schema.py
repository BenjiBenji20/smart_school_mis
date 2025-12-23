"""
    Date Written: 12/22/2025 at 4:36 PM
"""

from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.generic_schema import GenericResponse

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
    