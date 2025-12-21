"""
    Date Written: 12/14/2025 at 8:12 AM
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

import hashlib
from passlib.context import CryptContext
import logging

from app.schemas.base_user_schema import BaseUserRequestSchema, BaseUserResponseSchema
from app.repository.user_registration_repository import UserRegistrationRepository
from app.exceptions.customed_exception import *
from app.models.enums.user_state import UserRole, UserStatus

logger = logging.getLogger(__name__)


class RegistrationService:
    """
        Any user registration service
    """
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_registration_repo = UserRegistrationRepository(db)
    
    
    def hash_password(self, password: str) -> str:
        pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )
        # normalize
        password_bytes = password.encode("utf-8")
        # pre-hash (fixed length)
        sha256_hash = hashlib.sha256(password_bytes).hexdigest()
        # bcrypt hash
        return pwd_context.hash(sha256_hash)
    
    
    async def user_registration_service(
        self, 
        user: BaseUserRequestSchema
    ) -> Optional[BaseUserResponseSchema]:
        """
            Register any user model.
        
            :param user: Any user model
            :type user: BaseUserRequestSchema
            :return: Any user model
            :rtype: BaseUserResponseSchema
        """
        try:
            # validate if user exists by searching using its email
            is_user_exists = await self.user_registration_repo.is_email_exists(user.email)
            # if exists, invalidate the registration
            if is_user_exists:
                raise DuplicateEntryException(f"User with {user.email} as email already exists.")
            
            hashed_pw = self.hash_password(user.password)

            user_dict = user.model_dump(exclude={"password"})  
            user_dict["password_hash"] = hashed_pw
             
            new_user = await self.user_registration_repo.create(
                # personal details
                first_name=user_dict["first_name"], 
                middle_name=user_dict["middle_name"], 
                last_name=user_dict["last_name"],
                suffix=user_dict["suffix"],
                age=user_dict["age"],
                gender=user_dict["gender"],
                complete_address=user_dict["complete_address"], 
                # account details
                email=user_dict["email"], 
                cellphone_number=user_dict["cellphone_number"],
                password_hash=user_dict["password_hash"], 
                failed_attempts=0,
                is_active=False,
                # discriminator
                role=user_dict["role"],
                # [Approved, Rejected, Pending]
                status=UserStatus.PENDING
            )

            return new_user
            
        except DuplicateEntryException:
            raise
        except Exception as e:
            logger.error(f"An error occured: {e}")
            raise InternalServerError("An expected error occured.")
        