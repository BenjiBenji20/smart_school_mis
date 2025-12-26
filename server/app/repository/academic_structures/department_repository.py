"""
    Date Written: 12/23/2025 at 11:13 AM
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.department import Department


class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Department, db)

