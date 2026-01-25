"""
    Date Written: 1/24/2025 at 10:49 AM
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.users.dean import Dean
from app.exceptions.customed_exception import *
from app.repository.users.dean_repository import DeanRepository
from app.models.users.registrar import Registrar
from app.models.enums.user_state import DeanStatus


class RegistrarRepository(BaseRepository[Registrar]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Registrar, db)
        self.dean_repo = DeanRepository(db)
    
    
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
        dean: Dean = await self.dean_repo.get_dean_by_id(dean_id)
        
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
        