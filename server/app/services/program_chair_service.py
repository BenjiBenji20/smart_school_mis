"""
    Date Written: 12/26/2025 at 4:26 PM
"""

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.users.program_chair_repository import ProgramChairRepository
from app.models.users.program_chair import ProgramChair
from app.schemas.generic_schema import GenericResponse
from app.exceptions.customed_exception import *

class ProgramChairService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.prof_repo = ProgramChairRepository(db)


    async def assign_program_chair_program(
        self,
        program_chair_id: str,
        program_id: str,
        requested_by: str | None = None
    ) -> GenericResponse:
        
        assigned_prof: ProgramChair = await self.prof_repo.assign_program_chair_program(
            program_chair_id, program_id
        )
        
        if not assigned_prof:
            raise InvalidRequestException("Invalid program_chair program assignment.")
        
        return GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"ProgramChair assigned to program"
            )
         