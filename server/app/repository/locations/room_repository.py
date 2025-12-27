"""
    Date Written: 12/26/2025 at 9:15 PM
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.locations.room import Room
from app.exceptions.customed_exception import *


class RoomRepository(BaseRepository[Room]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Room, db)
    