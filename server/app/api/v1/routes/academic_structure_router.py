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
    tags=["Only registrar and dean role are allowed for these APIs"]
)

@academic_structure_router.post("/register-department", response_model=RegisterDepartmentResponseSchema)
async def register_department(
    department: RegisterDepartmentRequestSchema,
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
    
    
@academic_structure_router.post("/register-program", response_model=List[RegisterProgramResponseSchema])
async def register_program(
    programs: List[RegisterProgramRequestSchema],
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


@academic_structure_router.post("/register-curriculum", response_model=RegisterCurriculumResponseSchema)
async def register_curriculum(
    curriculum: RegisterCurriculumRequestSchema,
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


@academic_structure_router.post("/register-course", response_model=List[RegisterCourseResponseSchema])
async def register_course(
    courses: List[RegisterCourseRequestSchema],
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
    

@academic_structure_router.post("/register-curriculum-course", response_model=List[RegisterCurriculumCourseResponseSchema])
async def register_curriculum_course(
    curriculum_courses: List[RegisterCurriculumCourseRequestSchema],
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
        Register course_offering one at a time (Registrar only).
        Status is PENDING at registration. 
        Must be update by registrar or dean.
    """
    service = AcademicStructureService(db)
    return await service.register_course_offering(
        course_offering=course_offering,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


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
    response_model=List[ProfessorClassSectionResponseSchema]
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
