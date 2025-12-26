"""
    Date Written: 12/24/2025 at 6:57 PM
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.users.professor import Professor
from app.models.enums.user_state import ProfessorStatus
from app.exceptions.customed_exception import *


class ProfessorRepository(BaseRepository[Professor]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Professor, db)
        
        
    async def get_professor_by_id(self, professor_id: str) -> Optional[Professor]:
        """
            Get professor by ID.
            This will JOIN base_user and professor tables automatically.
        """
        result = await self.db.execute(
            select(Professor).where(Professor.id == professor_id)
        )
        return result.scalars().first()
    
    
    async def get_active_professors(self) -> List[Professor]:
        """Get all active professors."""
        result = await self.db.execute(
            select(Professor).where(
                Professor.professor_status == ProfessorStatus.ACTIVE
            )
        )
        return result.scalars().all()
    
    
    async def assign_professor_department(
        self,
        professor_id: str,
        department_id: str
    ) -> Optional[Professor]:
        professor: Professor = await self.get_professor_by_id(professor_id)
        
        if not professor:
            raise UnauthorizedAccessException(f"Professor not found with id: {professor_id}")
        
        if professor.department_id:
            raise InvalidRequestException(
                f"Professor already has department: {professor.department_id}"
                "Cannot assign to multiple departments."
            )
            
        professor.department_id = department_id
        await self.db.commit()
        await self.db.refresh(professor)
        
        return professor
        