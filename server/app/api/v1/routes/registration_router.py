"""
    Date Written: 12/14/2025 at 4:51 AM
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import logging

from app.exceptions.customed_exception import *
from app.db.db_session import get_async_db
from app.schemas.base_user_schema import *
from app.services.registration_service import RegistrationService

registration_router = APIRouter(
  prefix="/api/user",
  tags=["user API endpoints"]
)


logger = logging.getLogger(__name__)

@registration_router.post("/registration", response_model=BaseUserResponseSchema)
async def user_registration_router(user: BaseUserRequestSchema, db: AsyncSession = Depends(get_async_db)):
    try:
        registration_service = RegistrationService(db)
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