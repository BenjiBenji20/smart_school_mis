"""
    Date Written: 12/26/2025 at 4:16 PM
"""

from datetime import datetime, timezone
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.users.dean_repository import DeanRepository
from app.models.users.dean import Dean
from app.exceptions.customed_exception import *
from app.models.users.program_chair import ProgramChair
from app.schemas.generic_schema import GenericResponse
from app.schemas.user_schema import *

class DeanService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.dean_repo = DeanRepository(db)


    async def get_current_dean_user(self, dean_id: str) -> DeanResponseSchema:
        dean: Dean = await self.dean_repo.get_dean_by_id(dean_id)
        if dean is None:
            raise ResourceNotFoundException("Dean user not found.")
        
        return DeanResponseSchema(
            id=dean.id,
            created_at=dean.created_at,
            first_name=dean.first_name,
            middle_name=dean.middle_name,
            last_name=dean.last_name,
            suffix=dean.suffix,
            age=dean.age,
            gender=dean.gender,
            complete_address=dean.complete_address,
            email=dean.email,
            cellphone_number=dean.cellphone_number,
            role=dean.role,
            is_active=dean.is_active,
            university_code=dean.university_code,
            dean_status=dean.dean_status,
            department_id=dean.department_id,
        )
        
        
    async def assign_program_chair_program(
        self,
        program_chair_id: str,
        program_id: str,
        requested_by: str | None = None
    ) -> GenericResponse:
        
        assigned_prof: ProgramChair = await self.dean_repo.assign_program_chair_program(
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
         
         
    async def get_active_program_chairs(self) -> List[ProgramChairResponseSchema]:
        active_program_chairs: List[ProgramChair] = await self.dean_repo.get_active_program_chairs()
        if len(active_program_chairs) < 1:
            return []
        
        response: List[ProgramChairResponseSchema] = []
        for chair in active_program_chairs:
            response.append(
                ProgramChairResponseSchema(
                    id=chair.id,
                    created_at=chair.created_at,
                    first_name=chair.first_name,
                    middle_name=chair.middle_name,
                    last_name=chair.last_name,
                    suffix=chair.suffix,
                    age=chair.age,
                    gender=chair.gender,
                    complete_address=chair.complete_address,
                    email=chair.email,
                    cellphone_number=chair.cellphone_number,
                    role=chair.role,
                    is_active=chair.is_active,
                    university_code=chair.university_code,
                    status=chair.status,
                    program_id=chair.program_id,
                )
            )
                
        return response