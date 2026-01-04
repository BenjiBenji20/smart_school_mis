"""
    Date Written: 12/26/2025 at 9:15 PM
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repository.base_repository import BaseRepository
from app.models.locations.room import Room
from app.exceptions.customed_exception import *


class RoomRepository(BaseRepository[Room]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Room, db)
        
        
    async def get_existing_ids(self, room_ids: set[str]) -> List[str]:
        stmt = select(Room.id).where(Room.id.in_(room_ids))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    
    async def list_rooms_by_building(self, building_id: str) -> List[Room]:
        stmt = select(Room).where(
            Room.building_id == building_id
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
        