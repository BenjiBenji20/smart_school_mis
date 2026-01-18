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
from app.repository.users.professor_repository import ProfessorRepository

from app.models.academic_structures.term import Term
from app.models.academic_structures.course_offering import CourseOffering
from app.models.academic_structures.curriculum import Curriculum
from app.models.academic_structures.department import Department
from app.models.academic_structures.class_schedule import ClassSchedule
from app.models.locations.building import Building
from app.models.locations.room import Room
from app.models.academic_structures.program import Program
from app.models.academic_structures.curriculum_course import CurriculumCourse
from app.models.academic_structures.course import Course
from app.models.academic_structures.class_section import ClassSection
from app.models.users.professor import Professor


class AcademicStructureService:
    """
        Services list for academic structure route.
            - Register new building
            - List buildings
            - Register new rooms
            - List rooms by building
            - Register new department
            - List departments
            - Assign department building
            - Register new programs
            - List programs by department
            - Register new curriculum
            - List curriculums by program
            - Update curriculum status
            - Register new courses
            - List courses
            - Register new curriculum courses
            - Register new terms
            - Update term's status
            - Register course offering
            - List course offering by term
            - List curriculum course by field
            - Update course offerings's status
            - Register class section
            - List class sections by course offering
            - Assign class section professor
            - Assign a schedule to class section
            - List class schedule by section
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
        self.professor_repo = ProfessorRepository(db)
    
    # ==============================================
    # BUILDING SERVICE METHODS
    # ==============================================      
    async def register_building(
        self,
        building: BuildingRequestSchema,
        requested_by: str
    ) -> BuildingResponseSchema:
        """
             building
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
        
        return BuildingResponseSchema(
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
        
        
    async def list_buildings(self) -> List[BuildingResponseSchema]:
        """
            list of buildings (registrar role)
        """
        payload: List[dict] = []
        buildings: List[Building] = await self.building_repo.get_all()
        for building in buildings:
            payload.append(
                BuildingResponseSchema(
                    id=building.id,
                    created_at=building.created_at,
                    name=building.name,
                    room_capacity=building.room_capacity,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                    )
                )
            )
            
        return payload        
        
    
    # ==============================================
    # ROOM SERVICE METHODS
    # ==============================================  
    async def format_room_response(
        self, rooms: List[Room], requested_by: str = None
    ) -> List[RoomResponseSchema]:
        response: List[RoomResponseSchema] = []
        
        for room in rooms:
            building: Building = await self.building_repo.get_by_id(room.building_id)
            if building:
                response.append(
                    RoomResponseSchema(
                        id=str(room.id),
                        created_at=room.created_at,
                        room_code=room.room_code,
                        building_details=BuildingResponseSchema(
                            id=building.id,
                            created_at=building.created_at,
                            name=building.name,
                            room_capacity=building.room_capacity    
                        ),
                        request_log=GenericResponse(
                            success=True,
                            requested_at=datetime.now(timezone.utc),
                            requested_by=requested_by,
                            description=f"Register room {room.room_code}"
                        )
                    )
                )
            

        return response
    
        
    async def register_room(
        self,
        rooms: List[RoomRequestSchema],
        requested_by: str = None
    ) -> List[RoomResponseSchema]:
        """
            Register room (administrator role)
        """
        payload: list[dict] = []

        for room in rooms:
            data = room.model_dump()

            if data.get("room_code"):
                data["room_code"] = data["room_code"].upper()

            payload.append(data)
            
        # register rooms all at once
        registered_rooms: List[Room] = await self.room_repo.create_many(payload)
        
        if registered_rooms is None:
            raise UnprocessibleContentException(
                "Room registration failed. Try again."
            )
        
        return await self.format_room_response(requested_by=requested_by, rooms=registered_rooms)
        
        
    async def list_rooms_by_building(self, building_id: str) -> List[RoomResponseSchema]:
        rooms: List[Room] = await self.room_repo.list_rooms_by_building(building_id)
        
        if rooms is None:
            return []
        
        return await self.format_room_response(rooms=rooms)
        
    
    # ==============================================
    # DEPARTMENT SERVICE METHODS
    # ==============================================  
    async def register_department(
        self,
        department: DepartmentRequestSchema,
        requested_by: str
    ) -> DepartmentResponseSchema:
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
        
        return DepartmentResponseSchema(
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
        
        
    async def list_departments(self) -> List[DepartmentResponseSchema]:
        payload: List[dict] = []
        departments: List[Department] = await self.department_repo.get_all()
        for department in departments:
            payload.append(
                DepartmentResponseSchema(
                    id=department.id,
                    created_at=department.created_at,
                    title=department.title,
                    department_code=department.department_code,
                    description=department.description,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                    )
                )
            )
            
        return payload
    
        
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
        
      
    # ==============================================
    # PROGRAM SERVICE METHODS
    # ==============================================  
    async def format_program_response(
        self, programs: List[Program], requested_by: str = None, 
    ) -> List[ProgramResponseSchema]:
        response: List[ProgramResponseSchema] = []
        
        for program in programs:
            department: Department = await self.department_repo.get_by_id(program.department_id)
            if department:
                response.append(
                    ProgramResponseSchema(
                        id=str(program.id),
                        created_at=program.created_at,
                        title=program.title,
                        program_code=program.program_code,
                        description=program.description,
                        department_details=DepartmentResponseSchema(
                            id=department.id,
                            created_at=department.created_at,
                            title=department.title,
                            department_code=department.department_code,
                            description=department.description
                        ),
                        request_log=GenericResponse(
                            success=True,
                            requested_at=datetime.now(timezone.utc),
                            requested_by=requested_by,
                            description=f"Register program {program.title}"
                        )
                    )
                )

        return response
    
        
    async def register_program(
        self, 
        programs: List[ProgramRequestSchema], 
        requested_by: str
    ) -> List[ProgramResponseSchema]:
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
        
        return await self.format_program_response(programs=registered_programs, requested_by=requested_by)            
    
    
    async def list_programs_by_department(self, department_id: str) -> List[ProgramResponseSchema]:
        programs: List[Program] = await self.program_repo.list_programs_by_department(department_id)
        if programs is None:
            return []
        
        return await self.format_program_response(programs)
    
    
    # ==============================================
    # CURRICULUM SERVICE METHODS
    # ============================================== 
    async def format_curriculum_response(
        self, program_id: str, curriculum: Curriculum, requested_by: str = None
    ) -> CurriculumResponseSchema:
        program: Program = await self.program_repo.get_by_id(program_id)
        if program is None:
            raise InvalidRequestException(
                f"Curriculum registration failed. Program id {program_id} not found."
            )
            
        department: Department = await self.department_repo.get_by_id(program.department_id)
        if department is None:
            raise ResourceNotFoundException(f"Department from {program.title} not found.")
        
        return CurriculumResponseSchema(
            id=curriculum.id,
            created_at=curriculum.created_at,
            title=curriculum.title,
            effective_from=curriculum.effective_from,
            effective_to=curriculum.effective_to,
            status=curriculum.status,
            program_details=ProgramResponseSchema(
                id=program.id,
                created_at=program.created_at,
                title=program.title,
                program_code=program.program_code,
                description=program.description,
                department_details=DepartmentResponseSchema(
                    id=department.id,
                    created_at=department.created_at,
                    title=department.title,
                    department_code=department.department_code,
                    description=department.description,
                )
            ),
            request_log=GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Register curriculum {curriculum.title}"
            )
        )
    
    
    async def register_curriculum(
        self,
        curriculum: CurriculumRequestSchema,
        requested_by: str
    ) -> CurriculumResponseSchema:
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
        
        if curriculum is None:
            raise InvalidRequestException(f"Curriculum {curriculum_dict['curriculum_title']} registration failed.")
        
        return await self.format_curriculum_response(
            program_id=curriculum_dict["program_id"], curriculum=register_curriculum, requested_by=requested_by
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
    
    
    async def list_curriculums_by_program(self, program_id: str) -> List[CurriculumResponseSchema]:
        response: List[dict] = []
        curriculums: List[Curriculum] = await self.curriculum_repo.list_curriculums_by_program(program_id)
        for curriculum in curriculums:
            response.append(
                await self.format_curriculum_response(
                    program_id=curriculum.program_id, curriculum=curriculum
                )
            )
            
        return response
    
    
    # ==============================================
    # COURSE SERVICE METHODS
    # ============================================== 
    async def register_course(
        self, 
        courses: List[CourseRequestSchema], 
        requested_by: str
    ) -> List[CourseResponseSchema]:
        """
            Register courses 
        
            :param courses: list of courses (can be 1)
            :type courses: List[Course]
            :return: with appropriate data log
            :rtype: CourseResponseSchema
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
        
        response: List[CourseResponseSchema] = []
        
        for course in registered_courses:
            response.append(
                CourseResponseSchema(
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
    
    
    async def list_courses(self) -> List[CourseResponseSchema]:
        payload: List[dict] = []
        courses: List[Course] = await self.course_repo.get_all()
        for course in courses:
            payload.append(
                CourseResponseSchema(
                    id=course.id,
                    created_at=course.created_at,
                    title=course.title,
                    course_code=course.course_code,
                    units=course.units,
                    description=course.description,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc)
                    )
                )
            )
            
        return payload
    
    
    # ==============================================
    # CURRICULUM COURSE SERVICE METHODS
    # ============================================== 
    async def format_curriculum_course_response(
        self, 
        curriculum_course: CurriculumCourse, 
        requested_by: str = None
    ) -> CurriculumCourseResponseSchema:
        curriculum: Curriculum = await self.curriculum_repo.get_by_id(curriculum_course.curriculum_id)
        if curriculum is None:
            raise ResourceNotFoundException(
                f"Curriculum course registration failed. Curriculum {curriculum_course.curriculum_id} not found."
            )
            
        course: Course = await self.course_repo.get_by_id(curriculum_course.course_id)
        if course is None:
            raise ResourceNotFoundException(
                f"Curriculum course registration failed. Course {curriculum_course.course_id} not found."
            )
        
        return CurriculumCourseResponseSchema(
            id=str(curriculum_course.id),
            created_at=curriculum_course.created_at,
            year_level=curriculum_course.year_level,
            semester=curriculum_course.semester,
            is_required=curriculum_course.is_required,
            curriculum_details=await self.format_curriculum_response(curriculum.program_id, curriculum),
            course_details=CourseResponseSchema(
                id=course.id,
                created_at=course.created_at,
                title=course.title,
                course_code=course.course_code,
                units=course.units,
                description=course.description,
            ),
            request_log=GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Register curriculum course."
            )
        )
    
    
    async def register_curriculum_course(
        self, 
        curriculum_courses: List[CurriculumCourseRequestSchema], 
        requested_by: str
    ) -> List[CurriculumCourseResponseSchema]:
        """
            Register one or multiple curriculum courses (Registrar only) 
        
            :param courses: list of courses (can be 1)
            :type courses: List[Course]
            :return: with appropriate data log
            :rtype: CurriculumCourseResponseSchema
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
            
        response: List[CurriculumCourseResponseSchema] = []
        
        for curriculum_course in registered_curriculum_courses:
            response.append(
                await self.format_curriculum_course_response(
                    curriculum_course=curriculum_course, 
                    requested_by=requested_by
                )
            )
            
        return response        
    
    
    async def list_curriculum_course_by_field(
        self,
        curriculum_id: str = None,
        year_level: int = None,
        semester: int = None
    ) -> List[CurriculumCourseResponseSchema]:
        curriculum_courses: List[CurriculumCourse] = await self.curriculum_course_repo.list_curriculum_course_by_field(
            curriculum_id=curriculum_id,
            year_level=year_level,
            semester=semester
        )
        
        if curriculum_courses is None:
            return []
        
        response: List[CurriculumCourseResponseSchema] = []
        
        for curriculum_course in curriculum_courses:
            response.append(
                await self.format_curriculum_course_response(
                    curriculum_course=curriculum_course, 
                )
            )
            
        return response 
    
    
    # ==============================================
    # TERM SERVICE METHODS
    # ============================================== 
    async def register_term(
        self, 
        terms: List[TermRequestSchema], 
        requested_by: str
    ) -> List[TermResponseSchema]:
        """
            Register one or multiple terms (Registrar only) 
        
            :param courses: list of terms (can be 1)
            :return: with appropriate data log
            :rtype: TermResponseSchema
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
    
    
    # ==============================================
    # COURSE OFFERING SERVICE METHODS
    # ==============================================
    async def format_course_offering_response(
        self, 
        course_offering: CourseOffering, 
        term: Term,
        curriculum_course_response: CurriculumCourseResponseSchema,
        requested_by: str = None
    ) -> CourseOfferingResponseSchema:
        return CourseOfferingResponseSchema(
            id=course_offering.id,
            created_at=course_offering.created_at,
            curriculum_course_details=curriculum_course_response,
            term_details=TermResponseSchema(
                id=term.id,
                created_at=term.created_at,
                academic_year_start=term.academic_year_start,
                academic_year_end=term.academic_year_end,
                enrollment_start=term.enrollment_start,
                enrollment_end=term.enrollment_end,
                semester_period=term.semester_period,
                status=term.status
            ),
            status=course_offering.status,
            request_log=GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=f"Register course offering with status {course_offering.status.lower()}"
            )
        )
        
    
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
        
        curriculum_course: CurriculumCourse = await self.curriculum_course_repo.get_by_id(
            course_offering_dict['curriculum_course_id']
        )
        if curriculum_course is None:
            return InvalidRequestException(
                f"Course offering registration failed due to invalid curriculum course "
                f"id {course_offering_dict['curriculum_course_id']}."
            )
            
        term: Term = await self.term_repo.get_by_id(course_offering_dict['term_id'])
        if term is None:
            return InvalidRequestException(
                f"Course offering registration failed due to invalid curriculum course "
                f"id {course_offering_dict['term_id']}."
            )
        
        # register course offering
        register_course_offering = await self.course_offering_repo.register_course_offering(
            curriculum_course_id = course_offering_dict["curriculum_course_id"],
            term_id = course_offering_dict["term_id"],
            status = course_offering_dict["status"],
        )
        
        if not register_course_offering:
            raise InvalidRequestException("Registration of course offering failed.")
        
        curriculum_course_response: CurriculumCourseResponseSchema = await self.format_curriculum_course_response(
            curriculum_course=curriculum_course
        )
        
        return await self.format_course_offering_response(
            course_offering=register_course_offering,
            term=term,
            curriculum_course_response=curriculum_course_response,
            requested_by=requested_by
        )


    async def list_course_offering_by_term(self, term_id: str) -> List[CourseOfferingResponseSchema]:
        payload: List[dict] = []
        course_offerings: List[CourseOffering] = await self.course_offering_repo.list_course_offering_by_term(term_id)
        for course_offering in course_offerings:
            term: Term = await self.term_repo.get_by_id(course_offering.term_id)
            
            curriculum_course: CurriculumCourse = await self.curriculum_course_repo.get_by_id(
                course_offering.curriculum_course_id
            )
            
            if curriculum_course is None:
                raise InvalidRequestException("Request failed due to curriculum course issue.")
            
            curriculum_course_response: CurriculumCourseResponseSchema = await self.format_curriculum_course_response(
                curriculum_course=curriculum_course
            )
            
            payload.append(
                await self.format_course_offering_response(
                    course_offering=course_offering,
                    term=term,
                    curriculum_course_response=curriculum_course_response,
                )
            )
            
        return payload


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
        

    # ==============================================
    # CLASS SECTION SERVICE METHODS
    # ==============================================
    async def format_class_section_response(
        self, 
        class_section: ClassSection,
        course_offering: CourseOffering,
        description: str = None,
        error_description: str = None,
        requested_by: str = None
    ) -> ClassSectionResponseSchema:
        term: Term = await self.term_repo.get_by_id(course_offering.term_id)
        if term is None:
            raise InvalidRequestException(f"Class section {error_description} failed due to term issue.")
        
        curriculum_course: CurriculumCourse = await self.curriculum_course_repo.get_by_id(
            course_offering.curriculum_course_id
        )
        if curriculum_course is None:
            raise InvalidRequestException(f"Class section {error_description} failed due to curriculum course issue.")
        
        course: Course = await self.course_repo.get_by_id(curriculum_course.course_id)
        if course is None:
            raise InvalidRequestException(f"Class section {error_description} failed due to course issue.")
        
        curriculum: Curriculum = await self.curriculum_repo.get_by_id(curriculum_course.curriculum_id)
        if curriculum is None:
            raise InvalidRequestException(f"Class section {error_description} failed due to curriculum issue.")
        
        program: Program = await self.program_repo.get_by_id(curriculum.program_id)
        if program is None:
            raise InvalidRequestException(f"Class section {error_description} failed due to program issue.")
        
        department: Department = await self.department_repo.get_by_id(program.department_id)
        if department is None:
            raise InvalidRequestException(f"Class section {error_description} failed due to department issue.")
        
        return ClassSectionResponseSchema(
                id=str(class_section.id),
                created_at=class_section.created_at,
                section_code=class_section.section_code,
                student_capacity=class_section.student_capacity,
                current_student_cnt=class_section.current_student_cnt,
                status=class_section.status,
                course_offering_details=CourseOfferingResponseSchema(
                    id=course_offering.id,
                    created_at=course_offering.created_at,
                    term_details=TermResponseSchema(
                        id=term.id,
                        created_at=term.created_at,
                        academic_year_start=term.academic_year_start, 
                        academic_year_end=term.academic_year_end,
                        enrollment_start=term.enrollment_start,
                        enrollment_end=term.enrollment_end,
                        semester_period=term.semester_period,
                        status=term.status
                    ),
                    curriculum_course_details=CurriculumCourseResponseSchema(
                        id=curriculum_course.id,
                        created_at=curriculum_course.created_at,
                        is_required=curriculum_course.is_required,
                        curriculum_details=CurriculumResponseSchema(
                            id=curriculum.id,
                            created_at=curriculum.created_at,
                            title=curriculum.title,
                            effective_from=curriculum.effective_from,
                            effective_to=curriculum.effective_to,
                            status=curriculum.status,
                            program_details=ProgramResponseSchema(
                                id=program.id,
                                created_at=program.created_at,
                                title=program.title,
                                program_code=program.program_code,
                                description=program.description,
                                department_details=DepartmentResponseSchema(
                                    id=department.id,
                                    created_at=department.created_at,
                                    title=department.title,
                                    department_code=department.department_code,
                                    description=department.description
                                )
                            )
                        ),
                        course_details=CourseResponseSchema(
                            id=course.id,
                            created_at=course.created_at,
                            title=course.title,
                            course_code=course.course_code,
                            units=course.units,
                            description=course.description
                        )
                    ),
                    status=course_offering.status,
                ),
                request_log=GenericResponse(
                    success=True,
                    requested_at=datetime.now(timezone.utc),
                    requested_by=requested_by,
                    description=description
                )
            )
    
    
    async def register_class_section(
        self,
        class_sections: List[ClassSectionRequestSchema],
        requested_by: str
    ) -> List[ClassSectionResponseSchema]:
        """
            Register one or multiple class sections at the same time.
                - validate course_offering.status must be APPROVED
        """
        payload: list[dict] = []

        for class_section in class_sections:
            data = class_section.model_dump()
            
            # validate course_offering.status must be APPROVED
            course_offering: CourseOffering = await self.course_offering_repo.get_by_id(
                data['course_offering_id']
            )
            
            if course_offering.status != CourseOfferingStatus.APPROVED:
                raise InvalidRequestException(
                    f"Class section registration failed due to course offering status {course_offering.status.lower()}."
                )

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
                await self.format_class_section_response(
                    class_section=class_section,
                    course_offering=course_offering,
                    description=f"Register class section {class_section.section_code}",
                    error_description="registration",
                    requested_by=requested_by
                )
            )

        return response
        
    
    async def list_class_sections_by_course_offering(self, course_offering_id: str) -> List[ClassSectionResponseSchema]:
        course_offering: CourseOffering = await self.course_offering_repo.get_by_id(course_offering_id)
        if course_offering is None:
            raise ResourceNotFoundException(f"Course offering not found.")
        
        class_sections: List[ClassSection] = await self.class_section_repo.list_class_sections_by_course_offering(
            course_offering_id
        )
        
        if class_sections is None:
            return []
        
        response: List[dict] = []
        for class_section in class_sections:
            response.append(
                await self.format_class_section_response(
                    class_section=class_section,
                    course_offering=course_offering,
                )
            )
            
        return response
    

    # ==============================================
    # PROFESSOR CLASS SECTION SERVICE METHODS
    # ==============================================
    async def assign_class_section_professor(
        self,
        prof_id: str,
        class_section_ids: List[str],
        requested_by: str
    ) -> List[ProfessorClassSectionFormattedResponseSchema]:
        """
             one professor to multiple class section at the same request
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
        
        professor: Professor = await self.professor_repo.get_professor_by_id(prof_id)
        if professor is None:
            raise ResourceNotFoundException(f"Professor class section assignment failed due to professor not found.")
        
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
            course_offering: CourseOffering = await self.course_offering_repo.get_by_id(
                assignment.course_offering_id
            )
            
            term: Term = await self.term_repo.get_by_id(course_offering.term_id)
            
            curriculum_course: CurriculumCourse = await self.curriculum_course_repo.get_by_id(
                course_offering.curriculum_course_id
            )
            curriculum_course_response: CurriculumCourseResponseSchema = await self.format_curriculum_course_response(
                curriculum_course=curriculum_course
            )
            
            course_offering_response: CourseOfferingResponseSchema = await self.format_course_offering_response(
                course_offering=course_offering,
                term=term,
                curriculum_course_response=curriculum_course_response
            )
            
            class_section = await self.class_section_repo.get_by_id(
                assignment.class_section_id
            )
            
            class_section_response: ClassSectionResponseSchema = await self.format_class_section_response(
                    class_section=class_section,
                    course_offering=course_offering
                )
            
            response.append(
                ProfessorClassSectionFormattedResponseSchema(
                    id=assignment.id,
                    created_at=assignment.created_at,
                    professor_details=BaseUserResponseSchema(
                        id=professor.id,
                        created_at=professor.created_at,
                        first_name=professor.first_name,
                        middle_name=professor.middle_name,
                        last_name=professor.last_name,
                        suffix=professor.suffix,
                        age=professor.age,
                        gender=professor.gender,
                        complete_address=professor.complete_address,
                        email=professor.email,
                        cellphone_number=professor.cellphone_number,
                        role=professor.role,
                        is_active=professor.is_active,
                    ),
                    professor_status=assignment.professor_status,
                    university_code=assignment.university_code,
                    course_offering_details=course_offering_response,
                    class_section_details=class_section_response,
                    request_log=GenericResponse(
                        success=True,
                        requested_at=datetime.now(timezone.utc),
                        requested_by=requested_by,
                        description=f"Assigned professor {assignment.university_code} to class section {assignment.section_code}"
                    )
                )
            )
        
        return response
        
    
    # ==============================================
    # CLASS SCHEDULE SERVICE METHODS
    # ==============================================
    async def validate_time_logic(self, start_time: time, end_time: time):
        # Validate time logic (start < end) (start < other_end) AND (end > other_start)
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
            
    async def validate_term_status(self, term_id: str):
        term = await self.term_repo.get_by_id(term_id)
        if term.status != TermStatus.OPEN:
            raise InvalidRequestException(
                f"Invalid request. Term {term.status} currently not open."
            )
    
    
    async def format_class_schedule_response(
        self, class_schedule: ClassSchedule, class_section_response: ClassSectionResponseSchema,
        requested_by: str = None, description: str = None
    ) -> ClassScheduleResponseSchema:
        room: Room = await self.room_repo.get_by_id(class_schedule.room_id)
        if room is None:
            raise ResourceNotFoundException("Room not found.")
        
        building: Building = await self.building_repo.get_by_id(room.building_id)
        if building is None:
            raise ResourceNotFoundException("Building not found.")
        
        return ClassScheduleResponseSchema(
            id=class_schedule.id,
            created_at=class_schedule.created_at,
            day_of_week=class_schedule.day_of_week, 
            start_time=class_schedule.start_time,
            end_time=class_schedule.end_time,
            class_section_details=class_section_response,
            room_details=RoomResponseSchema(
                id=room.id,
                created_at=room.created_at,
                room_code=room.room_code,
                building_details=BuildingResponseSchema(
                    id=building.id,
                    created_at=building.created_at,
                    name=building.name,
                    room_capacity=building.room_capacity    
                )
            ),
            request_log=GenericResponse(
                success=True,
                requested_at=datetime.now(timezone.utc),
                requested_by=requested_by,
                description=description
            )
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
        
        # Validate class section
        class_section = await self.class_section_repo.get_by_id(class_schedule.class_section_id)
        if class_section.status != ClassSectionStatus.OPEN:
            raise InvalidRequestException(
                f"Invalid request. Class section {class_section.status} currently not open."
            )
        
        # Validate course offering and term
        course_offering = await self.course_offering_repo.get_course_offering(class_schedule.class_section_id)
        if course_offering.status != CourseOfferingStatus.APPROVED:
            raise InvalidRequestException(
                f"Invalid request. Course offering {course_offering.status} currently not yet approved."
            )
            
        # validate term status
        await self.validate_term_status(course_offering.term_id)
        
        # Persist schedule
        new_schedule = await self.class_schedule_repo.create(
            class_section_id=class_schedule.class_section_id,
            room_id=class_schedule.room_id,
            day_of_week=class_schedule.day_of_week,
            start_time=class_schedule.start_time,
            end_time=class_schedule.end_time
        )
        
        # format class section response
        class_section_response: ClassSectionResponseSchema = await self.format_class_section_response(
            class_section=class_section, course_offering=course_offering
        )
        
        # Build response
        return await self.format_class_schedule_response(
            class_schedule=new_schedule, class_section_response=class_section_response,
            requested_by=requested_by, description="Schedule assigned successfully"
        )
    
    
    async def list_class_schedule_by_section(self, class_section_id: str) -> List[ClassScheduleResponseSchema]:
        class_section: ClassSection = await self.class_section_repo.get_by_id(class_section_id)
        if class_section is None:
            raise ResourceNotFoundException(f"Class section not found with id {class_section_id}.")
        
        course_offering: CourseOffering = await self.course_offering_repo.get_by_id(
            class_section.course_offering_id
        )
        class_section_response: ClassSectionResponseSchema = await self.format_class_section_response(
            class_section=class_section, course_offering=course_offering
        )
        
        class_schedules: List[ClassSchedule] = await self.class_schedule_repo.list_class_schedule_by_section(
            class_section_id
        )

        if class_schedules is None:
            return []
        
        payload: List[dict] = []
        for class_schedule in class_schedules:
            payload.append(
                await self.format_class_schedule_response(
                    class_schedule=class_schedule, 
                    class_section_response=class_section_response
                )
            )
            
        return payload
    