"""
    Date Written: 12/26/2025 at 4:26 PM
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.users.program_chair import ProgramChair
from app.models.enums.user_state import ProgramChairStatus
from app.exceptions.customed_exception import *


class ProgramChairRepository(BaseRepository[ProgramChair]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ProgramChair, db)
        
        
    async def get_program_chair_by_id(self, program_chair_id: str) -> Optional[ProgramChair]:
        """
            Get program_chair by ID.
            This will JOIN base_user and program_chair tables automatically.
        """
        result = await self.db.execute(
            select(ProgramChair).where(ProgramChair.id == program_chair_id)
        )
        return result.scalars().first()
    
    
    async def get_active_program_chairs(self) -> List[ProgramChair]:
        """Get all active program_chairs."""
        result = await self.db.execute(
            select(ProgramChair).where(
                ProgramChair.program_chair_status == ProgramChairStatus.ACTIVE
            )
        )
        return result.scalars().all()
    
    
    async def assign_program_chair_program(
        self,
        program_chair_id: str,
        program_id: str
    ) -> Optional[ProgramChair]:
        program_chair: ProgramChair = await self.get_program_chair_by_id(program_chair_id)
        
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
        