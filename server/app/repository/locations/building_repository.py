"""
    Date Written: 12/26/2025 at 8:50 PM
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.locations.building import Building
from app.exceptions.customed_exception import *


class BuildingRepository(BaseRepository[Building]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Building, db)
    