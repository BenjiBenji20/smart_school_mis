"""
    Date Written: 12/20/2025 at 11:38 AM
"""

from pydantic import BaseModel


class FaceRegistrationRequest(BaseModel):
    image_base64: str
    angle: str = "front"  # "front", "left", "right"
    
    
class FaceRegistrationResponse(BaseModel):
    success: bool
    encoding_id: str
    quality_score: float
    message: str


class FaceVerificationRequest(BaseModel):
    image_base64: str
    action: str  # "change_password", "view_grades", etc.
    
    
class FaceVerificationResponse(BaseModel):
    verified: bool
    confidence: float
    distance: float
    matched_encoding_id: str    
    message: str
    