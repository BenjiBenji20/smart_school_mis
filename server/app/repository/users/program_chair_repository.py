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
    
    
    
        