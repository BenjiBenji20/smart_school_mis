"""
    Date Written: 12/14/2025 at 3:58 AM
"""

from pydantic import BaseModel

from app.models.enums.user_state import UserRole


class TokenResponseSchema(BaseModel):
  # return 2 different token
  access_token: str
  refresh_token: str
  token_type: str
  role: UserRole
  
  class Config:
    from_attributes = True
    
    
class RefreshTokenResponseSchema(BaseModel):
  # return 2 different token
  access_token: str
  token_type: str
  
  class Config:
    from_attributes = True
  