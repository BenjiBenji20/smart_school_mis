"""
    Date Written: 12/26/2025 at 4:26 PM
"""

from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.users.program_chair_repository import ProgramChairRepository
from app.models.users.program_chair import ProgramChair
from app.exceptions.customed_exception import *
from app.schemas.user_schema import ProgramChairResponseSchema

class ProgramChairService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.program_chair_repo = ProgramChairRepository(db)
        
        
    async def get_current_program_chair_user(self, program_chair_id: str) -> ProgramChairResponseSchema:
        program_chair: ProgramChair = await self.program_chair_repo.get_program_chair_by_id(program_chair_id)
        if program_chair is None:
            raise ResourceNotFoundException("Program Chair user not found.")
        
        return ProgramChairResponseSchema(
            id=program_chair.id,
            created_at=program_chair.created_at,
            first_name=program_chair.first_name,
            middle_name=program_chair.middle_name,
            last_name=program_chair.last_name,
            suffix=program_chair.suffix,
            age=program_chair.age,
            gender=program_chair.gender,
            complete_address=program_chair.complete_address,
            email=program_chair.email,
            cellphone_number=program_chair.cellphone_number,
            role=program_chair.role,
            is_active=program_chair.is_active,
            university_code=program_chair.university_code,
            program_chair_status=program_chair.program_chair_status,
            program_id=program_chair.program_id
        )
