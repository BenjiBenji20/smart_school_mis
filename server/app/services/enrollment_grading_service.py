"""
    Date Written: 12/28/2025 at 9:05 AM
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timezone

from app.schemas.academic_structure_schema import *
from app.schemas.enrollments_and_gradings_schema import *
from app.exceptions.customed_exception import *
from app.schemas.generic_schema import GenericResponse

from app.repository.academic_structures.course_repository import CourseRepository
from app.repository.academic_structures.term_repository import TermRepository
from app.repository.academic_structures.course_offering_repository import CourseOfferingRepository
from app.repository.academic_structures.class_section_repository import ClassSectionRepository
from app.repository.users.student_repository import StudentRepository
from app.repository.enrollments_and_gradings.enrollment_repository import EnrollmentRepository

from app.models.academic_structures.term import Term
from app.models.academic_structures.course_offering import CourseOffering
from app.models.academic_structures.class_section import ClassSection
from app.models.users.student import Student
from app.models.enrollment_and_gradings.enrollment import Enrollment
from app.services.academic_structure_service import AcademicStructureService


class EnrollmentGradingService:
    """
        Services list for enrollment and grading services.
            - Read student allowed class sections
            - Enroll student to class section
            - Read all enrollments
            - Read filtered enrollments
            - Update status of enrollments
            - List enrollment by status
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        
        self.course_repo = CourseRepository(db)
        self.term_repo = TermRepository(db)
        self.course_offering_repo = CourseOfferingRepository(db)
        self.class_section_repo = ClassSectionRepository(db)
        self.student_repo = StudentRepository(db)
        self.enrollment_repo = EnrollmentRepository(db)
        
        self.academic_structure_service = AcademicStructureService(db) 


    async def get_student_allowed_sections(
        self, 
        student_id: str, 
        requested_by: str
    ) -> List[AllowedEnrollSectionResponseSchema]:
        """
        Read all the allowed sections to enroll by the student.
        Class Sections must be of these followings:
        - Courses must be under the student's program
        - Courses must not be already taken by the student
        """
        # Use the flattened repo method that returns the data directly
        allowed_sections: List[AllowedEnrollSectionResponseSchema] = (
            await self.student_repo.get_student_allowed_sections(student_id)
        )
        
        if not allowed_sections:
            raise InvalidRequestException(
                f"No available class sections found for student {student_id}"
            )
        
        return allowed_sections
        
     
    async def format_enrollment_response(
        self,
        status: EnrollmentStatus,
        student: Student, 
        class_section: ClassSection,
        course_offering: CourseOffering,
        term: Term,
        requested_by: str = "",
        description: str = "",
        
    ) -> EnrollmentResponseSchema:
        return EnrollmentResponseSchema(
            status=status,
            student=StudentResponseSchema(
                id=str(student.id),
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
            ),
            class_section_details=await self.academic_structure_service.format_class_section_response(
                class_section=class_section,
                course_offering=course_offering
            ),
            term=TermResponseSchema(
                id=str(term.id),
                created_at=term.created_at,
                academic_year_start=term.academic_year_start, 
                academic_year_end=term.academic_year_end,
                enrollment_start=term.enrollment_start,
                enrollment_end=term.enrollment_end,
                semester_period=term.semester_period,
                status=term.status
            ),
            request_log=GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=description
            )
        )
        

    async def enroll_student_class_section(
        self,
        student_id: str,
        class_section_id: str,
        requested_by: str
    ) -> EnrollmentResponseSchema:
        
        """
            Student enrollment.
            Validations:
                Student not already enrolled
                Section not full
                ClassSection.status == OPEN
                CourseOffering.status == APPROVED
                Term.status == OPEN
                Curriculum compatibility
                Update current student count of class section

        """
        # validation: Student not already/currently enrolled to the section
        enrolled_sections: List[AllowedEnrollSectionResponseSchema] = await self.student_repo.get_student_current_enrolled_section(
            student_id
        )
        
        for section in enrolled_sections:
            if section.class_section_id == class_section_id:
                raise InvalidRequestException(
                    f"Enrollment failed due to student already enrolled to {section.section_code}."
                )
                
        # validation: section is not full if adding 1 student
        class_section: ClassSection = await self.class_section_repo.get_by_id(class_section_id)
        if class_section.current_student_cnt + 1 >= class_section.student_capacity:
            raise InvalidRequestException(
                f"Enrollment failed due to class section {class_section.section_code} already full."
            )
        
        # validation: section status must be open
        if class_section.status != ClassSectionStatus.OPEN:
            raise InvalidRequestException(
                f"Enrollment failed due to {class_section.section_code} is currently "
                f"{class_section.status.lower()}."
            )
    
        # validation: course offerings must be approved
        course_offering: CourseOffering = await self.course_offering_repo.get_by_id(
            class_section.course_offering_id
        )
        if course_offering.status != CourseOfferingStatus.APPROVED:
            raise InvalidRequestException(
                f"Enrollment failed due to course offer status is currently {course_offering.status.lower()}."
            )
        
        # validation: enrollment term must be open
        term: Term = await self.term_repo.get_by_id(course_offering.term_id)
        if term.status != TermStatus.OPEN:
            raise InvalidRequestException(
                f"Enrollment failed due to term status is currently {term.status.lower()}."
            )
        
        # validation: class section curriculum course compatibility to the student's program
        is_curriculum_compatible = await self.student_repo.validate_section_curriculum_compatibility(
            student_id, class_section_id
        )
        if not is_curriculum_compatible:
            raise InvalidRequestException(
                f"Enrollment failed due to class section curriculum imcompatibility."
            )
        
        student: Student = await self.student_repo.get_student_by_id(student_id)
        if not student:
            raise ResourceNotFoundException(f"Student not found by id: {student_id}.")
        
        enrollment: Enrollment = await self.enrollment_repo.create(
            status=EnrollmentStatus.PENDING,
            student_id=student_id,
            class_section_id=class_section_id,
            term_id=term.id
        )
        
        # update class section count before return
        class_section.current_student_cnt = await self.class_section_repo.current_student_count(
                class_section.id
            ) + 1 # add count every class section registration
        
        await self.class_section_repo.update(
            id=class_section.id,
            current_student_cnt=class_section.current_student_cnt
        )
        
        # format and return the enrollment
        return await self.format_enrollment_response(
            status=enrollment.status,
            student=student,
            class_section=class_section,
            course_offering=course_offering,
            term=term,
            requested_by=requested_by,
            description="Student enrollment request."
        )
        
        
    async def get_all_enrollments(self) -> List[EnrollmentResponseSchema]:
        """
            Read all student enrollment (Registrar role only)
        """
        enrollments: List[Enrollment] = await self.enrollment_repo.get_all()
        response: List[EnrollmentResponseSchema] = []
        
        for enrollment in enrollments:
            student: Student = await self.student_repo.get_student_by_id(enrollment.student_id)
            class_section: ClassSection = await self.class_section_repo.get_by_id(enrollment.class_section_id)
            course_offering: CourseOffering = await self.course_offering_repo.get_by_id(class_section.course_offering_id)
            term: Term = await self.term_repo.get_by_id(enrollment.term_id)
        
            response.append(
                await self.format_enrollment_response(
                    status=enrollment.status,
                    student=student,
                    class_section=class_section,
                    course_offering=course_offering,
                    term=term,
                    description="Read all student enrollments."
                )
            )
        
        return response
           
        
    async def get_filtered_enrollments(
        self,
        department_id: str = None,
        program_id: str = None,
        class_section_id: str = None,
        term_id: str = None,
    ) -> List[EnrollmentResponseSchema]:
        """
            Get filtered enrollment based on:
                [status] not yet implemented, department, program and term
        """
        enrollments: List[Enrollment] = await self.enrollment_repo.get_filtered_enrollments(
            department_id, program_id, class_section_id, term_id
        )
        response: List[EnrollmentResponseSchema] = []
        
        for enrollment in enrollments:
            student: Student = await self.student_repo.get_student_by_id(enrollment.student_id)
            class_section: ClassSection = await self.class_section_repo.get_by_id(enrollment.class_section_id)
            course_offering: CourseOffering = await self.course_offering_repo.get_by_id(class_section.course_offering_id)
            term: Term = await self.term_repo.get_by_id(enrollment.term_id)
        
            response.append(
                await self.format_enrollment_response(
                    status=enrollment.status,
                    student=student,
                    class_section=class_section,
                    course_offering=course_offering,
                    term=term,
                    description="Filter enrollments."
                )
            )
        
        return response
        
    
    async def update_enrollment_status(
        self,
        enrollments: UpdateEnrollmentStatusSchema,
        requested_by: str = ""
    ) -> List[EnrollmentResponseSchema]:
        """
            Update multiple enrollments (registrar role only)
                All the enrollment (through id) will be updated using 1 status
        """
        updated_enrollments_status: List[Enrollment] = await self.enrollment_repo.update_enrollments_status(
            enrollment_ids=enrollments.enrollment_ids,
            status=enrollments.status
        )
        response: List[EnrollmentResponseSchema] = []
        
        for enrollment in updated_enrollments_status:
            student: Student = await self.student_repo.get_student_by_id(enrollment.student_id)
            class_section: ClassSection = await self.class_section_repo.get_by_id(enrollment.class_section_id)
            course_offering: CourseOffering = await self.course_offering_repo.get_by_id(class_section.course_offering_id)
            term: Term = await self.term_repo.get_by_id(enrollment.term_id)
        
            response.append(
                await self.format_enrollment_response(
                    status=enrollment.status,
                    student=student,
                    class_section=class_section,
                    course_offering=course_offering,
                    term=term,
                    description="Updated enrollment status."
                )
            )
        
        return response  
    
    
    async def list_enrollment_by_status(self, enrollment_status: EnrollmentStatus) -> List[EnrollmentResponseSchema]:
        response: List[EnrollmentResponseSchema] = []
        enrollments = await self.enrollment_repo.list_enrollment_by_status(enrollment_status)
        
        for enrollment in enrollments:
            student: Student = await self.student_repo.get_student_by_id(enrollment.student_id)
            class_section: ClassSection = await self.class_section_repo.get_by_id(enrollment.class_section_id)
            course_offering: CourseOffering = await self.course_offering_repo.get_by_id(class_section.course_offering_id)
            term: Term = await self.term_repo.get_by_id(enrollment.term_id)
        
            response.append(
                await self.format_enrollment_response(
                    status=enrollment.status,
                    student=student,
                    class_section=class_section,
                    course_offering=course_offering,
                    term=term,
                    description="List all the enrollments based on status."
                )
            )
        
        return response  
    