"""
    Date Written: 12/26/2025 at 4:16 PM
"""

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.users.dean_repository import DeanRepository
from app.models.users.dean import Dean
from app.schemas.generic_schema import GenericResponse
from app.exceptions.customed_exception import *

class DeanService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.prof_repo = DeanRepository(db)


    async def assign_dean_department(
        self,
        dean_id: str,
        department_id: str,
        requested_by: str | None = None
    ) -> GenericResponse:
        
        assigned_prof: Dean = await self.prof_repo.assign_dean_department(
            dean_id, department_id
        )
        
        if not assigned_prof:
            raise InvalidRequestException("Invalid dean department assignment.")
        
        return GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Dean assigned to department"
            )
         