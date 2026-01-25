"""
    Date Written: 12/26/2025 at 4:14 PM
"""

from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_session import get_async_db
from app.middleware.current_user import get_current_user
from app.middleware.role_checker import role_required
from app.models.enums.user_state import UserRole
from app.models.users.base_user import BaseUser
from app.services.dean_service import DeanService
from app.schemas.user_schema import *
from app.schemas.generic_schema import GenericResponse


dean_router = APIRouter(
    prefix="/api/dean",
    tags=["dean APIs"]
)


@dean_router.get("/get/current-dean", response_model=DeanResponseSchema)
async def assign_department(
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.DEAN]))
):
    service = DeanService(db)
    return await service.get_current_dean_user(
        dean_id=current_user.id
    )
    
    
@dean_router.patch("/assign/{program_chair_id}/program_chair/{program_id}/program", response_model=GenericResponse)
async def assign_program(
    program_chair_id: str,
    program_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN]))
):
    service = DeanService(db)
    return await service.assign_program_chair_program(
        program_chair_id=program_chair_id,
        program_id=program_id,
        requested_by=current_user.first_name + " " + current_user.last_name
    )


@dean_router.get("/get/activate/program-chairs", response_model=List[ProgramChairResponseSchema])
async def get_active_program_chairs(
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN]))
):
    service = DeanService(db)
    return await service.get_active_program_chairs()
