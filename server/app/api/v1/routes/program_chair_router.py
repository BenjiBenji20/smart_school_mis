"""
    Date Written: 12/26/2025 at 4:24 PM
"""

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_session import get_async_db
from app.middleware.current_user import get_current_user
from app.middleware.role_checker import role_required
from app.models.enums.user_state import UserRole
from app.models.users.base_user import BaseUser
from app.schemas.generic_schema import GenericResponse
from app.services.program_chair_service import ProgramChairService


program_chair_router = APIRouter(
    prefix="/api/program_chair",
    tags=["program_chair APIs"]
)


@program_chair_router.patch("/assign/{program_chair_id}/program_chair/{program_id}/program", response_model=GenericResponse)
async def assign_program(
    program_chair_id: str,
    program_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR, UserRole.DEAN]))
):
    service = ProgramChairService(db)
    return await service.assign_program_chair_program(
        program_chair_id=program_chair_id,
        program_id=program_id,
        requested_by=current_user.first_name + " " + current_user.last_name
    )
