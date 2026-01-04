"""
    Date Written: 1/4/2026 at 4:54 PM
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.academic_structure_schema import *
from app.schemas.enrollments_and_gradings_schema import *
from app.exceptions.customed_exception import *

from app.services.enrollment_grading_service import EnrollmentGradingService

from app.repository.academic_structures.course_repository import CourseRepository
from app.repository.academic_structures.term_repository import TermRepository
from app.repository.academic_structures.class_section_repository import ClassSectionRepository
from app.repository.users.student_repository import StudentRepository

from app.models.academic_structures.term import Term
from app.models.academic_structures.class_section import ClassSection
from app.models.users.student import Student
from app.models.enrollment_and_gradings.enrollment import Enrollment


class StudentService:
    """
        Services list for student user.
            - Get my current enrollments
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        
        self.course_repo = CourseRepository(db)
        self.term_repo = TermRepository(db)
        self.class_section_repo = ClassSectionRepository(db)
        self.student_repo = StudentRepository(db)
        
        self.enrollment_service = EnrollmentGradingService(db)

     
    async def get_my_current_enrollments(self, student_id: str) -> List[EnrollmentResponseSchema]:
        response: List[EnrollmentResponseSchema] = []
        enrollments: List[Enrollment] = await self.student_repo.get_my_current_enrollments(student_id)
        for enrollment in enrollments:
            student: Student = await self.student_repo.get_student_by_id(enrollment.student_id)
            class_section: ClassSection = await self.class_section_repo.get_by_id(enrollment.class_section_id)
            term: Term = await self.term_repo.get_by_id(enrollment.term_id)
        
            response.append(
                self.enrollment_service.format_enrollment_response(
                    status=enrollment.status,
                    student=student,
                    class_section=class_section,
                    term=term,
                    description="Get my enrollments."
                )
            )
            
        return response
    