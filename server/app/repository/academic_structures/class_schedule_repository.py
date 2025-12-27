"""
    Date Written: 12/27/2025 at 2:37 PM
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.class_schedule import ClassSchedule
from app.models.academic_structures.class_section import ClassSection
from app.models.academic_structures.professor_class_section import ProfessorClassSection
from app.models.locations.room import Room


class ClassScheduleRepository(BaseRepository[ClassSchedule]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ClassSchedule, db)
        
        
    async def get_schedules_by_room(self, room_id: str, day_of_week: int) -> List[ClassSchedule]:
        stmt = (
            select(ClassSchedule)
                .where(
                    Room.id == room_id,
                    ClassSchedule.day_of_week == day_of_week
                )
        )
        
        result = await self.db.execute(stmt)
        schedules = result.scalars().all()
        return schedules
            
        
    async def get_schedules_by_professor(self, professor_id, day_of_week) -> List[ClassSchedule]:
        stmt = (
            select(ClassSchedule)
                .join(ProfessorClassSection, ProfessorClassSection.class_section_id == ClassSchedule.class_section_id)
                    .where(
                        ProfessorClassSection.professor_id == professor_id,
                        ClassSchedule.day_of_week == day_of_week
                    )
        )
        
        result = await self.db.execute(stmt)
        schedules = result.scalars().all()
        return schedules
        
