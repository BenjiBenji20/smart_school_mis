"""
    Date Written: 1/4/2026 at 4:40 PM
"""

from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.role_checker import role_required
from app.models.enums.user_state import UserRole
from app.db.db_session import get_async_db
from app.middleware.current_user import get_current_user
from app.services.student_service import StudentService
from app.models.users.student import Student
from app.schemas.enrollments_and_gradings_schema import AllowedEnrollSectionResponseSchema, EnrollmentResponseSchema
from app.schemas.academic_structure_schema import TermResponseSchema
from app.schemas.user_schema import BaseUserResponseSchema, StudentResponseSchema
from app.models.users.base_user import BaseUser

student_router = APIRouter(
    prefix="/api/student",
    tags=["API for student user"]
)

@student_router.get("/get/current-student", response_model=StudentResponseSchema)
async def get_current_student(
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.STUDENT]))
):
    service = StudentService(db)
    return await service.get_current_student_user(current_user.id)


@student_router.get("/get/enrollments", response_model=List[AllowedEnrollSectionResponseSchema])
async def get_my_current_enrollments(
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.STUDENT]))
):
    service = StudentService(db)
    return await service.get_my_current_enrollments(
        student_id=current_user.id
    )


@student_router.get("/get/current-term", response_model=TermResponseSchema)
async def get_my_current_term(
    db: AsyncSession = Depends(get_async_db),
    current_user: Student = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.STUDENT]))
):
    """
        Get the current enrolled term of student
    """
    service = StudentService(db)
    return await service.get_my_current_term(
        student_id=current_user.id
    )


@student_router.get("/get/next-term", response_model=TermResponseSchema)
async def get_my_next_term(
    db: AsyncSession = Depends(get_async_db),
    current_user: Student = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.STUDENT, UserRole.DEAN, UserRole.PROGRAM_CHAIR]))
):
    """
        Get the next term of student that needed to be enrolled
    """
    service = StudentService(db)
    return await service.get_my_next_term(
        student_id=current_user.id
    )
    

@student_router.delete(
    "/del/remove-enrollment/{class_section_id}", response_model=List[AllowedEnrollSectionResponseSchema]
)
async def remove_enrollment(
    class_section_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.STUDENT]))
):
    """
        Remove enrolled section that doesn't yet approved
    """
    service = StudentService(db)
    return await service.remove_enrollment(
        student_id=current_user.id,
        class_section_id=class_section_id
    )
    