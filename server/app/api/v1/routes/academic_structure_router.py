"""
    Date Written: 12/22/2025 at 4:32 PM
"""

from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.role_checker import role_required
from app.models.enums.user_state import UserRole
from app.models.users.registrar import Registrar
from app.schemas.academic_structure_schema import *
from app.db.db_session import get_async_db
from app.middleware.current_user import get_current_user
from app.services.academic_structure_service import AcademicStructureService


academic_structure_router = APIRouter(
    prefix="/api/academic-structure",
    tags=["API's for interacting with academic structure"]
)

@academic_structure_router.post("/register-building", response_model=BuildingResponseSchema)
async def register_building(
    building: BuildingRequestSchema,
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.ADMINISTRATOR]))
):
    """
        Register building (administrator role)
        param building: 
            name: str (building name)
            room_capacity: int (number of rooms)
    """
    service = AcademicStructureService(db)
    return await service.register_building(
        building=building,
        requested_by=current_user.first_name + " " + current_user.last_name
    )
    
    
@academic_structure_router.get("/list-buildings", response_model=List[BuildingResponseSchema])
async def list_buildings(
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.ADMINISTRATOR]))
):
    service = AcademicStructureService(db)
    return await service.list_buildings()
    
    
@academic_structure_router.post("/register-room", response_model=List[RoomResponseSchema])
async def register_room(
    rooms: List[RoomRequestSchema],
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.ADMINISTRATOR]))
):
    """
        Register room (administrator role)
        param room: 
            room_code: str (room name)
            capacity: int (number of students)
    """
    service = AcademicStructureService(db)
    return await service.register_room(
        rooms=rooms,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@academic_structure_router.get("/list-rooms/building/{building_id}", response_model=List[RoomResponseSchema])
async def list_rooms_by_building(
    building_id: str,
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.ADMINISTRATOR]))
):
    service = AcademicStructureService(db)
    return await service.list_rooms_by_building(building_id)


@academic_structure_router.post("/register-department", response_model=DepartmentResponseSchema)
async def register_department(
    department: DepartmentRequestSchema,
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Register one department at a time (Registrar only)
    """
    service = AcademicStructureService(db)
    return await service.register_department(
        department=department,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@academic_structure_router.get("/list-departments", response_model=List[DepartmentResponseSchema])
async def list_departments(
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    service = AcademicStructureService(db)
    return await service.list_departments()

    
@academic_structure_router.patch(
    "/department/{department_id}/building/{building_id}", 
    response_model=GenericResponse
)
async def register_department_building(
    department_id: str,
    building_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.ADMINISTRATOR]))
):
    """
        Register department to building (administrator role)

        Building <-> Department
        - Department must not have been registered to other building
    """
    service = AcademicStructureService(db)
    return await service.assign_department_building(
        department_id=department_id,
        building_id=building_id,
        requested_by=current_user.first_name + " " + current_user.last_name
    )
    
    
@academic_structure_router.post("/register-program", response_model=List[ProgramResponseSchema])
async def register_program(
    programs: List[ProgramRequestSchema],
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Register one or multiple programs (Registrar only)
    """
    service = AcademicStructureService(db)
    return await service.register_program(
        programs=programs,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@academic_structure_router.get(
    "/list-programs/department/{department_id}", 
    response_model=List[ProgramResponseSchema]
)
async def list_programs_by_department(
    department_id: str,
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN]))
):
    service = AcademicStructureService(db)
    return await service.list_programs_by_department(department_id)


@academic_structure_router.post("/register-curriculum", response_model=CurriculumResponseSchema)
async def register_curriculum(
    curriculum: CurriculumRequestSchema,
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Register curriculum one at a time (Registrar only)
    """
    service = AcademicStructureService(db)
    return await service.register_curriculum(
        curriculum=curriculum,
        requested_by=current_user.first_name + " " + current_user.last_name
    )
    
    
@academic_structure_router.get(
    "/list-curriculums/program/{program_id}", 
    response_model=List[CurriculumResponseSchema]
)
async def list_curriculums_by_program(
    program_id: str,
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN]))
):
    service = AcademicStructureService(db)
    return await service.list_curriculums_by_program(program_id)

    
@academic_structure_router.patch("/curriculum/{id}/status/{status}", response_model=GenericResponse)
async def update_curriculum_status(
    id: str,
    status: CurriculumStatus,
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Update curriculum status allowed only for registrar role.
        Curriculum has default DRAFT status when its first created.
        registrar must update it according to status needed.
    """
    service = AcademicStructureService(db)
    return await service.update_curriculum_status(
        id=id,
        status=status,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@academic_structure_router.post("/register-course", response_model=List[CourseResponseSchema])
async def register_course(
    courses: List[CourseRequestSchema],
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Register one or multiple courses (Registrar only)
    """
    service = AcademicStructureService(db)
    return await service.register_course(
        courses=courses,
        requested_by=current_user.first_name + " " + current_user.last_name
    )
    

@academic_structure_router.get("/list-courses", response_model=List[CourseResponseSchema])    
async def list_courses(
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN]))
):
    service = AcademicStructureService(db)
    return await service.list_courses()


@academic_structure_router.post("/register-curriculum-course", response_model=List[CurriculumCourseResponseSchema])
async def register_curriculum_course(
    curriculum_courses: List[CurriculumCourseRequestSchema],
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Register one or multiple curriculum courses (Registrar only)
    """
    service = AcademicStructureService(db)
    return await service.register_curriculum_course(
        curriculum_courses=curriculum_courses,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@academic_structure_router.get(
    "/list-curriculum-courses/curriculum/{curriculum_id}/year_level/{year_level}/semester/{semester}",
    response_model=List[CurriculumCourseResponseSchema]
)
async def list_curriculum_course_by_field(
    curriculum_id: str = None,
    year_level: int = None,
    semester: int = None,
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    service = AcademicStructureService(db)
    return await service.list_curriculum_course_by_field(
        curriculum_id=curriculum_id,
        year_level=year_level,
        semester=semester
    )


@academic_structure_router.post("/register-term", response_model=List[TermResponseSchema])
async def register_term(
    terms: List[TermRequestSchema],
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Create term
        default term status is DRAFT
        default term academic_period is FIRST
    """
    service = AcademicStructureService(db)
    return await service.register_term(
        terms=terms,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@academic_structure_router.patch("/term/{id}/status/{status}", response_model=GenericResponse)
async def update_term_status(
    id: str,
    status: TermStatus,
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Update term status allowed only for registrar role.
        term has default DRAFT status when its first created.
        registrar must update it according to status needed.
    """
    service = AcademicStructureService(db)
    return await service.update_term_status(
        id=id,
        status=status,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@academic_structure_router.get("/term/active-year", response_model=List[TermResponseSchema])
async def get_active_year_term(
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Get active terms.
        Terms that has status of OPEN and within or in the current 
        academic_year_start and academic_year_end.
    """
    service = AcademicStructureService(db)
    return await service.get_active_year_term(
        requested_by=current_user.first_name + " " + current_user.last_name
    )
    

@academic_structure_router.get("/term/active-enrollment", response_model=List[TermResponseSchema])
async def get_active_enrollment(
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Get active enrollments.
        Enrollments that has status of OPEN and within or in the current 
        enrollment_start and enrollment_end.
    """
    service = AcademicStructureService(db)
    return await service.get_active_enrollment(
        requested_by=current_user.first_name + " " + current_user.last_name
    )

    
@academic_structure_router.post("/register-course-offering", response_model=CourseOfferingResponseSchema)
async def register_course_offering(
    course_offering: CourseOfferingRequestSchema,
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
         course_offering one at a time (Registrar only).
        Status is PENDING at registration. 
        Must be update by registrar or dean.
    """
    service = AcademicStructureService(db)
    return await service.register_course_offering(
        course_offering=course_offering,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@academic_structure_router.get("/list-course-offerings/term/{term_id}", response_model=List[CourseOfferingResponseSchema])
async def list_course_offering_by_term(
    term_id: str,
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN]))
):
    service = AcademicStructureService(db)
    return await service.list_course_offering_by_term(term_id)


@academic_structure_router.patch("/course-offering/{id}/status/{status}", response_model=GenericResponse)
async def update_term_status(
    id: str,
    status: CourseOfferingStatus,
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN]))
):
    """
        Manage course offering status allowed only for registrar and dean role.
        Course offering has default PENDING status when its first registered.
        registrar or dean must update it according to status needed.
        
        param: id: for the target course_offering db record to update
        param: status: the status to be switch by the CourseOfferingStatus
    """
    service = AcademicStructureService(db)
    return await service.update_course_offering_status(
        id=id,
        status=status,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@academic_structure_router.post("/register/class-section", response_model=List[ClassSectionResponseSchema])
async def register_class_section(
    class_sections: List[ClassSectionRequestSchema],
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN, UserRole.PROGRAM_CHAIR]))
):
    """
        Register one or multiple class section at the same time.
    """
    service = AcademicStructureService(db)
    return await service.register_class_section(
        class_sections=class_sections,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@academic_structure_router.post(
    "/assign/professor/class-section",
    response_model=List[ProfessorClassSectionFormattedResponseSchema]
)
async def assign_class_section_professor(
    request: ProfessorClassSectionRequestSchema,
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN, UserRole.PROGRAM_CHAIR]))
):
    """
        Register one professor to multiple class section at the same request
        Assign professor to multiple class sections
            - Professor must be ACTIVE
            - No duplicate assignment (handled by UniqueConstraint)
    """
    service = AcademicStructureService(db)
    return await service.assign_class_section_professor(
        prof_id=request.prof_id,
        class_section_ids=request.class_section_ids,
        requested_by=current_user.first_name + " " + current_user.last_name
    ) 


@academic_structure_router.post(
    "/assign/schedule/class-section",
    response_model=ClassScheduleResponseSchema
)
async def assign_schedule_class_section(
    class_schedule: ClassScheduleRequestSchema,
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN, UserRole.PROGRAM_CHAIR]))
):
    """
        Assign a schedule to class section.
        Following these validation and constraints:
            - Validate time logic (start < end)
            - Validate room conflict
            - Validate professor conflict
            - Persist schedule
    """
    service = AcademicStructureService(db)
    return await service.assign_schedule_class_section(
        class_schedule=class_schedule,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@academic_structure_router.get(
    "/list-class-schedules/class-section/{class_section_id}",
    response_model=List[ClassScheduleResponseSchema]
)
async def list_class_schedule_by_section(
    class_section_id: str,
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN]))
):
    service = AcademicStructureService(db)
    return await service.list_class_schedule_by_section(
        class_section_id
    )
