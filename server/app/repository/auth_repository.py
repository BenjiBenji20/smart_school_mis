"""
    Date Written: 12/14/2025 at 4:20 AM
"""

from datetime import date
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import Optional

from app.models.users.base_user import BaseUser
from app.exceptions.customed_exception import *
from app.models.enums.user_state import UserRole, UserStatus
from app.repository.base_repository import BaseRepository

class AuthRepository(BaseRepository[BaseUser]):
    """
        Repository for authentication operations.
        Using BaseUser model as polymorphic accross all users.
    """
    
    def __init__(self, db: AsyncSession):
        super().__init__(BaseUser, db)
        self.db = db
    
    async def is_email_exists(self, email: str) -> bool:
        """Check if email is already registered."""
        result = await self.db.execute(
            select(BaseUser).where(BaseUser.email == email).limit(1)
        )
        return result.scalars().first() is not None
    
    
    async def register_user_by_role(self, role: UserRole, **user_data) -> BaseUser:
        """
            Create user with the correct polymorphic model based on role.
            This ensures the child table record is created.
        """
        # Import here to avoid circular imports
        from app.models.users.administrator import Administrator
        from app.models.users.registrar import Registrar
        from app.models.users.dean import Dean
        from app.models.users.program_chair import ProgramChair
        from app.models.users.professor import Professor
        from app.models.users.student import Student
        
        # Map role to model class
        role_model_map = {
            UserRole.ADMINISTRATOR: Administrator,
            UserRole.REGISTRAR: Registrar,
            UserRole.DEAN: Dean,
            UserRole.PROGRAM_CHAIR: ProgramChair,
            UserRole.PROFESSOR: Professor,
            UserRole.STUDENT: Student,
        }
        
        # Get the correct model class
        model_class = role_model_map.get(role)
        
        if not model_class:
            raise InvalidRequestException(f"Invalid role: {role}")
        
        # Create instance of CHILD model (not BaseUser)
        # This will create records in BOTH base_user AND child table
        instance = model_class(**user_data)
        
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        
        return instance
    
    
    async def approve_pending_registration(
        self, approved_by: str, user_role: Optional[UserRole], id: str
    ) -> bool:
        """
            Only user with higher role  can approved the user with lower role.
            
            :param approved_by: by whome the user approved
            :type approved_by: str
            :param role: the role of user to be approved
            :type enum UserRole: 
            :param id: the user to be approved
            :type id: str
            :return: to flag wheather the user is successfully approved
            :rtype: bool
        """
        result = await self.db.execute(
            select(BaseUser).where(BaseUser.id == id).limit(1)
        )
        
        user_to_approved: BaseUser = result.scalar_one_or_none()
        
        if user_to_approved is None:
            raise ResourceNotFoundException("User not found.")

        if user_to_approved.status != UserStatus.PENDING:
            raise InvalidRequestException("User is in pending approval. Please wait.")
        
        # update status
        user_to_approved.status = UserStatus.APPROVED
        user_to_approved.approved_by = approved_by
        
        # user cannot change its role during approval
        if user_role and user_role != user_to_approved.role:
            raise InvalidRequestException(
                "Role cannot be changed after registration. "
                "User must re-register with correct role."
            )
            
        user_to_approved.university_code = self.generate_university_number(user_to_approved.role)
        await self.db.commit()
        return True
    
    
    # ==== HELPER FUNCTIONS ====
    def generate_university_number(self, role: UserRole) -> str:
        role_code = ""
        if role == UserRole.ADMINISTRATOR: role_code = "ADMN"
        elif role == UserRole.REGISTRAR: role_code = "RGTR"
        elif role == UserRole.DEAN: role_code = "DEAN"
        elif role == UserRole.PROGRAM_CHAIR: role_code = "PRGC"
        elif role == UserRole.PROFESSOR: role_code = "PROF"
        else: role_code = "STDT"
        
        today = date.today().strftime("%m%d%Y")
        rand = str(random.randint(0, 999)).zfill(4)

        return role_code + today + rand
    
    
    async def get_user_by_email(self, email: str) -> Optional[BaseUser]:
        """
            Get any user by email (works for all user types).
            Returns the actual subclass instance (Student, Professor, etc.)
        """
        result = await self.db.execute(
            select(BaseUser).where(BaseUser.email == email)
        )
        return result.scalars().first()
    
    
    async def get_user_by_university_code(self, university_code: str) -> Optional[BaseUser]:
        """
            Find user using its unique university code. 
            Use for: authentication 
        """
        result = await self.db.execute(
            select(BaseUser).where(BaseUser.university_code == university_code)
        )
        return result.scalars().first()
    

    async def get_active_user_by_email(self, email: str) -> Optional[BaseUser]:
        """Get active user by email."""
        result = await self.db.execute(
            select(BaseUser).where(
                BaseUser.email == email,
                BaseUser.is_active == True
            )
        )
        return result.scalars().first()
    