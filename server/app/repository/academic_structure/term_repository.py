"""
    Date Written: 12/23/2025 at 6:07 PM
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.term import Term
from app.models.enums.academic_structure_state import TermStatus


class TermRepository(BaseRepository[Term]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Term, db)
        
        
    async def get_active_year_term(self, current_year: int) -> List[Term]:
        """
            Get active terms.
            Terms that has status of OPEN and within or in the current 
            academic_year_start and academic_year_end.
        """
        query = select(Term).where(
            and_(
                Term.academic_year_start == current_year,
                Term.academic_year_end >= current_year,
                Term.status == TermStatus.OPEN
            )
        )
        
        results = await self.db.execute(query)
        return results.scalars().all()
