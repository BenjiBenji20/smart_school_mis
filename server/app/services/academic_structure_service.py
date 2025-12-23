"""
    Date Written: 12/22/2025 at 8:31 PM
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date, datetime, timezone

from app.schemas.academic_structure_schema import *
from app.exceptions.customed_exception import *
from app.schemas.generic_schema import GenericResponse

from app.repository.academic_structure.department_repository import DepartmentRepository
from app.repository.academic_structure.program_repository import ProgramRepository
from app.repository.academic_structure.curriculum_repository import CurriculumRepository
from app.repository.academic_structure.course_repository import CourseRepository
from app.repository.academic_structure.curriculum_course_repository import CurriculumCourseRepository
from app.repository.academic_structure.term_repository import TermRepository

from app.models.academic_structures.term import Term


class AcademicStructureService:
    """
        Services exclusive only to registrar role.
            - Register new department
            - Register new programs
            - Register new curriculum
            - Register new courses
            - Register new curriculum courses
            - Register new terms
            - Update term's status
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        
        self.department_repo = DepartmentRepository(db)
        self.program_repo = ProgramRepository(db)
        self.curriculum_repo = CurriculumRepository(db)
        self.course_repo = CourseRepository(db)
        self.curriculum_course_repo = CurriculumCourseRepository(db)
        self.term_repo = TermRepository(db)
        
        
    async def register_department(
        self,
        department: RegisterDepartmentRequestSchema,
        requested_by: str
    ) -> RegisterDepartmentResponseSchema:
        """
            Register one department at a time
            to avoid spamming.
            
            Using DepartmentRepository.
        """
        department_dict = department.model_dump()
        
        # register department
        register_department = await self.department_repo.create(
            title=department_dict["title"],
            department_code=department_dict["department_code"].upper(),
            description=department_dict["description"]
        )
        
        return RegisterDepartmentResponseSchema(
            id=register_department.id,
            created_at=register_department.created_at,
            title=register_department.title,
            department_code=register_department.department_code.upper(),
            description=register_department.description,
            request_log=GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Register department {register_department.title}"
            )
        )
        
        
    async def register_program(
        self, 
        programs: List[RegisterProgramRequestSchema], 
        requested_by: str
    ) -> List[RegisterProgramResponseSchema]:
        """
            Register one or multiple program (Registrar role only) 
        """
        payload: list[dict] = []

        for program in programs:
            data = program.model_dump()

            if data.get("program_code"):
                data["program_code"] = data["program_code"].upper()

            payload.append(data)
            
        # register programs all at once
        registered_programs = await self.program_repo.create_many(payload)
        
        if registered_programs is None:
            raise UnprocessibleContentException(
                "Program registration failed. Try again."
            )
        
        response: List[RegisterProgramResponseSchema] = []
        
        for program in registered_programs:
            response.append(
                RegisterProgramResponseSchema(
                    id=str(program.id),
                    created_at=program.created_at,
                    title=program.title,
                    program_code=program.program_code,
                    description=program.description,
                    department_id=program.department_id,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                        requested_by=requested_by,
                        description=f"Register program {program.title}"
                    )
                )
            )

        return response
    
    
    async def register_curriculum(
        self,
        curriculum: RegisterCurriculumRequestSchema,
        requested_by: str
    ) -> RegisterCurriculumResponseSchema:
        """
            Register one curriculum at a time
            to avoid spamming.
            
            Using CurriculumRepository.
        """
        curriculum_dict = curriculum.model_dump()
        
        # register curriculum
        register_curriculum = await self.curriculum_repo.create(
            title = curriculum_dict["title"],
            effective_from = curriculum_dict["effective_from"],
            effective_to = curriculum_dict["effective_to"],
            status = curriculum_dict["status"],
            program_id = curriculum_dict["program_id"]
        )
        
        return RegisterCurriculumResponseSchema(
            id=register_curriculum.id,
            created_at=register_curriculum.created_at,
            title=register_curriculum.title,
            effective_from=register_curriculum.effective_from,
            effective_to=register_curriculum.effective_to,
            status=register_curriculum.status,
            program_id=register_curriculum.program_id,
            request_log=GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Register curriculum {register_curriculum.title}"
            )
        )
        
        
    async def register_course(
        self, 
        courses: List[RegisterCourseRequestSchema], 
        requested_by: str
    ) -> List[RegisterCourseResponseSchema]:
        """
            Register courses 
        
            :param courses: list of courses (can be 1)
            :type courses: List[Course]
            :return: with appropriate data log
            :rtype: RegisterCourseResponseSchema
        """
        payload: list[dict] = []

        for course in courses:
            data = course.model_dump()

            if data.get("course_code"):
                data["course_code"] = data["course_code"].upper()

            payload.append(data)
            
        # register courses all at once
        registered_courses = await self.course_repo.create_many(payload)
        
        if registered_courses is None:
            raise UnprocessibleContentException(
                "Course registration failed. Try again."
            )
        
        response: List[RegisterCourseResponseSchema] = []
        
        for course in registered_courses:
            response.append(
                RegisterCourseResponseSchema(
                    id=str(course.id),
                    created_at=course.created_at,
                    title=course.title,
                    course_code=course.course_code,
                    units=course.units,
                    description=course.description,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                        requested_by=requested_by,
                        description=f"Register course {course.title}"
                    )
                )
            )

        return response
    
    
    async def register_curriculum_course(
        self, 
        curriculum_courses: List[RegisterCurriculumCourseRequestSchema], 
        requested_by: str
    ) -> List[RegisterCurriculumCourseResponseSchema]:
        """
            Register one or multiple curriculum courses (Registrar only) 
        
            :param courses: list of courses (can be 1)
            :type courses: List[Course]
            :return: with appropriate data log
            :rtype: RegisterCurriculumCourseResponseSchema
        """
        payload: list[dict] = []

        for curriculum_course in curriculum_courses:
            data = curriculum_course.model_dump()
            payload.append(data)
            
        # register curriculum courses all at once
        registered_curriculum_courses = await self.curriculum_course_repo.create_many(payload)
        
        if registered_curriculum_courses is None:
            raise UnprocessibleContentException(
                "Curriculum course registration failed. Try again."
            )
        
        response: List[RegisterCurriculumCourseResponseSchema] = []
        
        for curriculum_course in registered_curriculum_courses:
            response.append(
                RegisterCurriculumCourseResponseSchema(
                    id=str(curriculum_course.id),
                    created_at=curriculum_course.created_at,
                    year_level=curriculum_course.year_level,
                    semester=curriculum_course.semester,
                    is_required=curriculum_course.is_required,
                    curriculum_id=curriculum_course.curriculum_id,
                    course_id=curriculum_course.course_id,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                        requested_by=requested_by,
                        description=f"Register curriculum course."
                    )
                )
            )

        return response
    
    
    async def register_term(
        self, 
        terms: List[TermRequestSchema], 
        requested_by: str
    ) -> List[TermResponseSchema]:
        """
            Register one or multiple terms (Registrar only) 
        
            :param courses: list of terms (can be 1)
            :return: with appropriate data log
            :rtype: RegisterTermResponseSchema
        """
        payload: list[dict] = []

        for term in terms:
            data = term.model_dump()
            payload.append(data)
            
        # register terms all at once
        registered_terms = await self.term_repo.create_many(payload)
        
        if registered_terms is None:
            raise UnprocessibleContentException(
                "Term registration failed. Try again."
            )
        
        response: List[TermResponseSchema] = []
        
        for term in registered_terms:
            response.append(
                TermResponseSchema(
                    id=str(term.id),
                    created_at=term.created_at,
                    academic_year_start=term.academic_year_start,
                    academic_year_end=term.academic_year_end,
                    enrollment_start=term.enrollment_start,
                    enrollment_end=term.enrollment_end,
                    semester_period=term.semester_period,
                    status=term.status,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                        requested_by=requested_by,
                        description=f"Register term."
                    )
                )
            )

        return response
  
  
    async def update_term_status(
        self,
        id: str,
        status: TermStatus,
        requested_by: str
    ) -> GenericResponse:
        """
            Manage term status allowed only for registrar role.
            term has default DRAFT status when its first created.
            registrar must manage it according to status needed.
            
            param: id: for the target term to manage
            param: status: the status to be switch by the term
        """
        term: Term = await self.term_repo.get_by_id(id)
        
        if not term:
            raise ResourceNotFoundException(f"Term not found.")
        
        # invalidate update if current term status is the same with request.
        if status == term.status:
            return GenericResponse(
                success=False,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Term is already {status.value.lower()}. No actions happened."
            )
  
        # update the term's status
        await self.term_repo.update(
            id=id,
            status=status
        )
        
        return GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Term status successfully updated to {status.value.lower()}."
            )
        
        
    async def get_active_year_term(
        self,
        requested_by: str
    ) -> List[TermResponseSchema]:
        """
            Get active terms.
            Terms that has status of OPEN and within or in the current 
            academic_year_start and academic_year_end.
        """
        current_year = int(date.today().year)
        active_terms = await self.term_repo.get_active_year_term(current_year)
        
        response: List[TermResponseSchema] = []
        
        for term in active_terms:
            response.append(
                TermResponseSchema(
                    id=str(term.id),
                    created_at=term.created_at,
                    academic_year_start=term.academic_year_start,
                    academic_year_end=term.academic_year_end,
                    enrollment_start=term.enrollment_start,
                    enrollment_end=term.enrollment_end,
                    semester_period=term.semester_period,
                    status=term.status,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                        requested_by=requested_by,
                        description=f"Get active terms within the current year {current_year} and status open."
                    )
                )
            )

        return response
    
    
    async def get_active_enrollment(
        self,
        requested_by: str
    ) -> List[TermResponseSchema]:
        """
            Get active enrollments.
            Enrollments that has status of OPEN and within or in the current 
            enrollment_start and enrollment_end.
        """
        current_datetime = datetime.now(timezone.utc)
        active_terms = await self.term_repo.get_active_enrollment(current_datetime)
        
        response: List[TermResponseSchema] = []
        
        for term in active_terms:
            response.append(
                TermResponseSchema(
                    id=str(term.id),
                    created_at=term.created_at,
                    academic_year_start=term.academic_year_start,
                    academic_year_end=term.academic_year_end,
                    enrollment_start=term.enrollment_start,
                    enrollment_end=term.enrollment_end,
                    semester_period=term.semester_period,
                    status=term.status,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                        requested_by=requested_by,
                        description=f"Get active terms within the enrollment {current_datetime.strftime('%m/%d/%Y %H:%M')} and status open."
                    )
                )
            )

        return response
    