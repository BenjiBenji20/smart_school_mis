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
    tags=["Only registrar role is allowed for these APIs"]
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
    
