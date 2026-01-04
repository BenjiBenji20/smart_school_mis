"""
    Date Written: 12/23/2025 at 4:10 PM
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.curriculum import Curriculum


class CurriculumRepository(BaseRepository[Curriculum]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Curriculum, db)
        
        
    async def list_curriculums_by_program(self, program_id: str) -> List[Curriculum]:
        stmt = select(Curriculum).where(
            Curriculum.program_id == program_id
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
