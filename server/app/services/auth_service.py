"""
    Date Written: 12/14/2025 at 4:15 AM
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

import hashlib
from passlib.context import CryptContext
import jwt

import logging

from app.configs.settings import settings
from app.exceptions.customed_exception import *
from app.models.users.base_user import BaseUser
from app.repository.auth_repository import AuthRepository
from app.models.enums.user_state import UserStatus
from app.schemas.base_user_schema import BaseUserRequestSchema, BaseUserResponseSchema

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.auth_repo = AuthRepository(db=db)

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
            is_user_exists = await self.auth_repo.is_email_exists(user.email)
            # if exists, invalidate the registration
            if is_user_exists:
                raise DuplicateEntryException(f"User with {user.email} as email already exists.")
            
            hashed_pw = self.hash_password(user.password)

            user_dict = user.model_dump(exclude={"password"})  
            user_dict["password_hash"] = hashed_pw
            role = user_dict.pop("role")
            new_user = await self.auth_repo.register_user_by_role(
                role=role,
                **user_dict
            )

            return new_user
            
        except DuplicateEntryException:
            raise
        except Exception as e:
            logger.error(f"An error occured: {e}")
            raise InternalServerError("An expected error occured.")

    
    def validate_password(self, plain_password: str, hashed_password: str) -> bool:
        """
            hash password into cryptograph
            validates plain password by comparing it to hashed password 
            (hashed pass will be decoded first so it will be compare in full string type)
        """
        pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )
        
        password_bytes = plain_password.encode("utf-8")
        sha256_hash = hashlib.sha256(password_bytes).hexdigest()
        return pwd_context.verify(sha256_hash, hashed_password)


    def validate_user_status(self, user_status: UserStatus) -> bool:
        return user_status.value == "Approved"


    async def auth_token_service(self, email: str, password: str) -> Optional[BaseUser]:
        try:
            user: Optional[BaseUser] = await self.auth_repo.get_user_by_email(email=email)
            if not user:
                raise ResourceNotFoundException(f"User with email: {email} not found.")
            
            now = datetime.now(timezone.utc)
            
            # check user status if approved as user
            if not self.validate_user_status(user.status):
                raise UnauthorizedAccessException(f"Please wait for your registration to be approved.")
            
            # Check if user is banned
            if user.banned_until:
                banned_until_aware = user.banned_until.replace(tzinfo=timezone.utc)
                if banned_until_aware > now:
                    raise UnauthorizedAccessException(f"User is banned until {user.banned_until}.")
                
            # if failed attempts persists due to wrong password, increment failed_attempts attribute
            if not self.validate_password(password, user.password_hash):
                user.failed_attempts += 1

                # Ban user if max attempts reached
                if user.failed_attempts >= settings.MAX_FAILED_ATTEMPTS:
                    user.banned_until = now + timedelta(minutes=settings.BAN_DURATION_MINUTES)
                    # response ban time in minutes
                    ban_duration: timedelta = user.banned_until - now
                    ban_minutes = int(ban_duration.total_seconds() / 60)
                    user.failed_attempts = 0  # reset to avoid stacking bans
                    await self.db.commit()
                    raise UnauthorizedAccessException(f"Banned for {ban_minutes} minutes")

                await self.db.commit()
                raise UnauthorizedAccessException("Invalid email or password.")
        
            # Reset failed attempts on success
            user.failed_attempts = 0
            user.banned_until = None
            user.last_login = now
            user.is_active = True
            await self.db.commit()

            return user
        except (UnauthorizedAccessException, ResourceNotFoundException) as e:
            logger.error("Authentication failed: %s", str(e))
            raise
        except Exception as e:
            logger.error("Unexpected error during authentication: %s", str(e))
            raise InternalServerError("An error occurred during authentication")
    
    
    def generate_access_token(self, payload: dict) -> str:
        """Generate short lived token exp: 15 mins"""
        # 15mins access token
        token_expiration = datetime.now(timezone.utc) + timedelta(minutes=15)

        # 7 days refresh token
        payload.update({
            "exp": int(token_expiration.timestamp()),
            "type": "access"
        })
        encoded_jwt = jwt.encode(payload, str(settings.JWT_SECRET_KEY), algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt


    def generate_refresh_token(self, payload: dict) -> str:
        """Generate long live token exp: 7 days"""
        # 7 days refresh token
        token_expiration = datetime.now(timezone.utc) + timedelta(days=7)
        payload.update({
            "exp": int(token_expiration.timestamp()),
            "type": "refresh"
        })
        encoded_jwt = jwt.encode(payload, str(settings.JWT_SECRET_KEY), algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt


    def refresh_token(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(refresh_token, str(settings.JWT_SECRET_KEY), algorithms=settings.JWT_ALGORITHM)

            if payload.get("type") != "refresh":
                raise UnauthorizedAccessException("Invalid token type.")

            if datetime.now(timezone.utc).timestamp() > payload["exp"]:
                raise UnauthorizedAccessException("Refresh token expired.")

            email = payload.get("sub")
            if not email:
                raise UnauthorizedAccessException("Invalid refresh token.")

            # Recreate access token only
            new_access_token = self.generate_access_token({
                "sub": email
            })

            return {
                "access_token": new_access_token,
                "token_type": "bearer"
            }

        except JWTError:
            raise UnauthorizedAccessException("Invalid refresh token.")
    