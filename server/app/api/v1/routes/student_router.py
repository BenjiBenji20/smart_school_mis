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
from app.schemas.enrollments_and_gradings_schema import EnrollmentResponseSchema

student_router = APIRouter(
    prefix="/api/student",
    tags=["API for student user"]
)


@student_router.get("/get/enrollments", response_model=List[EnrollmentResponseSchema])
async def get_my_current_enrollments(
    db: AsyncSession = Depends(get_async_db),
    current_user: Student = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.STUDENT]))
):
    service = StudentService(db)
    return await service.get_my_current_enrollments(
        student_id=current_user.id
    )
