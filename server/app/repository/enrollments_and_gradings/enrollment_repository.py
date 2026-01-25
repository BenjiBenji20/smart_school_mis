"""
    Date Written: 12/26/2025 at 4:22 PM
"""

from sqlalchemy import case, func, select, update
from sqlalchemy.orm import aliased
from typing import Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.base_repository import BaseRepository
from app.models.enrollment_and_gradings.enrollment import Enrollment
from app.exceptions.customed_exception import *
from app.models.academic_structures.class_section import ClassSection
from app.models.academic_structures.course_offering import CourseOffering
from app.models.academic_structures.curriculum import Curriculum
from app.models.academic_structures.curriculum_course import CurriculumCourse
from app.models.academic_structures.department import Department
from app.models.academic_structures.program import Program
from app.models.enums.enrollment_and_grading_state import EnrollmentStatus
from app.models.users.base_user import BaseUser
from app.models.users.professor import Professor
from app.models.users.student import Student
from app.models.academic_structures.class_schedule import ClassSchedule
from app.models.academic_structures.course import Course
from app.models.academic_structures.professor_class_section import ProfessorClassSection
from app.models.academic_structures.term import Term
from app.models.locations.room import Room


class EnrollmentRepository(BaseRepository[Enrollment]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Enrollment, db)
        
        
    async def get_all_enrollments(self) -> List[Any]:
        """
            Return all the enrollments with the rows needed:
            - enrollment_id
            - student_id
            - student_first_name
            - student_middle_name
            - student_last_name
            - class_section_id
            - course_code
            - title
            - units
            - section_code
            - term_id
            - semester_period
            - academic_year_start
            - academic_year_end
            - program_id
            - program_code
            - enrollment_status
        """
        StudentUser = aliased(BaseUser)
        ProfessorUser = aliased(BaseUser)
        StudentTbl = aliased(Student)
        ProfessorTbl = aliased(Professor)
        
        stmt = (
            select(
                Enrollment.id.label("enrollment_id"),
                Enrollment.student_id,
                ClassSection.id.label("class_section_id"),
                Term.id.label("term_id"),
                Program.id.label("program_id"),
                Enrollment.status.label("enrollment_status"),
                ClassSection.section_code,
                Course.course_code,
                Course.title,
                Course.units,
                ClassSchedule.day_of_week,
                ClassSchedule.start_time,
                ClassSchedule.end_time,
                Room.room_code,
                Term.semester_period,
                Term.academic_year_start,
                Term.academic_year_end,
                Program.program_code,
                case(
                    (
                        StudentUser.middle_name.isnot(None),
                        func.concat(
                            StudentUser.first_name, ' ',
                            StudentUser.middle_name, ' ',
                            StudentUser.last_name
                        )
                    ),
                    else_=func.concat(
                        StudentUser.first_name, ' ',
                        StudentUser.last_name
                    )
                ).label("student_name"),
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
            .select_from(Enrollment)
            .join(StudentTbl, StudentTbl.id == Enrollment.student_id)
            .join(StudentUser, StudentUser.id == StudentTbl.id)
            .join(ClassSection, ClassSection.id == Enrollment.class_section_id)
            .join(CourseOffering, CourseOffering.id == ClassSection.course_offering_id)
            .join(CurriculumCourse, CurriculumCourse.id == CourseOffering.curriculum_course_id)
            .join(Course, Course.id == CurriculumCourse.course_id)
            .join(Curriculum, Curriculum.id == CurriculumCourse.curriculum_id)
            .join(Program, Program.id == Curriculum.program_id)
            .join(Term, Term.id == Enrollment.term_id)
            # LEFT JOINs for optional data
            .outerjoin(ClassSchedule, ClassSchedule.class_section_id == ClassSection.id)
            .outerjoin(Room, Room.id == ClassSchedule.room_id)
            .outerjoin(
                ProfessorClassSection,
                ProfessorClassSection.class_section_id == ClassSection.id
            )
            .outerjoin(ProfessorTbl, ProfessorTbl.id == ProfessorClassSection.professor_id)
            .outerjoin(ProfessorUser, ProfessorUser.id == ProfessorTbl.id)
            .order_by(
                Enrollment.created_at.desc(),
                Course.course_code,
                ClassSection.section_code
            )
        )
    
        result = await self.db.execute(stmt)
        return result.all()
        
        
    async def get_filtered_enrollments(
        self,
        department_id: Optional[str] = None,
        program_id: Optional[str] = None,
        class_section_id: Optional[str] = None,
        term_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        desc: bool = False
    ) -> List[Any]: 
        """
            Get filtered enrollment based on:
            department, program and term
        """
        StudentUser = aliased(BaseUser)
        ProfessorUser = aliased(BaseUser)
        StudentTbl = aliased(Student)
        ProfessorTbl = aliased(Professor)
        
        # Build base query with ALL necessary joins
        stmt = (
            select(
                Enrollment.id.label("enrollment_id"),
                Enrollment.student_id,
                ClassSection.id.label("class_section_id"),
                Term.id.label("term_id"),
                Program.id.label("program_id"),
                Enrollment.status.label("enrollment_status"),
                ClassSection.section_code,
                Course.course_code,
                Course.title,
                Course.units,
                ClassSchedule.day_of_week,
                ClassSchedule.start_time,
                ClassSchedule.end_time,
                Room.room_code,
                Term.semester_period,
                Term.academic_year_start,
                Term.academic_year_end,
                Program.program_code,
                case(
                    (
                        StudentUser.middle_name.isnot(None),
                        func.concat(
                            StudentUser.first_name, ' ',
                            StudentUser.middle_name, ' ',
                            StudentUser.last_name
                        )
                    ),
                    else_=func.concat(
                        StudentUser.first_name, ' ',
                        StudentUser.last_name
                    )
                ).label("student_name"),
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
            )
            .select_from(Enrollment)
            
            # REQUIRED JOINS
            .join(ClassSection, Enrollment.class_section_id == ClassSection.id)
            .join(Term, Enrollment.term_id == Term.id)
            .join(CourseOffering, ClassSection.course_offering_id == CourseOffering.id)
            .join(CurriculumCourse, CourseOffering.curriculum_course_id == CurriculumCourse.id)
            .join(Course, CurriculumCourse.course_id == Course.id)
            .join(Curriculum, CurriculumCourse.curriculum_id == Curriculum.id)
            .join(Program, Curriculum.program_id == Program.id)
            .join(Department, Program.department_id == Department.id)
            
            # Student join
            .join(StudentTbl, StudentTbl.id == Enrollment.student_id)
            .join(StudentUser, StudentUser.id == StudentTbl.id)
            
            # LEFT JOINS
            .outerjoin(ClassSchedule, ClassSchedule.class_section_id == ClassSection.id)
            .outerjoin(Room, Room.id == ClassSchedule.room_id)
            .outerjoin(
                ProfessorClassSection, 
                ProfessorClassSection.class_section_id == ClassSection.id
            )
            .outerjoin(ProfessorTbl, ProfessorTbl.id == ProfessorClassSection.professor_id)
            .outerjoin(ProfessorUser, ProfessorUser.id == ProfessorTbl.id)
        )
        
        # Apply filters AFTER all joins are defined
        if term_id:
            stmt = stmt.where(Term.id == term_id) 
        
        if class_section_id:
            stmt = stmt.where(ClassSection.id == class_section_id)
        
        if program_id:
            stmt = stmt.where(Program.id == program_id)
        
        if department_id:
            stmt = stmt.where(Department.id == department_id)
        
        # Default ordering
        stmt = stmt.order_by(
            Enrollment.created_at.desc(),
            Course.course_code,
            ClassSection.section_code
        )
        
        # Custom ordering if specified
        if order_by:
            # Map order_by string to actual column
            order_map = {
                'course_code': Course.course_code,
                'section_code': ClassSection.section_code,
                'student_name': StudentUser.last_name, 
                'created_at': Enrollment.created_at,
            }
            
            order_column = order_map.get(order_by)
            if order_column:
                stmt = stmt.order_by(order_column.desc() if desc else order_column)
        
        # Pagination
        stmt = stmt.offset(skip).limit(limit)
        
        # Execute and return results
        result = await self.db.execute(stmt)
        return result.all()

        
    async def update_enrollments_status(
        self,
        enrollment_ids: List[str],
        status: EnrollmentStatus
    ) -> List[Any]:
        """
            Bulk update enrollment status.
            - Skips records that already have the target status
            - Returns only updated Enrollment rows
        """
        # Update only rows that actually need updating
        stmt = (
            update(Enrollment)
            .where(
                Enrollment.id.in_(enrollment_ids),
                Enrollment.status != status  # skip if enrollment record status == param status 
            )
            .values(status=status)
            .returning(Enrollment)
        )

        result = await self.db.execute(stmt)
        # commit the update
        await self.db.commit()
        
        updated_ids = [row[0] for row in result.all()]
    
        # Commit the update
        await self.db.commit()
        
        # If no rows were updated, return empty list
        if not updated_ids:
            return []
        
        return await self.get_all_enrollments()
        
    
    async def list_enrollment_by_status(self, enrollment_status: EnrollmentStatus) -> List[Enrollment]:
        stmt = select(Enrollment).where(
            Enrollment.status == enrollment_status
        )
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
    