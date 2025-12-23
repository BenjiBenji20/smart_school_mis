"""
    Date Written: 12/23/2025 at 11:54 AM
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.program import Program


class ProgramRepository(BaseRepository[Program]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Program, db)

