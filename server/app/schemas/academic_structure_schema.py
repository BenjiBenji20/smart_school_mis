"""
    Date Written: 12/22/2025 at 4:36 PM
"""

from pydantic import BaseModel, Field

from app.schemas.generic_schema import GenericResponse

class RegisterCourseRequestSchema(BaseModel):
    title: str = Field(..., max_length=100)
    course_code: str | None = None
    units: int
    description: str | None = None


class RegisterCourseResponseSchema(BaseModel):
    title: str
    course_code: str
    units: int
    description: str

    request_log: GenericResponse
    