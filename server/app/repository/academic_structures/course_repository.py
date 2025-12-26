"""
    Date Written: 12/22/2025 at 8:24 PM
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.course import Course


class CourseRepository(BaseRepository[Course]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Course, db)

