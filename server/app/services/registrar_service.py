"""
    Date Written: 12/22/2025 at 8:31 PM
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timezone

from app.repository.course_repository import CourseRepository
from app.schemas.academic_structure_schema import RegisterCourseRequestSchema, RegisterCourseResponseSchema
from app.models.academic_structures.course import Course
from app.exceptions.customed_exception import *
from app.schemas.generic_schema import GenericResponse

class RegistrarService:
    """
        Services exclusive only to registrar role.
        - Register new courses
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        
        self.course_repo = CourseRepository(db)
        
        
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
        