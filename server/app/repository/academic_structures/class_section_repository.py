"""
    Date Written: 12/24/2025 at 4:21 PM
"""

from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.models.academic_structures.class_section import ClassSection
from app.schemas.academic_structure_schema import ClassSectionRequestSchema
from app.models.enums.academic_structure_state import CourseOfferingStatus, TermStatus
from app.exceptions.customed_exception import *

from app.repository.base_repository import BaseRepository
from app.repository.academic_structures.course_offering_repository import CourseOfferingRepository
from app.repository.academic_structures.term_repository import TermRepository
from app.models.enrollment_and_gradings.enrollment import Enrollment


class ClassSectionRepository(BaseRepository[ClassSection]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ClassSection, db)
        self.course_offering_repo = CourseOfferingRepository(db)
        self.term_repo = TermRepository(db)
        
        
    async def register_many_class_section(
        self,
        class_sections: List[ClassSectionRequestSchema]
    ) -> Optional[List[ClassSection]]:
        """
            Register one or multiple class section at the same time.
                Constraints:
                    CourseOffering.status = APPROVED
                    Term.status = OPEN
                    capacity > 0
                    unique section_code per CourseOffering
        """
        instances: List[Dict] = []
        
        for class_section in class_sections:
            # check for class section capacity
            # invalidate if 0 capacity to avoid spamming of class section registration
            if class_section.student_capacity <= 0:
                raise InvalidRequestException(
                    f"Registration of class section {class_section.section_code.upper()} " 
                    f"failed due to class section capacity {class_section.student_capacity}"
                )
            
            # check the course offering status
            course_offering_id = class_section.course_offering_id
            course_offering = await self.course_offering_repo.get_by_id(course_offering_id)
            
            if not course_offering:
                raise ResourceNotFoundException(
                    f"Registration of class section {class_section.section_code.upper()} "
                    f"failed due to course offering not found"
                )
            
            if course_offering.status != CourseOfferingStatus.APPROVED:
                raise InvalidRequestException(
                    f"Registration of class section {class_section.section_code.upper()} " 
                    f"failed due to class section status {course_offering.status.lower()}"
                )
            
            # check the term status
            term = await self.term_repo.get_by_id(course_offering.term_id)
            
            if not term:
                raise ResourceNotFoundException(
                    f"Registration of class section {class_section.section_code.upper()} "
                    f"failed due to course offering not found"
                )
            
            if term.status != TermStatus.OPEN:
                raise InvalidRequestException(
                    f"Registration of class section {class_section.section_code.upper()} " 
                    f"failed due to class section status {term.status.lower()}"
                )

            # appendd 1 instance to the list
            c_s_dict = class_section.model_dump()
            instances.append(c_s_dict)
            
        # create class sections all at the same time
        self.db.add_all(instances)
        await self.db.commit()
        for instance in instances:
            await self.db.refresh(instance)
        return instances


    async def current_student_count(self, class_section_id: str) -> int:
        stmt = (
            select(func.count(Enrollment.id))
            .where(Enrollment.class_section_id == class_section_id)
        )

        result = await self.db.execute(stmt)
        return result.scalar_one()
