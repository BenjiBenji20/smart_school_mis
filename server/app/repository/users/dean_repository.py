"""
    Date Written: 12/26/2025 at 4:22 PM
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.users.dean import Dean
from app.exceptions.customed_exception import *
from app.models.enums.user_state import ProgramChairStatus
from app.models.users.program_chair import ProgramChair
from app.repository.users.program_chair_repository import ProgramChairRepository


class DeanRepository(BaseRepository[Dean]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Dean, db)
        self.program_chair_repo = ProgramChairRepository(db)
        
        
    async def get_dean_by_id(self, dean_id: str) -> Optional[Dean]:
        """
            Get dean by ID.
            This will JOIN base_user and dean tables automatically.
        """
        result = await self.db.execute(
            select(Dean).where(Dean.id == dean_id)
        )
        return result.scalars().first()
    
    
    async def assign_program_chair_program(
        self,
        program_chair_id: str,
        program_id: str
    ) -> Optional[ProgramChair]:
        program_chair: ProgramChair = await self.program_chair_repo.get_program_chair_by_id(program_chair_id)
        
        if not program_chair:
            raise UnauthorizedAccessException(f"ProgramChair not found with id: {program_chair_id}")
        
        if program_chair.program_id:
            raise InvalidRequestException(
                f"ProgramChair already has program: {program_chair.program_id}"
                "Cannot assign to multiple programs."
            )
            
        program_chair.program_id = program_id
        await self.db.commit()
        await self.db.refresh(program_chair)
        
        return program_chair
    
    
    async def get_active_program_chairs(self) -> List[ProgramChair]:
        """Get all active program_chairs."""
        result = await self.program_chair_repo.db.execute(
            select(ProgramChair).where(
                ProgramChair.program_chair_status == ProgramChairStatus.ACTIVE
            )
        )
        return result.scalars().all()