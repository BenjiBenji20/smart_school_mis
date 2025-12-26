"""
    Date Written: 12/23/2025 at 3:43 PM
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.curriculum_course import CurriculumCourse


class CurriculumCourseRepository(BaseRepository[CurriculumCourse]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(CurriculumCourse, db)
