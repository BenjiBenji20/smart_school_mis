"""
    Date Written: 12/14/2025 at 3:58 AM
"""

from fastapi import APIRouter, Request, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.schemas.token_schema import RefreshTokenResponseSchema, TokenResponseSchema
from app.models.users.base_user import BaseUser
from app.exceptions.customed_exception import *
from app.db.db_session import get_async_db
from app.services.auth_service import AuthService
from app.schemas.user_schema import BaseUserRequestSchema, BaseUserResponseSchema

logger = logging.getLogger(__name__)

auth_router = APIRouter(
  prefix="/api/user",
  tags=["General user authentication router"]
)

logger = logging.getLogger(__name__)

@auth_router.post("/registration", response_model=BaseUserResponseSchema)
async def user_registration_router(user: BaseUserRequestSchema, db: AsyncSession = Depends(get_async_db)):
    try:
        registration_service = AuthService(db)
        new_user: BaseUserResponseSchema = await registration_service.user_registration_service(user)
        if not new_user:
            raise UnprocessibleContentException("Value error")
        
        return new_user
    except DuplicateEntryException as e:
          logger.warning(f"Duplicate entry attempt: {e}")
          raise
    except UnprocessibleContentException as e:
        logger.warning(f"Unprocessible content: {e}")
        raise
    except InternalServerError as e:
        logger.error(f"Internal server error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in registration: {e}", exc_info=True)
        raise InternalServerError("An unexpected error occurred during registration")


@auth_router.post("/authenticate/token", response_model=TokenResponseSchema)
async def auth_token_router(
  response: Response,
  user_cred_data: OAuth2PasswordRequestForm = Depends(),
  db: AsyncSession = Depends(get_async_db)
):
    try:
        auth_service = AuthService(db)
        
        user: Optional[BaseUser] = await auth_service.auth_token_service(
            user_cred_data.username,
            user_cred_data.password, 
        )
        
        if not user:
            raise UnauthorizedAccessException("Invalid email or password")
        
        payload={
            "sub": user.email,
            "banned_until": user.banned_until.isoformat() if user.banned_until else None
        }
        
        # generate and get tokens
        access_token: str = auth_service.generate_access_token(payload)
        refresh_token: str = auth_service.generate_refresh_token({"sub": user.email})
        
        # attach token as http-only cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,       
            secure=True,         
            samesite="lax",       
            max_age=7*24*60*60,  # 7 days
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "role": user.role
        }
    except (UnauthorizedAccessException, ResourceNotFoundException) as e:
        logger.error("Authentication failed: %s", str(e))
        raise UnauthorizedAccessException("Invalid email or password")
    except Exception as e:
        logger.error("Unexpected error during authentication: %s", str(e))
        raise InternalServerError("An error occurred during authentication")
  

@auth_router.post("/authenticate/refresh-token", response_model=RefreshTokenResponseSchema)
async def refresh_access_token_route(request: Request, db: AsyncSession = Depends(get_async_db)):
    """Get the refresh token from request body or cookies"""
    try:
        auth_service = AuthService(db)
        token = request.cookies.get("refresh_token")
        
        if not token:
            raise InvalidTokenException("No refresh token provided")
        
        return auth_service.refresh_token(token)
    except Exception:
        # Handle specific refresh token errors appropriately
        raise InvalidTokenException("Invalid or expired refresh token")
