"""
    Date Written: 12/14/2025 at 8:42 AM
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users.base_user import BaseUser
from app.repository.base_repository import BaseRepository
from app.models.enums.user_state import UserStatus, UserRole
from app.exceptions.customed_exception import *


class UserRegistrationRepository(BaseRepository[BaseUser]):
    """
        Any user registration repository.
        This repository is for the first phase of registration process.
        Any user has the same registration inputs and procedure at first phase.
    """
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(BaseUser, db)
    
    
    async def is_email_exists(self, email: str) -> bool:
        """Check if email is already registered."""
        result = await self.db.execute(
            select(BaseUser).where(BaseUser.email == email).limit(1)
        )
        return result.scalars().first() is not None
    
    
    async def approve_pending_registration(
        self, approved_by: str, user_role: Optional[UserRole], id: str
    ) -> bool:
        """
            Only user with higher role  can approved the user with lower role.
            
            :param approved_by: by whome the user approved
            :type approved_by: str
            :param role: the role of user to be approved
            :type enum UserRole: 
            :param id: the user to be approved
            :type id: str
            :return: to flag wheather the user is successfully approved
            :rtype: bool
        """
        result = await self.db.execute(
            select(BaseUser).where(BaseUser.id == id).limit(1)
        )
        
        user_to_approved: BaseUser = result.scalar_one_or_none()
        
        if user_to_approved is None:
            raise ResourceNotFoundException("User not found.")

        if user_to_approved.status != UserStatus.PENDING:
            raise InvalidRequestException("User is not pending approval.")
        
        user_to_approved.status = UserStatus.APPROVED
        user_to_approved.approved_by = approved_by
        
        if user_role:
            user_to_approved.role = user_role
        
        await self.db.commit()
        return True
        