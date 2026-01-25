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
from app.services.program_chair_service import ProgramChairService
from app.schemas.user_schema import ProgramChairResponseSchema


program_chair_router = APIRouter(
    prefix="/api/program_chair",
    tags=["program_chair APIs"]
)

@program_chair_router.get("/get/current-program-chair", response_model=ProgramChairResponseSchema)
async def get_current_program_chair(
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.PROGRAM_CHAIR]))
):
    service = ProgramChairService(db)
    return await service.get_current_program_chair_user(
        program_chair_id=current_user.id
    )