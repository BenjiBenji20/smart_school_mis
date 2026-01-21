"""
    Date Written: 12/28/2025 at 11:00 AM
"""

from typing import List, Optional
from sqlalchemy import and_, case, exists, func, select, label
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
from sqlalchemy.orm import aliased
from app.models.academic_structures.class_schedule import ClassSchedule
from app.models.academic_structures.course import Course
from app.models.academic_structures.professor_class_section import ProfessorClassSection
from app.models.locations.room import Room
from app.models.users.professor import Professor
from app.models.users.base_user import BaseUser
from app.schemas.enrollments_and_gradings_schema import AllowedEnrollSectionResponseSchema
from app.models.enums.enrollment_and_grading_state import EnrollmentStatus


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
    

    async def get_student_allowed_sections(
        self,
        student_id: str
    ) -> List[AllowedEnrollSectionResponseSchema]:
        """
            Read all the allowed sections of student.
            Class Sections must be of these followings:
            - Courses must be under the student's program
            - Courses must be isn't taken by the student [not sure about this]
        """
        StudentUser = aliased(BaseUser)
        ProfessorUser = aliased(BaseUser)

        StudentTbl = aliased(Student)
        ProfessorTbl = aliased(Professor)

        enrolled_subq = (
            select(1)
            .where(
                and_(
                    Enrollment.student_id == student_id,
                    Enrollment.class_section_id == ClassSection.id
                )
            )
            .exists()
        )

        stmt = (
            select(
                Course.course_code,
                Course.title,
                Course.units,
                ClassSection.id.label("class_section_id"),
                ClassSection.section_code,
                ClassSchedule.day_of_week,
                ClassSchedule.start_time,
                ClassSchedule.end_time,
                Room.room_code,
                case(
                    (
                        ProfessorUser.middle_name.isnot(None),
                        func.concat(
                            ProfessorUser.first_name, ' ',
                            ProfessorUser.middle_name, ' ',
                            ProfessorUser.last_name
                        )
                    ),
                    else_=func.concat(
                        ProfessorUser.first_name, ' ',
                        ProfessorUser.last_name
                    )
                ).label("assigned_professor")
            )
            .select_from(Course)

            .join(CurriculumCourse, CurriculumCourse.course_id == Course.id)
            .join(CourseOffering, CourseOffering.curriculum_course_id == CurriculumCourse.id)
            .join(ClassSection, ClassSection.course_offering_id == CourseOffering.id)

            # LEFT JOIN
            .outerjoin(ClassSchedule, ClassSchedule.class_section_id == ClassSection.id)
            .outerjoin(Room, Room.id == ClassSchedule.room_id)

            .outerjoin(
                ProfessorClassSection,
                ProfessorClassSection.class_section_id == ClassSection.id
            )
            .outerjoin(ProfessorTbl, ProfessorTbl.id == ProfessorClassSection.professor_id)
            .outerjoin(ProfessorUser, ProfessorUser.id == ProfessorTbl.id)

            .join(Curriculum, Curriculum.id == CurriculumCourse.curriculum_id)
            .join(StudentTbl, StudentTbl.program_id == Curriculum.program_id)
            .join(StudentUser, StudentUser.id == StudentTbl.id)

            .where(
                and_(
                    StudentTbl.id == student_id,
                    CourseOffering.status == CourseOfferingStatus.APPROVED,
                    ~enrolled_subq
                )
            )

            .order_by(
                Course.course_code,
                ClassSection.section_code,
                ClassSchedule.day_of_week,
                ClassSchedule.start_time
            )
        )

        result = await self.db.execute(stmt)

        return [
            AllowedEnrollSectionResponseSchema(
                class_section_id=r.class_section_id,
                course_code=r.course_code,
                title=r.title,
                units=r.units,
                section_code=r.section_code,
                day_of_week=r.day_of_week,
                start_time=r.start_time,
                end_time=r.end_time,
                room_code=r.room_code,
                assigned_professor=r.assigned_professor
            )
            for r in result.all()
        ]
        
        
    async def get_student_current_enrolled_section(
        self,
        student_id: str
    ) -> List[AllowedEnrollSectionResponseSchema]:
        """
        Get all currently enrolled sections for a student.
        This returns sections where the student is actually enrolled.
        """
        StudentUser = aliased(BaseUser)
        ProfessorUser = aliased(BaseUser)
        
        ProfessorTbl = aliased(Professor)
        
        stmt = (
            select(
                Course.course_code,
                Course.title,
                Course.units,
                ClassSection.id.label("class_section_id"),
                ClassSection.section_code,
                ClassSchedule.day_of_week,
                ClassSchedule.start_time,
                ClassSchedule.end_time,
                Room.room_code,
                case(
                    (
                        ProfessorUser.middle_name.isnot(None),
                        func.concat(
                            ProfessorUser.first_name, ' ',
                            ProfessorUser.middle_name, ' ',
                            ProfessorUser.last_name
                        )
                    ),
                    else_=func.concat(
                        ProfessorUser.first_name, ' ',
                        ProfessorUser.last_name
                    )
                ).label("assigned_professor"),
                Enrollment.status.label("enrollment_status")
            )
            .select_from(Enrollment)  # Start from Enrollment table since student is enrolled
            
            # Join to get class section details
            .join(ClassSection, ClassSection.id == Enrollment.class_section_id)
            .join(CourseOffering, CourseOffering.id == ClassSection.course_offering_id)
            .join(CurriculumCourse, CurriculumCourse.id == CourseOffering.curriculum_course_id)
            .join(Course, Course.id == CurriculumCourse.course_id)
            
            # LEFT JOIN for schedule and room
            .outerjoin(ClassSchedule, ClassSchedule.class_section_id == ClassSection.id)
            .outerjoin(Room, Room.id == ClassSchedule.room_id)
            
            # LEFT JOIN for professor info
            .outerjoin(
                ProfessorClassSection,
                ProfessorClassSection.class_section_id == ClassSection.id
            )
            .outerjoin(ProfessorTbl, ProfessorTbl.id == ProfessorClassSection.professor_id)
            .outerjoin(ProfessorUser, ProfessorUser.id == ProfessorTbl.id)
            
            # Filter for this specific student
            .where(
                and_(
                    Enrollment.student_id == student_id,
                    # Enrollment.status == EnrollmentStatus.APPROVED,  # Only approved enrollments
                    CourseOffering.status == CourseOfferingStatus.APPROVED,
                    # Optionally filter by current term/semester
                    # CourseOffering.term_id == current_term_id,
                )
            )
            
            .order_by(
                Course.course_code,
                ClassSection.section_code,
                ClassSchedule.day_of_week,
                ClassSchedule.start_time
            )
        )
        
        result = await self.db.execute(stmt)
        
        return [
            AllowedEnrollSectionResponseSchema(
                class_section_id=r.class_section_id,
                course_code=r.course_code,
                title=r.title,
                units=r.units,
                section_code=r.section_code,
                day_of_week=r.day_of_week,
                start_time=r.start_time,
                end_time=r.end_time,
                room_code=r.room_code,
                assigned_professor=r.assigned_professor
            )
            for r in result.all()
        ]


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
    