"""
    Date Written: 12/23/2025 at 3:43 PM
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.curriculum_course import CurriculumCourse


class CurriculumCourseRepository(BaseRepository[CurriculumCourse]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(CurriculumCourse, db)
        
        
    async def list_curriculum_course_by_field(
        self,
        curriculum_id: str = None,
        year_level: int = None,
        semester: int = None
    ) -> List[CurriculumCourse]:
        stmt = select(CurriculumCourse)
        
        # check if any of the params has value to use as filter
        if curriculum_id:
            stmt = stmt.where(CurriculumCourse.curriculum_id == curriculum_id)
            
        if year_level:
            stmt = stmt.where(CurriculumCourse.year_level == year_level)
            
        if semester:
            stmt = stmt.where(CurriculumCourse.semester == semester)
            
        result = await self.db.execute(stmt)
        return result.scalars().all()
