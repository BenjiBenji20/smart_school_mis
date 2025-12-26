"""
    Date Written: 12/21/2025 at 1:49 PM
"""

from datetime import datetime
from typing import Optional
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_session import get_async_db
from app.models.enums.user_state import UserRole
from app.repository.auth_repository import AuthRepository
from app.utils.approval_matrix import can_approve
from app.exceptions.customed_exception import UnauthorizedAccessException
from app.models.users.base_user import BaseUser

class BaseUserService:
    def __init__(self, db: AsyncSession = Depends(get_async_db)):
        self.db = db
        
        self.auth_repo = AuthRepository(db)
        
        
    async def approve_user(
        self, 
        approved_by: str, 
        user_role: Optional[UserRole],
        approver_role: UserRole, 
        id: str
    ) -> dict:
        """
            Administrator role can only approved: administrator and registrar
            Registrar role can only approved:  registrar, dean, program_chair, professor and student
            Dean role can only approved:  program_chair, professor and student
            ProgramChair role can only approved: professor and student
            
            :param approved_by: by whome the user approved
            :type approved_by: str
            :param role: the role of user to be approved
            :type enum UserRole: 
            :param id: the user to be approved
            :type id: str
            :return: to flag wheather the user is successfully approved
            :rtype: bool
        """
        user = await self.auth_repo.get_by_id(id)
        role = user_role if user_role else user.role
        
        if not can_approve(approver_role, role):
            raise UnauthorizedAccessException(
                f"{approver_role.value} cannot approve {role}"
            )
        
        await self.auth_repo.approve_pending_registration(
            approved_by, role, id
        )
        
        return {
            "success": True,
            "requested_at": datetime.now(),
            "requested_by": approved_by
        }
    