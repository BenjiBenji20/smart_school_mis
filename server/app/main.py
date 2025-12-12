"""
    Date written: 12/6/2025 at 2:23 PM
"""

from fastapi import FastAPI

from contextlib import asynccontextmanager

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


# models - pending users
from app.models.users.pending_users.pending_enrollee import PendingEnrollee
from app.models.users.pending_users.pending_dean import PendingDean
from app.models.users.pending_users.pending_program_chair import PendingProgramChair
from app.models.users.pending_users.pending_professor import PendingProfessor
from app.models.users.pending_users.pending_registrar import PendingRegistrar


# models - Academic Structures
from app.models.academic_structures.class_section import ClassSection
from app.models.academic_structures.course import Course
from app.models.academic_structures.department import Department
from app.models.academic_structures.program import Program
from app.models.academic_structures.professor_class_section import professor_class_section


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


@asynccontextmanager
async def life_span(app: FastAPI):
    try:
        async with engine.begin() as conn:
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
