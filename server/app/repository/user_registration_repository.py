"""
    Date Written: 12/14/2025 at 8:42 AM
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users.base_user import BaseUser
from app.repository.base_repository import BaseRepository


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
        