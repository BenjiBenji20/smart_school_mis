"""
    Date Written: 12/22/2025 at 4:36 PM
"""

from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

from app.schemas.generic_schema import GenericResponse
from app.models.enums.academic_structure_state import *
from app.models.enums.user_state import ProfessorStatus

# ==============================================
# BUILDING SCHEMAS
# ==============================================
class RegisterBuildingRequestSchema(BaseModel):
    name: str = Field(..., max_length=100)
    room_capacity: int
    

class RegisterBuildingResponseSchema(BaseModel):
    id: str
    created_at: datetime
    name: str
    room_capacity: int
    
    request_log: GenericResponse
    

# ==============================================
# BUILDING SCHEMAS
# ==============================================
class RegisterRoomRequestSchema(BaseModel):
    room_code: str | None = Field(default=None, max_length=10)
    section_capacity: int # section capacity MAX 10

    # foreign keys
    building_id: str = Field(..., max_length=36)
    

class RegisterRoomResponseSchema(BaseModel):
    id: str
    created_at: datetime
    building_id: str
    room_code: str | None = None
    section_capacity: int
    
    request_log: GenericResponse


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
    department_code: str | None = None
    description: str | None = None

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
    program_code: str | None = None
    description: str | None = None
    
    department_id: str | None = None

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
    effective_to: int | None = None
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
    course_code: str | None = None
    units: int
    description: str | None = None

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
     
     
# ==============================================
# TERM SCHEMAS
# ==============================================  
class TermRequestSchema(BaseModel):
    # Enforces a 4-digit positive integer (2000 to 3000)
    academic_year_start: int = Field(gt=1999, lt=3001) 
    academic_year_end: int = Field(gt=1999, lt=3001)
    enrollment_start: datetime
    enrollment_end: datetime

    semester_period: SemesterPeriod
    status: TermStatus = TermStatus.DRAFT
    
    
class TermResponseSchema(BaseModel):
    id: str
    created_at: datetime
    academic_year_start: int 
    academic_year_end: int
    enrollment_start: datetime
    enrollment_end: datetime

    semester_period: SemesterPeriod
    status: TermStatus
    
    request_log: GenericResponse


# ==============================================
# CourseOffering SCHEMAS
# ==============================================  
class CourseOfferingRequestSchema(BaseModel):
    term_id: str = Field(..., max_length=36)
    curriculum_course_id: str = Field(..., max_length=36)
    status: CourseOfferingStatus = CourseOfferingStatus.PENDING
    
    
class CourseOfferingResponseSchema(BaseModel):
    id: str
    created_at: datetime
    term_id: str
    curriculum_course_id: str
    status: CourseOfferingStatus
    
    request_log: GenericResponse
    
    
# ==============================================
# CLASSSECTION SCHEMAS
# ==============================================  
class ClassSectionRequestSchema(BaseModel):
    course_offering_id: str = Field(..., max_length=36)
    room_id: str | None = Field(default=None, max_length=36)
    section_code: str = Field(..., max_length=10)
    student_capacity: int = Field(gt=0) 
    time_schedule: str | None = None
    status: ClassSectionStatus = ClassSectionStatus.CLOSE
    
    
class ClassSectionResponseSchema(BaseModel):
    id: str
    created_at: datetime
    course_offering_id: str
    room_id: str | None = None
    section_code: str
    student_capacity: int
    time_schedule: str | None = None
    status: ClassSectionStatus
    
    request_log: GenericResponse
    
    
# ==============================================
# CLASSSECTION_PROFESSOR SCHEMAS
# ==============================================
class ProfessorClassSectionRequestSchema(BaseModel):
    prof_id: str
    class_section_ids: List[str]

class ProfessorClassSectionResponseSchema(BaseModel):
    id: str
    created_at: datetime
    course_offering_id: str
    
    professor_id: str
    professor_status: ProfessorStatus
    first_name: str
    middle_name: str | None = None
    last_name: str
    suffix: str | None = None
    university_code: str
    
    class_section_id: str
    section_code: str
    room_number: int | None = None
    student_capacity: int
    time_schedule: str | None = None
    class_section_status: ClassSectionStatus
    
    request_log: GenericResponse
    