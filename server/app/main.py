"""
    Date written: 12/6/2025 at 2:23 PM
"""

from fastapi import FastAPI

from contextlib import asynccontextmanager

from sqlalchemy import text

from app.db.db_session import engine
from app.db.base import Base
from app.configs.settings import settings

# models - Users
from app.models.users.base_user import BaseUser
from app.models.users.administrator import Administrator
from app.models.users.dean import Dean
from app.models.users.professor import Professor
from app.models.users.program_chair import ProgramChair
from app.models.users.registrar import Registrar
from app.models.users.student import Student


# models - Academic Structures
from app.models.academic_structures.class_section import ClassSection
from app.models.academic_structures.course import Course
from app.models.academic_structures.department import Department
from app.models.academic_structures.program import Program
from app.models.academic_structures.professor_class_section import ProfessorClassSection
from app.models.academic_structures.course_offering import CourseOffering
from app.models.academic_structures.curriculum import Curriculum
from app.models.academic_structures.curriculum_course import CurriculumCourse
from app.models.academic_structures.term import Term
from app.models.academic_structures.class_schedule import ClassSchedule


# models - Location
from app.models.locations.building import Building
from app.models.locations.room import Room


# models - Announcements
from app.models.announcements.announcement import Announcement


# models - Cheating Detections
from app.models.cheating_detections.cheating_incident import CheatingIncident


# models - Enrollment and Grading
from app.models.enrollment_and_gradings.enrollment import Enrollment
from app.models.enrollment_and_gradings.student_grade import StudentGrade


# models - Exams
from app.models.exams.exam import Exam
from app.models.exams.exam_session import ExamSession


# models - Student Tasks
from app.models.student_tasks.task import Task
from app.models.student_tasks.task_submission import TaskSubmission


# # models - Face Recognitions
from app.models.face_recognitions.face_encoding import FaceEncoding


# routers
from app.api.v1.routes.auth_router import auth_router
from app.api.v1.routes.face_recognition_router import face_recognition_router
from app.api.v1.routes.base_user_router import base_user_router
from app.api.v1.routes.academic_structure_router import academic_structure_router
from app.api.v1.routes.professor_router import prof_router
from app.api.v1.routes.dean_router import dean_router
from app.api.v1.routes.program_chair_router import program_chair_router


# middlewares
from app.middleware.filter_jwt import FilterJWT


from app.exceptions.customed_exception import *
from app.exceptions.error_handler import *


@asynccontextmanager
async def life_span(app: FastAPI):
    try:
        async with engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

            print("\n\nRDBMS table are created successfully!")
            
        yield
        
    finally:
        await engine.dispose()
        print("\n\nRDBMS engine disposed...")
        print("Application shutdown...")
        

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=life_span
)

#middleware
app.add_middleware(FilterJWT)


# router registration
app.include_router(auth_router)
app.include_router(face_recognition_router)
app.include_router(base_user_router)
app.include_router(academic_structure_router)
app.include_router(prof_router)
app.include_router(dean_router)
app.include_router(program_chair_router)


# regiustering global exeception handler
app.add_exception_handler(InternalServerError, internal_server_error_handler)
app.add_exception_handler(UnprocessibleContentException, unprocessible_content_handler)
app.add_exception_handler(ResourceNotFoundException, resource_not_found_handler)
app.add_exception_handler(DuplicateEntryException, duplicate_entry_exception_handler)
app.add_exception_handler(UnauthorizedAccessException, unauthorized_access_handler)
app.add_exception_handler(ForbiddenAccessException, forbidden_access_handler)
app.add_exception_handler(InvalidTokenException, invalid_token_handler)
app.add_exception_handler(InvalidRequestException, invalid_request_handler)
