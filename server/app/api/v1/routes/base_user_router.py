"""
    Date Written: 12/20/2025 at 5:20 PM
"""

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from app.schemas.generic_schema import GenericResponse
from app.db.db_session import get_async_db
from app.middleware.role_checker import role_required
from app.models.enums.user_state import UserRole
from app.models.users.base_user import BaseUser
from app.middleware.current_user import get_current_user
from app.services.auth_service import AuthService
from app.schemas.base_user_schema import CredentialValidatorSchema
from app.exceptions.customed_exception import InvalidRequestException
from app.services.base_user_service import BaseUserService

base_user_router = APIRouter(
    prefix="/api/base-user", 
    tags=["Routes for general user access"]
)


@base_user_router.post("/approve-registration", response_model=GenericResponse)
async def approve_registration(
    id: str,
    user_role: UserRole,
    user_credential: CredentialValidatorSchema,
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user),
    allowed_roles = Depends(role_required([
        UserRole.ADMINISTRATOR, UserRole.REGISTRAR,
        UserRole.DEAN, UserRole.PROGRAM_CHAIR
    ]))
):
    # validate user action
    auth_service = AuthService(db)
    is_password_matched = auth_service.validate_password(
        plain_password=user_credential.password,
        hashed_password=current_user.password_hash
    )
    
    if not is_password_matched or user_credential.email != current_user.email:
        raise InvalidRequestException("Credentials not matched.")
    
    base_user_service = BaseUserService(db)
    
    result = await base_user_service.approve_user(
        approved_by=current_user.first_name + " " + current_user.last_name,
        approver_role=current_user.role,
        target_role=user_role,
        id=id
    )
    
    return result
