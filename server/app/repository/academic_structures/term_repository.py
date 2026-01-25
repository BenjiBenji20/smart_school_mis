"""
    Date Written: 12/23/2025 at 6:07 PM
"""

from datetime import datetime, timezone
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, case, exists, or_, select

from app.repository.base_repository import BaseRepository
from app.models.academic_structures.term import Term
from app.models.enums.academic_structure_state import SemesterPeriod, TermStatus
from app.models.enrollment_and_gradings.enrollment import Enrollment
from app.models.academic_structures.course_offering import CourseOffering
from app.models.academic_structures.curriculum import Curriculum
from app.models.academic_structures.curriculum_course import CurriculumCourse


class TermRepository(BaseRepository[Term]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Term, db)
        
        
    async def get_active_year_term(self, current_year: int) -> List[Term]:
        """
            Get active terms.
            Terms that has status of OPEN and within or in the current 
            academic_year_start and academic_year_end.
        """
        query = select(Term).where(
            and_(
                Term.academic_year_end >= current_year,
                Term.status == TermStatus.OPEN
            )
        )
        
        results = await self.db.execute(query)
        return results.scalars().all()
    
    
    async def get_active_enrollment(self, current_datetime: datetime) -> List[Term]:
        """
            Get active enrollments.
            Enrollments that has status of OPEN and within or in the current 
            enrollment_start and enrollment_end.
        """
        query = select(Term).where(
            and_(
                Term.enrollment_start <= current_datetime,
                Term.enrollment_end >= current_datetime,
                Term.status == TermStatus.OPEN
            )
        )
        
        results = await self.db.execute(query)
        return results.scalars().all()


    async def get_student_current_term(self, student_id: str) -> Term | None:
        """
            Get the current (on going) enrolled term of student
        """
        now = datetime.now(timezone.utc)

        stmt = (
            select(Term)
            .join(Enrollment, Enrollment.term_id == Term.id)
            .where(
                and_(
                    Enrollment.student_id == student_id,
                    Term.status == TermStatus.OPEN,
                    Term.enrollment_start <= now,
                    Term.enrollment_end >= now
                )
            )
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    
    async def get_student_next_term(self, student_id: str) -> Term | None:
        """
            Get the next term of student that needed to be enrolled
        """
        current_term_subq = (
            select(Term)
            .join(Enrollment, Enrollment.term_id == Term.id)
            .where(Enrollment.student_id == student_id)
            .order_by(
                Term.academic_year_start.desc(),
                case(
                    (Term.semester_period == SemesterPeriod.SUMMER, 3),
                    (Term.semester_period == SemesterPeriod.SECOND, 2),
                    else_=1
                ).desc()
            )
            .limit(1)
            .subquery()
        )

        stmt = (
            select(Term)
                .where(
                    or_(
                        # NEXT semester in SAME academic year
                        and_(
                            Term.academic_year_start == current_term_subq.c.academic_year_start,
                            case(
                                (Term.semester_period == SemesterPeriod.FIRST, 1),
                                (Term.semester_period == SemesterPeriod.SECOND, 2),
                                else_=3
                            )
                            >
                            case(
                                (current_term_subq.c.semester_period == SemesterPeriod.FIRST, 1),
                                (current_term_subq.c.semester_period == SemesterPeriod.SECOND, 2),
                                else_=3
                            )
                        ),

                        # FIRST semester of NEXT academic year
                        and_(
                            Term.academic_year_start == current_term_subq.c.academic_year_end,
                            Term.semester_period == SemesterPeriod.FIRST
                        )
                    ),
                    Term.status == TermStatus.OPEN
                )
                .order_by(
                    Term.academic_year_start,
                    case(
                        (Term.semester_period == SemesterPeriod.FIRST, 1),
                        (Term.semester_period == SemesterPeriod.SECOND, 2),
                        else_=3
                    )
                )
                .limit(1)
        )

        result = await self.db.execute(stmt)
        return result.scalars().first()


    async def get_term_based_program(self, term_id: str, program_id: str) -> Term:
        """
            Read term based on program
        """
        stmt = (
            select(Term)
            .join(CourseOffering, CourseOffering.term_id == Term.id)
            .join(CurriculumCourse, CurriculumCourse.id == CourseOffering.curriculum_course_id)
            .join(Curriculum, Curriculum.id == CurriculumCourse.curriculum_id)
            .where(
                and_(
                    Term.id == term_id,
                    Curriculum.program_id == program_id
                )
            )
        )
        
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
        