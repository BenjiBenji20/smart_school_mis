"""
    Date Written: 12/26/2025 at 11:44 AM
"""

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.users.professor_repository import ProfessorRepository
from app.models.users.professor import Professor
from app.schemas.generic_schema import GenericResponse
from app.exceptions.customed_exception import *

class ProfessorService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.prof_repo = ProfessorRepository(db)


    async def assign_professor_department(
        self,
        professor_id: str,
        department_id: str,
        requested_by: str | None = None
    ) -> GenericResponse:
        
        assigned_prof: Professor = await self.prof_repo.assign_professor_department(
            professor_id, department_id
        )
        
        if not assigned_prof:
            raise InvalidRequestException("Invalid professor department assignment.")
        
        return GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Professor assigned to department"
            )
         