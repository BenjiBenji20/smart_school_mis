"""
    Date Written: 12/22/2025 at 4:36 PM
"""

from datetime import datetime, time
from typing import List
from pydantic import BaseModel, Field, field_validator

from app.schemas.generic_schema import GenericResponse
from app.models.enums.academic_structure_state import *
from app.models.enums.user_state import ProfessorStatus
from app.schemas.user_schema import BaseUserResponseSchema, StudentResponseSchema
from app.models.enums.enrollment_and_grading_state import EnrollmentStatus

# ==============================================
# BUILDING SCHEMAS
# ==============================================
class BuildingRequestSchema(BaseModel):
    name: str = Field(..., max_length=100)
    room_capacity: int
    

class BuildingResponseSchema(BaseModel):
    id: str
    created_at: datetime
    name: str
    room_capacity: int
    
    request_log: GenericResponse | None = None
    

# ==============================================
# BUILDING SCHEMAS
# ==============================================
class RoomRequestSchema(BaseModel):
    room_code: str | None = Field(default=None, max_length=10)
    # section_capacity: int # section capacity MAX 10

    # foreign keys
    building_id: str = Field(..., max_length=36)
    

class RoomResponseSchema(BaseModel):
    id: str
    created_at: datetime
    room_code: str | None = None
    building_details: BuildingResponseSchema
    
    request_log: GenericResponse | None = None


# ==============================================
# DEPARTMENT SCHEMAS
# ==============================================
class DepartmentRequestSchema(BaseModel):
    title: str = Field(..., max_length=100)
    department_code: str | None = None
    description: str | None = None


class DepartmentResponseSchema(BaseModel):
    id: str
    created_at: datetime
    title: str
    department_code: str | None = None
    description: str | None = None

    request_log: GenericResponse | None = None
    

# ==============================================
# PROGRAM SCHEMAS
# ==============================================
class ProgramRequestSchema(BaseModel):
    title: str = Field(..., max_length=100)
    program_code: str | None = None
    description: str | None = None
    department_id: str | None = None


class ProgramResponseSchema(BaseModel):
    id: str
    created_at: datetime
    title: str
    program_code: str | None = None
    description: str | None = None
    
    department_details: DepartmentResponseSchema | None = None

    request_log: GenericResponse | None = None


# ==============================================
# CURRICULUM SCHEMAS
# ==============================================
class CurriculumRequestSchema(BaseModel):
    title: str = Field(..., max_length=100)
    effective_from: int
    effective_to: int | None = None
    status: CurriculumStatus
    program_id: str = Field(..., max_length=36)
    
    
class CurriculumResponseSchema(BaseModel):
    id: str
    created_at: datetime
    title: str
    effective_from: int
    effective_to: int | None = None
    status: CurriculumStatus
    program_details: ProgramResponseSchema | None = None
        
    request_log: GenericResponse | None = None


# ==============================================
# COURSE SCHEMAS
# ==============================================
class CourseRequestSchema(BaseModel):
    title: str = Field(..., max_length=100)
    course_code: str | None = None
    units: int
    description: str | None = None


class CourseResponseSchema(BaseModel):
    id: str
    created_at: datetime
    title: str
    course_code: str | None = None
    units: int
    description: str | None = None

    request_log: GenericResponse | None = None
    
    
# ==============================================
# CURRICULUMCOURSE SCHEMAS
# ==============================================    
class CurriculumCourseRequestSchema(BaseModel):
    year_level: int
    semester: int
    is_required: bool
    curriculum_id: str = Field(..., max_length=36)
    course_id: str = Field(..., max_length=36)
    
    
class CurriculumCourseResponseSchema(BaseModel):
    id: str
    created_at: datetime
    is_required: bool
    curriculum_details: CurriculumResponseSchema
    course_details: CourseResponseSchema
    
    request_log: GenericResponse | None = None
     
     
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
    
    request_log: GenericResponse | None = None


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
    term_details: TermResponseSchema
    curriculum_course_details: CurriculumCourseResponseSchema
    status: CourseOfferingStatus
    
    request_log: GenericResponse | None = None
    
    
# ==============================================
# CLASSSECTION SCHEMAS
# ==============================================  
class ClassSectionRequestSchema(BaseModel):
    course_offering_id: str = Field(..., max_length=36)
    section_code: str = Field(..., max_length=10)
    student_capacity: int = Field(gt=0) 
    status: ClassSectionStatus = ClassSectionStatus.CLOSE
    
    
class ClassSectionResponseSchema(BaseModel):
    id: str
    created_at: datetime
    section_code: str
    student_capacity: int
    current_student_cnt: int
    status: ClassSectionStatus
    course_offering_details: CourseOfferingResponseSchema
    
    request_log: GenericResponse | None = None
    
    
# ==============================================
# CLASSSECTION_PROFESSOR SCHEMAS
# ==============================================
class ProfessorClassSectionRequestSchema(BaseModel):
    prof_id: str = Field(..., max_length=36)
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
    
    request_log: GenericResponse | None = None
    
    
class ProfessorClassSectionFormattedResponseSchema(BaseModel):
    id: str
    created_at: datetime
    professor_details: BaseUserResponseSchema
    professor_status: ProfessorStatus
    university_code: str | None = None
    course_offering_details: CourseOfferingResponseSchema
    class_section_details: ClassSectionResponseSchema
    
    request_log: GenericResponse | None = None
    
    
# ==============================================
# CLASSSCHEDULE SCHEMAS
# ==============================================    
class ClassScheduleRequestSchema(BaseModel):
    class_section_id: str = Field(..., max_length=36)
    room_id: str = Field(..., max_length=36)
    day_of_week: int  # 1=Mon, 7=Sun
    # day of week must not less than 1 (monday) or greater than 7 (sunday)
    @field_validator("day_of_week")
    @classmethod
    def validate_day_of_week(key, value):
        if value > 7 or value < 1:
            raise ValueError(f"Invalid day schedule: {value}")
        return value
    
    start_time: time
    end_time: time

class ClassScheduleResponseSchema(BaseModel):
    id: str
    created_at: datetime
    
    day_of_week: int 
    start_time: time
    end_time: time
    class_section_details: ClassSectionResponseSchema
    room_details: RoomResponseSchema
    
    request_log: GenericResponse | None = None
    