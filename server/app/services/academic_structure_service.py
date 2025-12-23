"""
    Date Written: 12/22/2025 at 8:31 PM
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timezone

from app.schemas.academic_structure_schema import *
from app.exceptions.customed_exception import *
from app.schemas.generic_schema import GenericResponse

from app.repository.academic_structure.course_repository import CourseRepository
from app.repository.academic_structure.department_repository import DepartmentRepository
from app.repository.academic_structure.program_repository import ProgramRepository

class AcademicStructureService:
    """
        Services exclusive only to registrar role.
        - Register new department
        - Register new courses
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        
        self.course_repo = CourseRepository(db)
        self.department_repo = DepartmentRepository(db)
        self.program_repo = ProgramRepository(db)
        
        
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
                requested_by=requested_by
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
                        requested_by=requested_by
                    )
                )
            )

        return response
        
        
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
                        requested_by=requested_by
                    )
                )
            )

        return response
        