"""
    Date Written: 12/26/2025 at 4:22 PM
"""

from sqlalchemy import select, update
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.enrollment_and_gradings.enrollment import Enrollment
from app.exceptions.customed_exception import *
from app.models.academic_structures.class_section import ClassSection
from app.models.academic_structures.course_offering import CourseOffering
from app.models.academic_structures.curriculum import Curriculum
from app.models.academic_structures.curriculum_course import CurriculumCourse
from app.models.academic_structures.department import Department
from app.models.academic_structures.program import Program
from app.models.enums.enrollment_and_grading_state import EnrollmentStatus


class EnrollmentRepository(BaseRepository[Enrollment]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Enrollment, db)
        
        
    async def get_filtered_enrollments(
        self,
        department_id: Optional[str] = None,
        program_id: Optional[str] = None,
        class_section_id: Optional[str] = None,
        term_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        desc: bool = False
    ) -> List[Enrollment]:
        """
            Get filtered enrollment based on:
                department, program and term
        """
        stmt = (
            select(Enrollment)
                .join(ClassSection, Enrollment.class_section_id == ClassSection.id)
                .join(CourseOffering, ClassSection.course_offering_id == CourseOffering.id)
                .join(CurriculumCourse, CourseOffering.curriculum_course_id == CurriculumCourse.id)
                .join(Curriculum, CurriculumCourse.curriculum_id == Curriculum.id)
                .join(Program, Curriculum.program_id == Program.id)
                .join(Department, Program.department_id == Department.id)
        )
        
        # condition filter
        if term_id:
            stmt = stmt.where(Enrollment.term_id == term_id)

        if class_section_id:
            stmt = stmt.where(Enrollment.class_section_id == class_section_id)

        if program_id:
            stmt = stmt.where(Program.id == program_id)

        if department_id:
            stmt = stmt.where(Department.id == department_id)
        
        if order_by:
            ordered_columns = getattr(Enrollment, order_by, None)
            if ordered_columns is not None:
                stmt = stmt.order_by(ordered_columns.desc() if desc else ordered_columns)
        
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()


    async def update_enrollments_status(
        self,
        enrollment_ids: List[str],
        status: EnrollmentStatus
    ) -> List[Enrollment]:
        """
            Bulk update enrollment status.
            - Skips records that already have the target status
            - Returns only updated Enrollment rows
        """

        # Update only rows that actually need updating
        stmt = (
            update(Enrollment)
            .where(
                Enrollment.id.in_(enrollment_ids),
                Enrollment.status != status  # skip if enrollment record status == param status 
            )
            .values(status=status)
            .returning(Enrollment)
        )

        result = await self.db.execute(stmt)
        updated_enrollments = result.scalars().all()
        await self.db.commit()
        return updated_enrollments