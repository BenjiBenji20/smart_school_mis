"""
    Date Written: 12/14/2025 at 4:20 AM
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import Optional

from app.models.users.base_user import BaseUser

class AuthRepository:
    """
        Repository for authentication operations.
        Using BaseUser model as polymorphic accross all users.
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_email(self, email: str) -> Optional[BaseUser]:
        """
            Get any user by email (works for all user types).
            Returns the actual subclass instance (Student, Professor, etc.)
        """
        result = await self.db.execute(
            select(BaseUser).where(BaseUser.email == email)
        )
        return result.scalars().first()
    
    
    async def is_email_exists(self, email: str) -> bool:
        """Check if email is already registered."""
        result = await self.db.execute(
            select(BaseUser).where(BaseUser.email == email).limit(1)
        )
        return result.scalars().first() is not None
    
    
    async def get_active_user_by_email(self, email: str) -> Optional[BaseUser]:
        """Get active user by email."""
        result = await self.db.execute(
            select(BaseUser).where(
                BaseUser.email == email,
                BaseUser.is_active == True
            )
        )
        return result.scalars().first()
    