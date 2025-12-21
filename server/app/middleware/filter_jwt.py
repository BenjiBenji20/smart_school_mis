"""
    Date written: 12/20/2025 at 4:06 PM
"""

from datetime import datetime, timezone
from typing import Optional
from fastapi import Request
import jwt
from starlette.middleware.base import BaseHTTPMiddleware

import logging

from app.exceptions.customed_exception import *
from app.configs.settings import settings
from app.db.db_session import get_async_db
from app.models.users.base_user import BaseUser
from app.repository.auth_repository import AuthRepository
from app.models.enums.user_state import UserStatus

logger = logging.getLogger(__name__)


class FilterJWT(BaseHTTPMiddleware):
    """
        Filter access token for every request to private routes
    """
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # check if path is public uri then no need for token validation
        if match_uri(path):
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.log("\nInvalid token.\nLoc: 2nd validation.\n")
            raise InvalidTokenException("Invalid request.")
        
        # extract jwt access token from header
        access_token = auth_header.split(" ")[1]

        try:
            # decode the payload using the token, secret key and SHA256 algorithm
            payload: dict = jwt.decode(access_token, str(settings.JWT_SECRET_KEY), settings.JWT_ALGORITHM)
            email: str = payload.get("sub")
            
            # validate token expiration
            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload["exp"], tz=timezone.utc):
                logger.error("\nSession expired.\nLoc: 3rd validation.\n")
                raise InvalidTokenException("Invalid request.")
            
            # validate user banned time
            async for db in get_async_db():
                auth_repo = AuthRepository(db)
                user: Optional[BaseUser] = await auth_repo.get_user_by_email(email)
                
            if user is None:
                logger.error("\nUser not found.\nLoc:5th validation.\n")
                raise ResourceNotFoundException(f"User with {email} email not found..")
                
            if not self.validate_user_status(user.status):
                logger.error("\nUser not approved.\nLoc:4th validation.\n")
                raise UnauthorizedAccessException(f"Please wait for your registration to be approved.")
            
            # check if user has banned time
            if user.banned_until and datetime.now(timezone.utc) < user.banned_until.replace(tzinfo=timezone.utc):
                logger.error("\nUser is currently banned.\nLoc: 6th validation.\n")
                raise InvalidRequestException("User is currently banned. You don't have access to this request.")
            
            # validate if user is active/ if not, means the 
            # authentication process doesn't go in /api/user/authentication/token
            # where validation is happened. This guard against session hijacking.
            if not user.is_active:
                logger.error("\nUser is deactivated.\nLoc: 7th validation.\n")
                raise InvalidRequestException("User is deactivated. You don't have access to this request.")

            request.state.user = payload
            
        except (
            InvalidTokenException, InvalidRequestException, 
            UnauthorizedAccessException, ResourceNotFoundException
        ) as e:
            logger.error("\nJWT Filtering failed: %s", str(e))
            raise
        
        except Exception as s:
            logger.critical("\nInternal server error: %s", str(s))
            raise 
        
        # on success to all validations, pass the token to the router
        return await call_next(request)
            
                
    def validate_user_status(self, user_status: UserStatus) -> bool:
        return user_status.value == "Approved"
        

def match_uri(request_route: str) -> bool:
    import re
    
    public_routes = {
        # swagger
        r"/docs",
        r"/openapi.json",
        
        # authentication
        r"/api/user/registration",
        r"/api/user/authenticate/token",
        r"/api/user/authenticate/refresh-token"
    }
    return True if any(re.match(route, request_route) for route in public_routes) else False