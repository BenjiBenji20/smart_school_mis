"""
    Date Written: 12/28/2025 at 9:00 AM
"""

from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.role_checker import role_required
from app.models.enums.user_state import UserRole
from app.models.users.registrar import Registrar
from app.schemas.academic_structure_schema import *
from app.schemas.enrollments_and_gradings_schema import *
from app.db.db_session import get_async_db
from app.middleware.current_user import get_current_user
from app.services.enrollment_grading_service import EnrollmentGradingService
from app.models.users.student import Student

enrollment_grading_router = APIRouter(
    prefix="/api/enrollment",
    tags=["Enrollment API for Student and Registrar Role only"]
)


@enrollment_grading_router.get("/allowed-sections", response_model=List[ClassSectionResponseSchema])
async def get_allowed_section(
    current_user: Student = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN, UserRole.PROGRAM_CHAIR, UserRole.STUDENT]))
):
    """
        Read all the allowed sections to enroll by the student.
        Class Sections must be of these followings:
        - Courses must be under the student's program
        - Courses must be isn't taken by the student [not sure about this]
    """
    service = EnrollmentGradingService(db)
    return await service.get_student_allowed_sections(
        student_id=current_user.id,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@enrollment_grading_router.post(
    "/student/{student_id}/class_section/{class_section_id}", 
    response_model=EnrollmentResponseSchema
)
async def enroll_student_class_section(
    student_id: str,
    class_section_id: str,
    current_user: Student = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([
        UserRole.REGISTRAR, UserRole.DEAN, 
        UserRole.PROGRAM_CHAIR, UserRole.STUDENT
    ]))
):
    """
        Student enrollment.
        Validations:
            Term.status == OPEN
            ClassSection.status == OPEN
            Section not full
            Student not already enrolled
            Curriculum compatibility
            CourseOffering.status == APPROVED

    """
    service = EnrollmentGradingService(db)
    return await service.enroll_student_class_section(
        student_id=student_id,
        class_section_id=class_section_id,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@enrollment_grading_router.get("/get-enrollments", response_model=List[EnrollmentResponseSchema])
async def get_all_enrollments(
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Read all student enrollment (Registrar role only)
    """
    service = EnrollmentGradingService(db)
    return await service.get_all_enrollments()
    
    
@enrollment_grading_router.get(
    "/filter", 
    response_model=List[EnrollmentResponseSchema]
)
async def get_all_enrollments(
    department_id: str = None,
    program_id: str = None,
    class_section_id: str = None,
    term_id: str = None,
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Read all student enrollment (Registrar role only)
    """
    service = EnrollmentGradingService(db)
    return await service.get_filtered_enrollments(
        department_id=department_id,
        program_id=program_id,
        class_section_id=class_section_id,
        term_id=term_id
    )


@enrollment_grading_router.patch("/status", response_model=List[EnrollmentResponseSchema])
async def update_enrollment_status(
    enrollments: UpdateEnrollmentStatusSchema,
    db: AsyncSession = Depends(get_async_db),
    current_user: Registrar = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    """
        Update multiple enrollments (registrar role only)
            All the enrollment (through id) will be updated using 1 status
    """
    service = EnrollmentGradingService(db)
    return await service.update_enrollment_status(
        enrollments=enrollments,
        requested_by=current_user.first_name + " " + current_user.last_name
    )
    

@enrollment_grading_router.get("/list/status/{enrollment_status}", response_model=List[EnrollmentResponseSchema])
async def list_enrollment_by_status(
    enrollment_status: EnrollmentStatus,
    db: AsyncSession = Depends(get_async_db),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    service = EnrollmentGradingService(db)
    return await service.list_enrollment_by_status(
        enrollment_status=enrollment_status
    )
    