"""
    Date Written: 12/23/2025 at 4:10 PM
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.curriculum import Curriculum


class CurriculumRepository(BaseRepository[Curriculum]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Curriculum, db)
