"""
    Date Written: 12/22/2025 at 8:31 PM
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date, datetime, timezone

from app.schemas.academic_structure_schema import *
from app.exceptions.customed_exception import *
from app.schemas.generic_schema import GenericResponse

from app.repository.locations.building_repository import BuildingRepository
from app.repository.locations.room_repository import RoomRepository
from app.repository.academic_structures.department_repository import DepartmentRepository
from app.repository.academic_structures.program_repository import ProgramRepository
from app.repository.academic_structures.curriculum_repository import CurriculumRepository
from app.repository.academic_structures.course_repository import CourseRepository
from app.repository.academic_structures.curriculum_course_repository import CurriculumCourseRepository
from app.repository.academic_structures.term_repository import TermRepository
from app.repository.academic_structures.course_offering_repository import CourseOfferingRepository
from app.repository.academic_structures.class_section_repository import ClassSectionRepository
from app.repository.academic_structures.professor_class_section_repository import ProfessorClassSectionRepository
from app.repository.academic_structures.class_schedule_repository import ClassScheduleRepository

from app.models.academic_structures.term import Term
from app.models.academic_structures.course_offering import CourseOffering
from app.models.academic_structures.curriculum import Curriculum
from app.models.academic_structures.department import Department
from app.models.academic_structures.class_schedule import ClassSchedule


class AcademicStructureService:
    """
        Services exclusive only to registrar role.
            - Register new building
            - Register new rooms
            - Register new department
            - Assign department building
            - Register new programs
            - Register new curriculum
            - Update curriculum status
            - Register new courses
            - Register new curriculum courses
            - Register new terms
            - Update term's status
            - Register course offering
            - Update course offerings's status
            - Register class section
            - Assign class section professor
            - Assign a schedule to class section
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        
        self.building_repo = BuildingRepository(db)
        self.room_repo = RoomRepository(db)
        self.department_repo = DepartmentRepository(db)
        self.program_repo = ProgramRepository(db)
        self.curriculum_repo = CurriculumRepository(db)
        self.course_repo = CourseRepository(db)
        self.curriculum_course_repo = CurriculumCourseRepository(db)
        self.term_repo = TermRepository(db)
        self.course_offering_repo = CourseOfferingRepository(db)
        self.class_section_repo = ClassSectionRepository(db)
        self.prof_class_section_repo = ProfessorClassSectionRepository(db)
        self.class_schedule_repo = ClassScheduleRepository(db)
        
        
    async def register_building(
        self,
        building: RegisterBuildingRequestSchema,
        requested_by: str
    ) -> RegisterBuildingResponseSchema:
        """
            Register building
            param building: 
                name: str (building name)
                capacity: int (number of rooms)
        """
        building_dict = building.model_dump()
        
        # register building
        register_building = await self.building_repo.create(
            name=building_dict["name"],
            room_capacity=building_dict["room_capacity"]
        )
        
        return RegisterBuildingResponseSchema(
            id=register_building.id,
            created_at=register_building.created_at,
            name=register_building.name,
            room_capacity=register_building.room_capacity,
            request_log=GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Register building {register_building.name}"
            )
        )
        
        
    async def register_room(
        self,
        rooms: List[RegisterRoomRequestSchema],
        requested_by: str = None
    ) -> List[RegisterRoomResponseSchema]:
        """
            Register room (administrator role)
            param room: 
                room_code: str (room name)
                capacity: int (number of students)
        """
        payload: list[dict] = []

        for room in rooms:
            data = room.model_dump()

            if data.get("room_code"):
                data["room_code"] = data["room_code"].upper()

            payload.append(data)
            
        # register rooms all at once
        registered_rooms = await self.room_repo.create_many(payload)
        
        if registered_rooms is None:
            raise UnprocessibleContentException(
                "Room registration failed. Try again."
            )
        
        response: List[RegisterRoomResponseSchema] = []
        
        for room in registered_rooms:
            response.append(
                RegisterRoomResponseSchema(
                    id=str(room.id),
                    created_at=room.created_at,
                    room_code=room.room_code,
                    section_capacity=room.section_capacity,
                    building_id=room.building_id,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                        requested_by=requested_by,
                        description=f"Register room {room.room_code}"
                    )
                )
            )

        return response
        
        
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
        
        
    async def assign_department_building(
        self,
        department_id: str,
        building_id: str,
        requested_by: str = None
    ) -> GenericResponse:
        """
            Register department to building (administrator role)

            Department <-> Building
            - Department must not have been registered to other building
        """
        # find the department and validate if it was assigned to some building
        department: Department = await self.department_repo.get_by_id(department_id)
        
        if not department:
            raise InvalidRequestException(f"Assignation of department failed.")
        
        # find the building if exist
        building = await self.building_repo.get_by_id(building_id)
        if not building:
            raise ResourceNotFoundException(f"Building not found using id: {building_id}.")
        
        # assign a building to the department
        await self.department_repo.update(
            id=department_id,
            building_id=building_id
        )
        
        return GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Department successfully assigned to building {building.name}."
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
    
    
    async def update_curriculum_status(
        self,
        id: str,
        status: CurriculumStatus,
        requested_by: str
    ) -> GenericResponse:
        """
            Update curriculum status allowed only for registrar role.
            curriculum has default DRAFT status when its first created.
            registrar must manage it according to status needed.
            
            param: id: for the target curriculum to manage
            param: status: the status to be switch by the curriculum
        """
        curriculum: Curriculum = await self.curriculum_repo.get_by_id(id)
        
        if not curriculum:
            raise ResourceNotFoundException(f"curriculum not found.")
        
        # invalidate update if current curriculum status is the same with request.
        if status == curriculum.status:
            return GenericResponse(
                success=False,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Curriculum is already {status.value.lower()}. No actions happened."
            )
  
        # update the curriculum's status
        await self.curriculum_repo.update(
            id=id,
            status=status
        )
        
        return GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Curriculum status successfully updated to {status.value.lower()}."
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
    
    
    async def register_course_offering(
        self,
        course_offering: CourseOfferingRequestSchema,
        requested_by: str
    ) -> CourseOfferingResponseSchema:
        """
            Register course_offering one at a time (Registrar only).
            Registration must meet this conditions:
                Curriculum.status = Active
                Term.status = OPEN
                
                else invalidate the registration
            
            Status is PENDING at registration. 
            Must be update by registrar or dean.
        """
        course_offering_dict = course_offering.model_dump()
        
        # register course offering
        register_course_offering = await self.course_offering_repo.register_course_offering(
            curriculum_course_id = course_offering_dict["curriculum_course_id"],
            term_id = course_offering_dict["term_id"],
            status = course_offering_dict["status"],
        )
        
        if not register_course_offering:
            raise InvalidRequestException("Registration of course offering failed.")
        
        return CourseOfferingResponseSchema(
            id=register_course_offering.id,
            created_at=register_course_offering.created_at,
            curriculum_course_id=register_course_offering.curriculum_course_id,
            term_id=register_course_offering.term_id,
            status=register_course_offering.status,
            request_log=GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Register course offering with status {register_course_offering.status.lower()}"
            )
        )


    async def update_course_offering_status(
        self,
        id: str,
        status: CourseOfferingStatus,
        requested_by: str
    ) -> GenericResponse:
        """
            Manage course offering status allowed only for registrar and dean role.
            Course offering has default PENDING status when its first registered.
            registrar or dean must update it according to status needed.
            
            param: id: for the target course_offering db record to update
            param: status: the status to be switch by the CourseOfferingStatus
        """
        course_offering: CourseOffering = await self.course_offering_repo.get_by_id(id)
        
        if not course_offering:
            raise ResourceNotFoundException(f"course offering not found.")
        
        # invalidate update if current course offering status is the same with request.
        if status == course_offering.status:
            return GenericResponse(
                success=False,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Course offering is already {status.value.lower()}. No actions happened."
            )
  
        # update the course offering's status
        await self.course_offering_repo.update(
            id=id,
            status=status
        )
        
        return GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Course offering status successfully updated to {status.value.lower()}."
            )
        
        
    async def register_class_section(
        self,
        class_sections: List[ClassSectionRequestSchema],
        requested_by: str
    ) -> List[ClassSectionResponseSchema]:
        """
            Register one or multiple class sections at the same time.
        """
        payload: list[dict] = []

        for class_section in class_sections:
            data = class_section.model_dump()

            if data.get("section_code"):
                data["section_code"] = data["section_code"].upper()

            payload.append(data)
            
        # register class sections all at once
        registered_class_sections = await self.class_section_repo.create_many(payload)
        
        if registered_class_sections is None:
            raise UnprocessibleContentException(
                "Class section registration failed. Try again."
            )
        
        response: List[ClassSectionResponseSchema] = []
        
        for class_section in registered_class_sections:
            response.append(
                ClassSectionResponseSchema(
                    id=str(class_section.id),
                    created_at=class_section.created_at,
                    course_offering_id=class_section.course_offering_id,
                    section_code=class_section.section_code,
                    student_capacity=class_section.student_capacity,
                    status=class_section.status,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                        requested_by=requested_by,
                        description=f"Register class section {class_section.section_code}"
                    )
                )
            )

        return response
        
        
    async def assign_class_section_professor(
        self,
        prof_id: str,
        class_section_ids: List[str],
        requested_by: str
    ) -> List[ProfessorClassSectionResponseSchema]:
        """
            Register one professor to multiple class section at the same request
            Assign professor to multiple class sections
            - Professor must be ACTIVE
            - No duplicate assignment (handled by UniqueConstraint)
        """
        # Validate that all class sections exist
        for class_section_id in class_section_ids:
            class_section = await self.class_section_repo.get_by_id(class_section_id)
            if not class_section:
                raise ResourceNotFoundException(
                    f"Class section with id: {class_section_id} not found"
                )
            
            if class_section.status != ClassSectionStatus.OPEN:
                raise InvalidRequestException(
                    f"Invalid professor assignment due to class section status {class_section.status.lower()}."
                )
        
        # Create assignments in repository
        assignments = await self.prof_class_section_repo.assign_professor_class_section(
            prof_id=prof_id,
            class_section_ids=class_section_ids
        )
        
        if not assignments:
            raise UnprocessibleContentException(
                "Professor-class section assignment failed. Try again."
            )
        
        # Get the created assignment IDs
        assignment_ids = [str(assignment.id) for assignment in assignments]
        
        # Get detailed information for response
        detailed_assignments = await self.prof_class_section_repo.get_professor_class_section_details(
            assignment_ids
        )
        
        # Build response
        response: List[ProfessorClassSectionResponseSchema] = []
        
        for assignment in detailed_assignments:
            response.append(
                ProfessorClassSectionResponseSchema(
                    id=assignment.id,
                    created_at=assignment.created_at,
                    course_offering_id=assignment.course_offering_id,
                    
                    professor_id=assignment.professor_id,
                    professor_status=assignment.professor_status,
                    first_name=assignment.first_name,
                    middle_name=assignment.middle_name,
                    last_name=assignment.last_name,
                    suffix=assignment.suffix,
                    university_code=assignment.university_code,
                    
                    class_section_id=assignment.class_section_id,
                    section_code=assignment.section_code,
                    room_number=assignment.room_number,
                    student_capacity=assignment.student_capacity,
                    time_schedule=assignment.time_schedule,
                    class_section_status=assignment.class_section_status,
                    
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                        requested_by=requested_by,
                        description=f"Assigned professor {assignment.university_code} to class section {assignment.section_code}"
                    )
                )
            )
        
        return response
        
    
    # -------------------------------
    # CLASS SCHEDULING VALIDATION METHODS
    # -------------------------------
    async def validate_time_logic(self, start_time: time, end_time: time):
        #Validate time logic (start < end) (start < other_end) AND (end > other_start)
        if start_time >= end_time:
            raise InvalidRequestException("Start time must be before end time")
    
    async def validate_room_conflict(self, room_id: str, day_of_week: int, start_time: time, end_time: time):
        # Check if any existing schedule in this room overlaps with requested time
        existing_schedules: List[ClassSchedule] = await self.class_schedule_repo.get_schedules_by_room(room_id, day_of_week)
        for sched in existing_schedules:
            if (start_time < sched.end_time) and (end_time > sched.start_time):
                raise InvalidRequestException(f"Room {room_id} is already booked from {sched.start_time} to {sched.end_time}")
    
    async def validate_professor_conflict(self, class_section_id: str, day_of_week: int, start_time: time, end_time: time):
        # Get professor assigned to this class section
        professor_id = await self.prof_class_section_repo.get_professor_id(class_section_id)
        if not professor_id:
            raise ResourceNotFoundException("No professor assigned to class section")
        
        existing_schedules: List[ClassSchedule] = await self.class_schedule_repo.get_schedules_by_professor(professor_id, day_of_week)
        for sched in existing_schedules:
            if (start_time < sched.end_time) and (end_time > sched.start_time):
                raise InvalidRequestException(
                    f"Professor {professor_id} has a schedule conflict from {sched.start_time} to {sched.end_time}"
                )
    
    async def validate_class_section_status(self, class_section_id: str):
        class_section = await self.class_section_repo.get_by_id(class_section_id)
        if class_section.status != ClassSectionStatus.OPEN:
            raise InvalidRequestException(
                f"Invalid request. Class section {class_section.status} currently not open."
            )
            
    async def validate_course_offering_status(self, class_section_id: str):
        course_offering = await self.course_offering_repo.get_course_offering(class_section_id)
        if course_offering.status != CourseOfferingStatus.APPROVED:
            raise InvalidRequestException(
                f"Invalid request. Course offering {course_offering.status} currently not yet approved."
            )
        # validate term status
        await self.validate_term_status(course_offering.term_id)
            
    async def validate_term_status(self, term_id: str):
        term = await self.term_repo.get_by_id(term_id)
        if term.status != TermStatus.OPEN:
            raise InvalidRequestException(
                f"Invalid request. Term {term.status} currently not open."
            )
    
    async def assign_schedule_class_section(
        self,
        class_schedule: ClassScheduleRequestSchema,
        requested_by: str = None
    ) -> ClassScheduleResponseSchema:
        """
            Assign a schedule to class section.
            Following these validation and constraints:
                - Validate time logic (start < end)
                    (start < other_end) AND (end > other_start)
                - Validate room conflict
                - Validate professor conflict
                - ClassSection.status != CLOSED
                - CourseOffering.status == APPROVED
                - Term.status == OPEN
                - Persist schedule
        """
        # Validate time logic
        await self.validate_time_logic(class_schedule.start_time, class_schedule.end_time)
        
        # Validate room conflicts
        await self.validate_room_conflict(
            class_schedule.room_id,
            class_schedule.day_of_week,
            class_schedule.start_time,
            class_schedule.end_time
        )
        
        # Validate professor conflicts
        await self.validate_professor_conflict(
            class_schedule.class_section_id,
            class_schedule.day_of_week,
            class_schedule.start_time,
            class_schedule.end_time
        )
        
        # Validate class section status
        await self.validate_class_section_status(
            class_schedule.class_section_id
        )
        
        # Validate course offering and term status
        await self.validate_course_offering_status(
            class_schedule.class_section_id
        )
        
        # Persist schedule
        new_schedule = await self.class_schedule_repo.create(
            class_section_id=class_schedule.class_section_id,
            room_id=class_schedule.room_id,
            day_of_week=class_schedule.day_of_week,
            start_time=class_schedule.start_time,
            end_time=class_schedule.end_time
        )
        
        # Build response
        response = ClassScheduleResponseSchema(
            id=new_schedule.id,
            created_at=new_schedule.created_at,
            class_section_id=new_schedule.class_section_id,
            room_id=new_schedule.room_id,
            day_of_week=new_schedule.day_of_week,
            start_time=new_schedule.start_time,
            end_time=new_schedule.end_time,
            request_log=GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description="Schedule assigned successfully"
            )
        )
        
        return response
    