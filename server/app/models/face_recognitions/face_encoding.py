"""
    Date written: 12/20/2025 at 3:49 AM
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, LargeBinary, String
from app.db.base import Base

class FaceEncoding(Base):
    __tablename__ = "face_encoding"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Foreign key
    user_id = Column(String(36), ForeignKey("base_user.id"), nullable=False)
    
    # Face encoding (128-dimensional array stored as binary)
    encoding = Column(LargeBinary, nullable=False)
    
    # Original image reference
    image_url = Column(String(500), nullable=True)
    
    # Metadata
    image_quality_score = Column(Float, default=0.0)
    # Face detection confidence (0.0 to 1.0)
    
    face_angle = Column(String(20), default="front")
    # "front", "left", "right" 
    
    is_active = Column(Boolean, default=True)
    # Can deactivate old encodings without deleting
    
    
    # many-to-one relationship with BaseUser
    user = relationship(
        "BaseUser", 
        back_populates="face_encodings",
        uselist=False
    )
    
    def get_encoding_array(self):
        """Convert binary back to numpy array."""
        import numpy as np
        return np.frombuffer(self.encoding, dtype=np.float64)
    
    @staticmethod
    def encode_array(encoding_array):
        """Convert numpy array to binary for storage."""
        import numpy as np
        return encoding_array.tobytes()
    