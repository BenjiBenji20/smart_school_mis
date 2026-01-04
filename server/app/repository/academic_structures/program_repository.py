"""
    Date Written: 12/23/2025 at 11:54 AM
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.program import Program


class ProgramRepository(BaseRepository[Program]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Program, db)


    async def list_programs_by_department(self, department_id: str) -> List[Program]:
        stmt = select(Program).where(
            Program.department_id == department_id
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
