"""
    Date Written: 12/24/2025 at 11:18 AM
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.course_offering import CourseOffering
from app.models.enums.academic_structure_state import CourseOfferingStatus, CurriculumStatus, TermStatus

from app.repository.academic_structures.curriculum_course_repository import CurriculumCourseRepository
from app.repository.academic_structures.curriculum_repository import CurriculumRepository
from app.repository.academic_structures.term_repository import TermRepository

from app.exceptions.customed_exception import *
from app.models.academic_structures.class_section import ClassSection
from app.models.academic_structures.term import Term


class CourseOfferingRepository(BaseRepository[CourseOffering]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(CourseOffering, db)
        self.curriculum_course_repo = CurriculumCourseRepository(db)
        self.curriculum_repo = CurriculumRepository(db)
        self.term_repo = TermRepository(db)
        
        
    async def register_course_offering(
        self, 
        curriculum_course_id: str,
        term_id: str,
        status: CourseOfferingStatus
    ) -> Optional[CourseOffering]:
        """
            Register course_offering that meets the conditions:
            Curriculum.status = Active
            Term.status = OPEN
            
            else invalidate the registration
        """
         
        # find first the curriculum status
        # first, get the curriculum_course object using the param: curriculum_course_id
        curriculum_course = await self.curriculum_course_repo.get_by_id(curriculum_course_id)
        
        if not curriculum_course:
            raise ResourceNotFoundException(f"Curriculum course not found with id: {curriculum_course_id}")
        
        # second, use the curriculum_id from curriculum_course object to determine its curriculum status
        curriculum = await self.curriculum_repo.get_by_id(curriculum_course.curriculum_id)
        
        # third, validate curriculum status
        if curriculum.status != CurriculumStatus.ACTIVE:
            raise InvalidRequestException(
                f"Registration of course offering failed due to curriculum status {curriculum.status.lower()}"
            )

        # find the term status
        # first, get the term object using the param: term_id
        term: Term = await self.term_repo.get_by_id(term_id)
        
        if not term:
            raise ResourceNotFoundException(f"Term course not found with id: {term_id}")
        
        # second, validate term status
        if term.status != TermStatus.OPEN:
            raise InvalidRequestException(
                f"Registration of course offering failed due to term status {term.status.value}."
            )
            
        instance = CourseOffering(
            curriculum_course_id = curriculum_course_id,
            term_id = term_id,
            status = status
        )
        
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
    
    
    async def get_course_offering(self, class_section_id: str) -> Optional[CourseOffering]:
        result = await self.db.execute(
            select(CourseOffering)
                .join(
                    ClassSection, ClassSection.course_offering_id == CourseOffering.id
                )
                .where(
                    ClassSection.id == class_section_id
                )
        )
        course_offering = result.scalars().first()
        return course_offering
    
    
    async def list_course_offering_by_term(self, term_id: str) -> List[CourseOffering]:
        stmt = select(CourseOffering).where(
            CourseOffering.term_id == term_id
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
        