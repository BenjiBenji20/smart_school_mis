"""
    Date Written: 12/26/2025 at 4:22 PM
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.users.dean import Dean
from app.models.enums.user_state import DeanStatus
from app.exceptions.customed_exception import *


class DeanRepository(BaseRepository[Dean]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Dean, db)
        
        
    async def get_dean_by_id(self, dean_id: str) -> Optional[Dean]:
        """
            Get dean by ID.
            This will JOIN base_user and dean tables automatically.
        """
        result = await self.db.execute(
            select(Dean).where(Dean.id == dean_id)
        )
        return result.scalars().first()
    
    
    async def get_active_deans(self) -> List[Dean]:
        """Get all active deans."""
        result = await self.db.execute(
            select(Dean).where(
                Dean.dean_status == DeanStatus.ACTIVE
            )
        )
        return result.scalars().all()
    
    
    async def assign_dean_department(
        self,
        dean_id: str,
        department_id: str
    ) -> Optional[Dean]:
        dean: Dean = await self.get_dean_by_id(dean_id)
        
        if not dean:
            raise UnauthorizedAccessException(f"Dean not found with id: {dean_id}")
        
        if dean.department_id:
            raise InvalidRequestException(
                f"Dean already has department: {dean.department_id}"
                "Cannot assign to multiple departments."
            )
            
        dean.department_id = department_id
        await self.db.commit()
        await self.db.refresh(dean)
        
        return dean
        