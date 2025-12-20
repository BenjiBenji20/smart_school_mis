"""
    Date Written: 12/20/2025 at 11:38 AM
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_session import get_async_db
from app.middleware.current_user import get_current_user
from app.ai.face_recognition.face_recognition import FaceRecognitionAI
from app.schemas.face_recognition_schema import *
from app.exceptions.customed_exception import *
from app.models.users.base_user import BaseUser

face_recognition_router = APIRouter(prefix="/api/face-recognition", tags=["Face Recognition"])

@face_recognition_router.post("/register", response_model=FaceRegistrationResponse)
async def register_face(
    data: FaceRegistrationRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user)
):
    """
        Register user's face encoding.
        
        Flow:
        1. User captures photo from frontend
        2. Frontend sends base64 image
        3. Backend processes and stores encoding
    """
    service = FaceRecognitionAI(db)
    
    result = await service.register_face(
        user_id=current_user.id,
        image_base64=data.image_base64,
        angle=data.angle
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result


@face_recognition_router.post("/verify", response_model=FaceVerificationResponse)
async def verify_face(
    data: FaceVerificationRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user)
):
    """
        Verify user's identity via face recognition.
        
        Used as second-factor authentication for sensitive actions.
    """
    service = FaceRecognitionAI(db)
    
    result = await service.verify_face(
        user_id=current_user.id,
        image_base64=data.image_base64
    )
    
    if not result["verified"]:
        # Log failed attempt (security audit)
        # TODO: Implement failed attempt tracking
        # add failed attempt count to the face_encoding table
        # and limit the failed attempt to 3 to force logout the current user.
        raise UnauthorizedAccessException("Request prohibited.")

    return result


# === For admin access only ===
@face_recognition_router.get("/my-encodings")
async def get_my_encodings(
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user)
):
    """Get list of user's registered face encodings."""
    service = FaceRecognitionAI(db)
    
    encodings = await service.get_user_encodings(current_user.id)
    
    return {
        "count": len(encodings),
        "encodings": [
            {
                "id": enc.id,
                "angle": enc.face_angle,
                "quality_score": enc.quality_score,
                "created_at": enc.created_at,
                "is_active": enc.is_active
            }
            for enc in encodings
        ]
    }


@face_recognition_router.delete("/encodings/{encoding_id}")
async def delete_encoding(
    encoding_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: BaseUser = Depends(get_current_user)
):
    """Delete a specific face encoding."""
    service = FaceRecognitionAI(db)
    
    # Verify encoding belongs to current user
    encodings = await service.get_user_encodings(current_user.id)
    encoding_ids = [enc.id for enc in encodings]
    
    if encoding_id not in encoding_ids:
        raise HTTPException(status_code=403, detail="Not your encoding")
    
    success = await service.delete_encoding(encoding_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Encoding not found")
    
    return {"message": "Encoding deleted successfully"}
