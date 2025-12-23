"""
    Date Written: 12/23/2025 at 6:07 PM
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.term import Term


class TermRepository(BaseRepository[Term]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Term, db)
