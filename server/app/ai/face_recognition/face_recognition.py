"""
    Date written: 12/20/2025 at 7:11 AM
"""

import os
import uuid
import face_recognition
import numpy as np
import cv2
import base64
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.face_recognitions.face_encoding import FaceEncoding
from app.configs.settings import settings
from app.repository.face_recognition_repository import FaceRecognitionRepository

class FaceRecognitionAI:
    """
        AI/Service for face encoding and verification.
        Uses face_recognition library (dlib + OpenCV).
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.face_recognition_repo = FaceRecognitionRepository(db)
        
        # Configuration
        self.TOLERANCE = 0.6  # Lower = stricter (0.6 is default)
        self.MIN_FACE_SIZE = 100  # Minimum face dimension in pixels
        self.IMAGE_SIZE = (600, 600)  # Resize large images for performance
    
    
    # ============================================
    # REGISTRATION (Encoding Creation)
    # ============================================
    async def register_face(
        self,
        user_id: str,
        image_base64: str,
        angle: str = "front"
    ) -> Dict:
        """
            Register a user's face by creating and storing encoding.
            
            Args:
                user_id: User's database ID
                image_base64: Base64-encoded image from frontend
                angle: "front", "left", or "right"
            
            Returns:
                {
                    "success": True/False,
                    "encoding_id": "uuid",
                    "quality_score": 0.95,
                    "message": "Face registered successfully"
                }
        """
        
        # Decode base64 to numpy array
        image_array = self._decode_base64_image(image_base64)
        
        if image_array is None:
            return {
                "success": False,
                "message": "Invalid image format"
            }
        
        # Detect face locations
        face_locations = face_recognition.face_locations(image_array)
        
        if len(face_locations) == 0:
            return {
                "success": False,
                "message": "No face detected. Please ensure your face is clearly visible."
            }
        
        if len(face_locations) > 1:
            return {
                "success": False,
                "message": "Multiple faces detected. Please ensure only your face is visible."
            }
        
        # Check face size (quality control)
        top, right, bottom, left = face_locations[0]
        face_width = right - left
        face_height = bottom - top
        
        if face_width < self.MIN_FACE_SIZE or face_height < self.MIN_FACE_SIZE:
            return {
                "success": False,
                "message": f"Face too small. Please move closer to the camera."
            }
        
        # Generate encoding
        encodings = face_recognition.face_encodings(image_array, face_locations)
        
        if len(encodings) == 0:
            return {
                "success": False,
                "message": "Could not generate face encoding. Please try again with better lighting."
            }
        
        encoding = encodings[0]  # First (and only) face
        
        # Calculate quality score (based on face size and clarity)
        quality_score = self._calculate_quality_score(face_width, face_height)
        
        # Upload image to S3/Cloudinary
        image_url = await self._upload_image(user_id, image_base64, angle)
        
        # Store encoding in database
        face_encoding_record = await self.face_recognition_repo.register_face(
            user_id,
            encoding,
            image_url,
            angle,
            quality_score
        )
        
        return {
            "success": True,
            "encoding_id": face_encoding_record.id,
            "quality_score": quality_score,
            "message": "Face registered successfully"
        }
    
    
    # ============================================
    # VERIFICATION (Face Matching)
    # ============================================
    async def verify_face(
        self,
        user_id: str,
        image_base64: str
    ) -> Dict:
        """
        Verify a user's identity by comparing face with stored encoding.
        
        Args:
            user_id: User's database ID
            image_base64: Base64-encoded image from frontend
        
        Returns:
            {
                "verified": True/False,
                "confidence": 0.95,
                "distance": 0.35,
                "message": "Face verified"
            }
        """
        
        # Get user's stored encodings
        stored_encodings = await self.face_recognition_repo.get_all_user_encodings(user_id)
        
        if not stored_encodings:
            return {
                "verified": False,
                "message": "No face registered. Please register your face first."
            }
        
        # Decode captured image
        image_array = self._decode_base64_image(image_base64)
        
        if image_array is None:
            return {
                "verified": False,
                "message": "Invalid image format"
            }
        
        # Detect face in captured image
        face_locations = face_recognition.face_locations(image_array)
        
        if len(face_locations) == 0:
            return {
                "verified": False,
                "message": "No face detected. Please ensure your face is clearly visible."
            }
        
        if len(face_locations) > 1:
            return {
                "verified": False,
                "message": "Multiple faces detected. Please ensure only your face is visible."
            }
        
        # Generate encoding for captured face
        current_encodings = face_recognition.face_encodings(image_array, face_locations)
        
        if len(current_encodings) == 0:
            return {
                "verified": False,
                "message": "Could not process face. Please try again with better lighting."
            }
        
        current_encoding = current_encodings[0]
        
        # Compare with ALL stored encodings (if multiple angles)
        best_match = None
        best_distance = float('inf')
        
        for stored in stored_encodings:
            stored_array = stored.get_encoding_array()
            
            # Calculate face distance (lower = more similar)
            distance = face_recognition.face_distance([stored_array], current_encoding)[0]
            
            if distance < best_distance:
                best_distance = distance
                best_match = stored
        
        # Determine if verified
        verified = best_distance <= self.TOLERANCE
        confidence = 1.0 - best_distance  # Convert distance to confidence
        
        if verified:
            return {
                "verified": True,
                "confidence": round(confidence, 3),
                "distance": round(best_distance, 3),
                "matched_encoding_id": best_match.id,
                "message": "Face verified successfully"
            }
        else:
            return {
                "verified": False,
                "confidence": round(confidence, 3),
                "distance": round(best_distance, 3),
                "message": f"Face verification failed. Confidence too low ({round(confidence * 100, 1)}%)"
            }
    
    
    # ============================================
    # HELPER METHODS
    # ============================================
    def _decode_base64_image(self, base64_string: str) -> Optional[np.ndarray]:
        """
            Convert base64 string to numpy array (BGR format).
            
            Line-by-line explanation:
            1. Remove data URL prefix if present (e.g., "data:image/jpeg;base64,")
            2. Decode base64 to bytes
            3. Convert bytes to numpy array
            4. Decode image using OpenCV (JPEG/PNG → BGR)
            5. Convert BGR to RGB (face_recognition expects RGB)
        """
        try:
            # Remove data URL prefix
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # Decode base64 to bytes
            image_bytes = base64.b64decode(base64_string)
            
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            
            # Decode image (JPEG/PNG → BGR)
            image_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image_bgr is None:
                return None
            
            # Resize if too large (performance optimization)
            height, width = image_bgr.shape[:2]
            if width > self.IMAGE_SIZE[0] or height > self.IMAGE_SIZE[1]:
                image_bgr = cv2.resize(image_bgr, self.IMAGE_SIZE)
            
            # Convert BGR to RGB (face_recognition expects RGB)
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            
            return image_rgb
            
        except Exception as e:
            print(f"Error decoding image: {e}")
            return None
    
    
    def _calculate_quality_score(self, face_width: int, face_height: int) -> float:
        """
            Calculate quality score based on face size.
            Larger faces = better quality (more detail).
            
            Returns: 0.0 to 1.0
        """
        face_area = face_width * face_height
        
        # Scoring thresholds
        if face_area >= 40000:  # ~200x200 pixels
            return 1.0
        elif face_area >= 20000:  # ~140x140 pixels
            return 0.85
        elif face_area >= 10000:  # ~100x100 pixels
            return 0.70
        else:
            return 0.50
    
    
    async def _upload_image(
        self,
        user_id: str,
        image_base64: str,
        angle: str
    ) -> Optional[str]:
        if settings.ENV == "dev":
            
            os.makedirs("test_images", exist_ok=True)

            filename = f"{user_id}_{angle}_{uuid.uuid4()}.jpg"
            filepath = os.path.join("test_images", filename)

            if "," in image_base64:
                image_base64 = image_base64.split(",")[1]

            with open(filepath, "wb") as f:
                f.write(base64.b64decode(image_base64))

            return filepath  # local path for testing
        
        """
        Upload image to S3/Cloudinary (implement later).
        For now, return None.
        
        TODO: Implement S3/Cloudinary upload
        """
        # Placeholder - implement cloud storage later
        return None
    
    
    # ============================================
    # ADMIN FUNCTIONS
    # ============================================
    async def get_all_user_encodings(self, user_id: str) -> List[FaceEncoding]:
        """Get all face encodings for a user."""
        return await self.face_recognition_repo.get_all_user_encodings(user_id)
    
    
    async def delete_encoding(self, encoding_id: str) -> bool:
        """Delete a specific face encoding."""
        result = await self.db.execute(
            select(FaceEncoding).where(FaceEncoding.id == encoding_id)
        )
        encoding = result.scalars().first()
        
        if encoding:
            await self.db.delete(encoding)
            await self.db.commit()
            return True
        
        return False
   
    
    async def deactivate_encoding(self, encoding_id: str) -> bool:
        """Soft delete - deactivate instead of deleting."""
        result = await self.db.execute(
            select(FaceEncoding).where(FaceEncoding.id == encoding_id)
        )
        encoding = result.scalars().first()
        
        if encoding:
            encoding.is_active = False
            await self.db.commit()
            return True
        
        return False
    