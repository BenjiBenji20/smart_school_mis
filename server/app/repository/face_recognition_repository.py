from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.face_recognitions.face_encoding import FaceEncoding
from app.repository.base_repository import BaseRepository
from app.exceptions.customed_exception import InvalidRequestException


class FaceRecognitionRepository(BaseRepository[FaceEncoding]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(FaceEncoding, db)
        
    async def register_face(
        self, 
        user_id: str,
        encoding,
        image_url: str,
        angle: str,
        quality_score: float
    ) -> Optional[FaceEncoding]:
        
        """
            User that has already face encoded cannot make a duplicate entry.
        """
        is_user_encoded = await self.get_user_encoding(user_id)
        
        if is_user_encoded:
            raise InvalidRequestException("User already face encoded.")
        
        # Store encoding in database
        face_encoding_record = FaceEncoding(
            user_id=user_id,
            encoding=FaceEncoding.encode_array(encoding),
            image_url=image_url,
            image_quality_score=quality_score,
            face_angle=angle,
            is_active=True
        )
        
        self.db.add(face_encoding_record)
        await self.db.commit()
        await self.db.refresh(face_encoding_record)
        
        return face_encoding_record

    
    async def get_user_encoding(self, user_id: str, is_active: bool = True) -> Optional[FaceEncoding]:
        """Get user's face encodings using user id."""
        is_user_encoded = await self.db.execute(
            select(FaceEncoding)
                .where(
                    FaceEncoding.user_id == user_id,
                    FaceEncoding.is_active == is_active
                )
        )
        
        return is_user_encoded.scalars().first()
    
    
    async def get_all_user_encodings(self, user_id: str, is_active: bool = True) -> Optional[List[FaceEncoding]]:
        """Get all face encodings for a user."""
        is_user_encoded = await self.db.execute(
            select(FaceEncoding)
                .where(
                    FaceEncoding.user_id == user_id,
                    FaceEncoding.is_active == is_active
                )
        )
        
        return is_user_encoded.scalars().all()
    