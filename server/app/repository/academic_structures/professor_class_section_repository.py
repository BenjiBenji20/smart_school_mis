"""
    Date Written: 12/24/2025 at 6:48 PM
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.academic_structures.professor_class_section import ProfessorClassSection
from app.models.enums.user_state import ProfessorStatus, UserRole
from app.schemas.academic_structure_schema import ProfessorClassSectionResponseSchema
from app.exceptions.customed_exception import *

from app.repository.base_repository import BaseRepository
from app.repository.users.professor_repository import ProfessorRepository
from app.models.academic_structures.class_section import ClassSection
from app.models.users.base_user import BaseUser
from app.models.users.professor import Professor

        
class ProfessorClassSectionRepository(BaseRepository[ProfessorClassSection]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ProfessorClassSection, db)
        self.professor_repo = ProfessorRepository(db)
        
      
    async def create_prof_class_sections(self, instances):
        """Create multiple instances"""
        created = []
        for instance_data in instances:
            instance = self.model(**instance_data)
            self.db.add(instance)
            created.append(instance)
        
        await self.db.flush()
        await self.db.commit()
        return created   
       
        
    async def assign_professor_class_section(
        self,
        prof_id: str,
        class_section_ids: List[str],
    ) -> List[ProfessorClassSection]:
        """
            Assign professor to multiple class sections
            - Professor must be ACTIVE
            - No duplicate assignment (handled by UniqueConstraint)
        """
        # Check if professor exists and is active
        professor: Professor = await self.professor_repo.get_professor_by_id(prof_id)
        
        if not professor:
            raise ResourceNotFoundException(
                f"Assignment of class section professor failed "
                f"due to professor with id: {prof_id} not found"
            )
        
        if professor.professor_status != ProfessorStatus.ACTIVE:
            raise InvalidRequestException(
                f"Assignment of class section professor failed "
                f"due to professor has {professor.professor_status.lower()} status."
            )
        # Check for existing assignments
        new_class_section_ids = await self.check_prof_class_section_assignment(
            prof_id, class_section_ids
        )
        
        if not new_class_section_ids:
            raise InvalidRequestException(
                "All specified class sections are already assigned to this professor"
            )
        
        # Prepare instances for bulk insert
        instances = []
        for class_section_id in new_class_section_ids:
            instances.append({
                "professor_id": prof_id,
                "class_section_id": class_section_id
            })
            
        # Create all assignments at once
        created_assignments = await self.create_prof_class_sections(instances)
        
        return created_assignments
    
    
    async def get_professor_class_section_details(
        self,
        assignment_ids: List[str]
    ) -> List[ProfessorClassSectionResponseSchema]:
        """
            Get detailed information for professor-class section assignments
        """
        # Query to join professor, class_section tables
        stmt = select(
                ProfessorClassSection.id.label("id"),
                ProfessorClassSection.created_at.label("created_at"),
                ProfessorClassSection.professor_id.label("professor_id"),
                ProfessorClassSection.class_section_id.label("class_section_id"),
                Professor.professor_status.label("professor_status"),
                BaseUser.first_name.label("first_name"),
                BaseUser.middle_name.label("middle_name"),
                BaseUser.last_name.label("last_name"),
                BaseUser.suffix.label("suffix"),
                BaseUser.university_code.label("university_code"),
                ClassSection.section_code.label("section_code"),
                ClassSection.room_number.label("room_number"),
                ClassSection.student_capacity.label("student_capacity"),
                ClassSection.time_schedule.label("time_schedule"),
                ClassSection.status.label("class_section_status"),
                ClassSection.course_offering_id.label("course_offering_id")
            ).join(
                Professor, ProfessorClassSection.professor_id == Professor.id
            ).join(
                ClassSection, ProfessorClassSection.class_section_id == ClassSection.id
            ).where(
                ProfessorClassSection.id.in_(assignment_ids)
        )
        
        result = await self.db.execute(stmt)
        rows = result.all()
        
        return rows
    
    
    # ===========================================
    # HELPER METHOD: Query professor_class_section
    # ===========================================
    async def check_prof_class_section_assignment(
        self,
        prof_id: str,
        class_section_ids: List[str]
    ) -> List[str]:
        """
            Check existing professor_class_section ids
            with matching FKs to the params: class_section_ids
            return only the class_section_ids that does not yet once matched
            to the same professor.
        """
        stmt = select(ProfessorClassSection.class_section_id).where(
            ProfessorClassSection.professor_id == prof_id,
            ProfessorClassSection.class_section_id.in_(class_section_ids)
        )
        result = await self.db.execute(stmt)
        existing_section_ids = {row[0] for row in result.all()}
        
        # Filter out already assigned sections
        new_class_section_ids = [
            cs_id for cs_id in class_section_ids 
            if cs_id not in existing_section_ids
        ]
        
        return new_class_section_ids
    
    
    async def get_professor_id(self, class_section_id: str) -> str | None:
        result = await self.db.execute(
            select(ProfessorClassSection).where(
                ProfessorClassSection.class_section_id == class_section_id
            )
        )
        
        link = result.scalars().first()
        return link.professor_id
        