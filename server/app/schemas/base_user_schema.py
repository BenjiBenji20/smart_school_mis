from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator, EmailStr

import regex

from app.exceptions.customed_exception import UnprocessibleContentException
from app.models.enums.user_state import UserRole, UserGender, UserStatus


class BaseUserResponseSchema(BaseModel):
    id: str
    created_at: datetime
    
    first_name: str
    middle_name: str
    last_name: str
    suffix: str | None
    age: int
    gender: UserGender
    complete_address: str
    
    email: str
    cellphone_number: str
    role: UserRole | None
    is_active: bool
    
    class Config: 
        from_attributes = True
    
    
class BaseUserRequestSchema(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    cellphone_number: str = Field(..., min_length=11, max_length=13)
    password: str = Field(..., min_length=8, max_length=50)
    role: UserRole | None = None
    
    first_name: str = Field(..., max_length=50)
    middle_name: str | None = Field(None, max_length=50)
    last_name: str = Field(..., max_length=50)
    suffix: str | None = Field(None, max_length=4)
    age: int = Field(default=18, gt=0, le=120)
    gender: UserGender = Field(..., description="Male and Female only")
    complete_address: str = Field(default="Malabon City", max_length=255)

    @field_validator("first_name", "middle_name", "last_name")
    @classmethod
    def validate_names(cls, val: str):
        # Names should start with a letter, contain only letters, spaces, hyphens, apostrophes
        pattern = r"^[\p{L}][\p{L}\p{M}'\- ]*$"
        if not regex.match(pattern, val.strip()):
            raise UnprocessibleContentException(f"Must be valid name format: {val}")
        return val.strip()


    @field_validator("complete_address")
    @classmethod
    def validate_address(cls, val: str):
        # Addresses can start with numbers, contain letters, numbers, spaces, punctuation
        pattern = r"^[\p{L}\p{N}][\p{L}\p{N}\p{M}'\-\s.,#]*$"
        if not regex.match(pattern, val.strip()):
            raise UnprocessibleContentException(f"Must be valid address format: {val}")
        return val.strip()
  
  
    @field_validator('email')
    @classmethod
    def validate_email_length(cls, val: str):
        """Additional length validation for database compatibility"""
        if len(val) > 100:
            raise ValueError('Email must be less than 100 characters')
        return val.strip()
  
  
class CredentialValidatorSchema(BaseModel):
    email: str
    password: str
    
    
class StudentResponseSchema(BaseUserResponseSchema):
    university_code: str
    status: UserStatus
    last_school_attended: str| None = None
    program_enrolled_date: date| None = None
    year_level: int 
    