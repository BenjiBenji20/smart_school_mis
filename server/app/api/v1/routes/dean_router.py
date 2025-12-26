"""
    Date Written: 12/26/2025 at 4:14 PM
"""

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_session import get_async_db
from app.middleware.current_user import get_current_user
from app.middleware.role_checker import role_required
from app.models.enums.user_state import UserRole
from app.models.users.base_user import BaseUser
from app.schemas.generic_schema import GenericResponse
from app.services.dean_service import DeanService


dean_router = APIRouter(
    prefix="/api/dean",
    tags=["dean APIs"]
)


@dean_router.patch("/assign/{dean_id}/dean/{department_id}/department", response_model=GenericResponse)
async def assign_department(
    dean_id: str,
    department_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user),
    allowed_roles = Depends(role_required([UserRole.REGISTRAR]))
):
    service = DeanService(db)
    return await service.assign_dean_department(
        dean_id=dean_id,
        department_id=department_id,
        requested_by=current_user.first_name + " " + current_user.last_name
    )
