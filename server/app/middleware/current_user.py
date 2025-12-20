from typing import Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

import jwt

from app.db.db_session import get_async_db
from app.models.users.base_user import BaseUser
from app.configs.settings import settings
from app.exceptions.customed_exception import *
from app.repository.auth_repository import AuthRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/authenticate/token")

async def get_current_user(
    user_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
) -> Optional[BaseUser]:
    try:
        user_repo = AuthRepository(db)
        
        payload: dict = jwt.decode(user_token, str(settings.JWT_SECRET_KEY), settings.JWT_ALGORITHM)
        email = payload.get("sub")

        if email is None:
            raise InvalidTokenException("Invalid session")
        
    except JWTError:
        raise UnauthorizedAccessException("Could not validate credentials")
    
    user: Optional[BaseUser] = await user_repo.get_user_by_email(email=email)
    if not user:
        raise ResourceNotFoundException(f"User with email {email} not found")
    
    return user
