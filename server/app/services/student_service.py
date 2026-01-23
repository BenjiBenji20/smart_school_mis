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
from app.repository.academic_structures.course_offering_repository import CourseOfferingRepository

from app.models.academic_structures.term import Term
from app.models.users.student import Student


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
        self.course_offering_repo = CourseOfferingRepository(db)
        
        self.enrollment_service = EnrollmentGradingService(db)

    async def get_current_student_user(self, student_id: str) -> StudentResponseSchema:
        student: Student = await self.student_repo.get_student_by_id(student_id)
        if student is None:
            raise ResourceNotFoundException("Student user not found.")
        
        return StudentResponseSchema(
            id=student.id,
            created_at=student.created_at,
            first_name=student.first_name,
            middle_name=student.middle_name,
            last_name=student.last_name,
            suffix=student.suffix,
            age=student.age,
            gender=student.gender,
            complete_address=student.complete_address,
            email=student.email,
            cellphone_number=student.cellphone_number,
            role=student.role,
            is_active=student.is_active,
            university_code=student.university_code,
            status=student.status,
            last_school_attended=student.last_school_attended,
            program_enrolled_date=student.program_enrolled_date,
            year_level=student.year_level
        )
    
    
    async def get_my_current_enrollments(self, student_id: str) -> List[AllowedEnrollSectionResponseSchema]:
        enrollments: List[AllowedEnrollSectionResponseSchema] = await self.student_repo.get_student_current_enrolled_section(
            student_id
        )
        
        if len(enrollments) < 1:
            return []
            
        return enrollments
    
    
    async def get_my_current_term(self, student_id: str) -> TermResponseSchema:
        """
            Get the current enrolled term of student
        """
        current_term: Term = await self.term_repo.get_student_current_term(student_id)
        if current_term is None:
            raise ResourceNotFoundException("Student doesn't enrolled to any term.")
        
        return TermResponseSchema(
            id=current_term.id,
            created_at=current_term.created_at,
            academic_year_start=current_term.academic_year_start, 
            academic_year_end=current_term.academic_year_end,
            enrollment_start=current_term.enrollment_start,
            enrollment_end=current_term.enrollment_end,
            semester_period=current_term.semester_period,
            status=current_term.status,
        )
    
    
    async def get_my_next_term(self, student_id: str) -> TermResponseSchema:
        """
            Get the next term of student that needed to be enrolled
        """
        next_term: Term = await self.term_repo.get_student_next_term(student_id)
        if next_term is None:
            raise ResourceNotFoundException("Student doesn't enrolled to any term.")
        
        return TermResponseSchema(
            id=next_term.id,
            created_at=next_term.created_at,
            academic_year_start=next_term.academic_year_start, 
            academic_year_end=next_term.academic_year_end,
            enrollment_start=next_term.enrollment_start,
            enrollment_end=next_term.enrollment_end,
            semester_period=next_term.semester_period,
            status=next_term.status,
        )

    
    async def remove_enrollment(
        self,
        student_id: str,
        class_section_id: str 
    ) -> List[AllowedEnrollSectionResponseSchema]:
        print(class_section_id)
        """
            Remove enrolled section that doesn't yet approved
        """
        print(f"\n\nCLASS SECTION ID TO REMOVE: {class_section_id}\n\n")
        print(f"\n\nSTUDENT ID TO REMOVE: {student_id}\n\n")
        await self.student_repo.remove_enrollment(
            student_id=student_id, class_section_id=class_section_id
        )
        
        # fetch current enrolled list 
        enrollments: List[AllowedEnrollSectionResponseSchema] = await self.student_repo.get_student_current_enrolled_section(
            student_id
        )
        
        if len(enrollments) < 1:
            return []
            
        return enrollments
    