"""
    Date Written: 12/28/2025 at 11:00 AM
"""

from typing import List, Optional
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.users.student import Student
from app.models.enums.user_state import UserStatus
from app.exceptions.customed_exception import *
from app.models.academic_structures.class_section import ClassSection
from app.models.academic_structures.course_offering import CourseOffering
from app.models.academic_structures.curriculum import Curriculum
from app.models.academic_structures.curriculum_course import CurriculumCourse
from app.models.academic_structures.program import Program
from app.models.enrollment_and_gradings.enrollment import Enrollment
from app.models.enums.academic_structure_state import CourseOfferingStatus


class StudentRepository(BaseRepository[Student]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Student, db)
        
        
    async def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """
            Get student by ID.
            This will JOIN base_user and student tables automatically.
        """
        result = await self.db.execute(
            select(Student).where(Student.id == student_id)
        )
        return result.scalars().first()
    
    
    async def get_active_students(self) -> List[Student]:
        """Get all active students."""
        result = await self.db.execute(
            select(Student).where(
                Student.status == UserStatus.APPROVED
            )
        )
        return result.scalars().all()
    
    
    async def get_student_allowed_sections(self, student_id: str) -> Optional[List[ClassSection]]:
        """
            Read all the allowed sections of student.
            Class Sections must be of these followings:
            - Courses must be under the student's program
            - Courses must be isn't taken by the student [not sure about this]
        """
        # class section -> FK course_offering -> course_offering -> 
        # FK curriculum_course_id -> curriculum -> FK program <- student
        stmt = (
            select(ClassSection)
            .join(CourseOffering, ClassSection.course_offering_id == CourseOffering.id)
            .join(CurriculumCourse, CourseOffering.curriculum_course_id == CurriculumCourse.id)
            .join(Curriculum, CurriculumCourse.curriculum_id == Curriculum.id)
            .join(Student, Student.program_id == Curriculum.program_id)
                .where(
                    Student.id == student_id,
                    CourseOffering.status == CourseOfferingStatus.APPROVED
                )
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    
    async def get_student_current_enrolled_section(self, student_id: str) -> Optional[List[ClassSection]]:
        """
            Get student current enrolled sections
        """
        stmt = (
            select(ClassSection)
            .join(Enrollment, Enrollment.class_section_id == ClassSection.id)
            .where(Enrollment.student_id == student_id)
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().all()


    async def validate_section_curriculum_compatibility(
        self,
        student_id: str,
        class_section_id: str
    ) -> bool:
        stmt = (
            select(
                exists().where(
                    ClassSection.id == class_section_id,
                    ClassSection.course_offering_id == CourseOffering.id,
                    CourseOffering.curriculum_course_id == CurriculumCourse.id,
                    CurriculumCourse.curriculum_id == Curriculum.id,
                    Curriculum.program_id == Student.program_id,
                    Student.id == student_id
                )
            )
        )

        result = await self.db.execute(stmt)
        return result.scalar()