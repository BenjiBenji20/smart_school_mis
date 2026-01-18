/**
 * Date Written: 1/18/2026 at 2:30 PM
 */

import securedRequest  from './authentication_api';
import type {
    BuildingRequest,
    BuildingResponse,
    RoomRequest,
    RoomResponse,
    DepartmentRequest,
    DepartmentResponse,
    ProgramRequest,
    ProgramResponse,
    CurriculumRequest,
    CurriculumResponse,
    CourseRequest,
    CourseResponse,
    CurriculumCourseRequest,
    CurriculumCourseResponse,
    TermRequest,
    TermResponse,
    CourseOfferingRequest,
    CourseOfferingResponse,
    ClassSectionRequest,
    ClassSectionResponse,
    ProfessorClassSectionRequest,
    ProfessorClassSectionFormattedResponse,
    ClassScheduleRequest,
    ClassScheduleResponse,
    GenericResponse,
} from '@/types/academic_structure.types';
import {
    CurriculumStatus,
    TermStatus,
    CourseOfferingStatus,
} from '@/types/academic_structure.enums.types';

export const academicStructureApi = {
    // ==============================================
    // BUILDING APIs
    // ==============================================
    /**
     * Register a building (Administrator only)
     */
    async registerBuilding(building: BuildingRequest): Promise<BuildingResponse> {
        const response = await securedRequest.post<BuildingResponse>(
            `/academic-structure/register-building`,
            building
        );
        return response.data;
    },

    /**
     * List all buildings (Administrator only)
     */
    async listBuildings(): Promise<BuildingResponse[]> {
        const response = await securedRequest.get<BuildingResponse[]>(
            `/academic-structure/list-buildings`
        );
        return response.data;
    },

    // ==============================================
    // ROOM APIs
    // ==============================================
    /**
     * Register rooms (Administrator only)
     */
    async registerRoom(rooms: RoomRequest[]): Promise<RoomResponse[]> {
        const response = await securedRequest.post<RoomResponse[]>(
            `/academic-structure/register-room`,
            rooms
        );
        return response.data;
    },

    /**
     * List rooms by building (Administrator only)
     */
    async listRoomsByBuilding(buildingId: string): Promise<RoomResponse[]> {
        const response = await securedRequest.get<RoomResponse[]>(
            `/academic-structure/list-rooms/building/${buildingId}`
        );
        return response.data;
    },

    // ==============================================
    // DEPARTMENT APIs
    // ==============================================
    /**
     * Register a department (Registrar only)
     */
    async registerDepartment(department: DepartmentRequest): Promise<DepartmentResponse> {
        const response = await securedRequest.post<DepartmentResponse>(
            `/academic-structure/register-department`,
            department
        );
        return response.data;
    },

    /**
     * List all departments (Registrar only)
     */
    async listDepartments(): Promise<DepartmentResponse[]> {
        const response = await securedRequest.get<DepartmentResponse[]>(
            `/academic-structure/list-departments`
        );
        return response.data;
    },

    /**
     * Assign department to building (Administrator only)
     */
    async assignDepartmentBuilding(
        departmentId: string,
        buildingId: string
    ): Promise<GenericResponse> {
        const response = await securedRequest.patch<GenericResponse>(
            `/academic-structure/department/${departmentId}/building/${buildingId}`
        );
        return response.data;
    },

    // ==============================================
    // PROGRAM APIs
    // ==============================================
    /**
     * Register programs (Registrar only)
     */
    async registerProgram(programs: ProgramRequest[]): Promise<ProgramResponse[]> {
        const response = await securedRequest.post<ProgramResponse[]>(
            `/academic-structure/register-program`,
            programs
        );
        return response.data;
    },

    /**
     * List programs by department (Registrar, Dean)
     */
    async listProgramsByDepartment(departmentId: string): Promise<ProgramResponse[]> {
        const response = await securedRequest.get<ProgramResponse[]>(
            `/academic-structure/list-programs/department/${departmentId}`
        );
        return response.data;
    },

    // ==============================================
    // CURRICULUM APIs
    // ==============================================
    /**
     * Register a curriculum (Registrar only)
     */
    async registerCurriculum(curriculum: CurriculumRequest): Promise<CurriculumResponse> {
        const response = await securedRequest.post<CurriculumResponse>(
            `/academic-structure/register-curriculum`,
            curriculum
        );
        return response.data;
    },

    /**
     * List curriculums by program (Registrar, Dean)
     */
    async listCurriculumsByProgram(programId: string): Promise<CurriculumResponse[]> {
        const response = await securedRequest.get<CurriculumResponse[]>(
            `/academic-structure/list-curriculums/program/${programId}`
        );
        return response.data;
    },

    /**
     * Update curriculum status (Registrar only)
     */
    async updateCurriculumStatus(
        id: string,
        status: CurriculumStatus
    ): Promise<GenericResponse> {
        const response = await securedRequest.patch<GenericResponse>(
            `/academic-structure/curriculum/${id}/status/${status}`
        );
        return response.data;
    },

    // ==============================================
    // COURSE APIs
    // ==============================================
    /**
     * Register courses (Registrar only)
     */
    async registerCourse(courses: CourseRequest[]): Promise<CourseResponse[]> {
        const response = await securedRequest.post<CourseResponse[]>(
            `/academic-structure/register-course`,
            courses
        );
        return response.data;
    },

    /**
     * List all courses (Registrar, Dean)
     */
    async listCourses(): Promise<CourseResponse[]> {
        const response = await securedRequest.get<CourseResponse[]>(
            `/academic-structure/list-courses`
        );
        return response.data;
    },

    // ==============================================
    // CURRICULUM COURSE APIs
    // ==============================================
    /**
     * Register curriculum courses (Registrar only)
     */
    async registerCurriculumCourse(
        curriculumCourses: CurriculumCourseRequest[]
    ): Promise<CurriculumCourseResponse[]> {
        const response = await securedRequest.post<CurriculumCourseResponse[]>(
            `/academic-structure/register-curriculum-course`,
            curriculumCourses
        );
        return response.data;
    },

    /**
     * List curriculum courses by fields (Registrar only)
     */
    async listCurriculumCourseByField(
        curriculumId: string,
        yearLevel: number,
        semester: number
    ): Promise<CurriculumCourseResponse[]> {
        const response = await securedRequest.get<CurriculumCourseResponse[]>(
            `/academic-structure/list-curriculum-courses/curriculum/${curriculumId}/year_level/${yearLevel}/semester/${semester}`
        );
        return response.data;
    },

    // ==============================================
    // TERM APIs
    // ==============================================
    /**
     * Register terms (Registrar only)
     */
    async registerTerm(terms: TermRequest[]): Promise<TermResponse[]> {
        const response = await securedRequest.post<TermResponse[]>(
            `/academic-structure/register-term`,
            terms
        );
        return response.data;
    },

    /**
     * Update term status (Registrar only)
     */
    async updateTermStatus(id: string, status: TermStatus): Promise<GenericResponse> {
        const response = await securedRequest.patch<GenericResponse>(
            `/academic-structure/term/${id}/status/${status}`
        );
        return response.data;
    },

    /**
     * Get active year terms (Registrar only)
     */
    async getActiveYearTerm(): Promise<TermResponse[]> {
        const response = await securedRequest.get<TermResponse[]>(
            `/academic-structure/term/active-year`
        );
        return response.data;
    },

    /**
     * Get active enrollment terms (Registrar only)
     */
    async getActiveEnrollment(): Promise<TermResponse[]> {
        const response = await securedRequest.get<TermResponse[]>(
            `/academic-structure/term/active-enrollment`
        );
        return response.data;
    },

    // ==============================================
    // COURSE OFFERING APIs
    // ==============================================
    /**
     * Register course offering (Registrar only)
     */
    async registerCourseOffering(
        courseOffering: CourseOfferingRequest
    ): Promise<CourseOfferingResponse> {
        const response = await securedRequest.post<CourseOfferingResponse>(
            `/academic-structure/register-course-offering`,
            courseOffering
        );
        return response.data;
    },

    /**
     * List course offerings by term (Registrar, Dean)
     */
    async listCourseOfferingByTerm(termId: string): Promise<CourseOfferingResponse[]> {
        const response = await securedRequest.get<CourseOfferingResponse[]>(
            `/academic-structure/list-course-offerings/term/${termId}`
        );
        return response.data;
    },

    /**
     * Update course offering status (Registrar, Dean)
     */
    async updateCourseOfferingStatus(
        id: string,
        status: CourseOfferingStatus
    ): Promise<GenericResponse> {
        const response = await securedRequest.patch<GenericResponse>(
            `/academic-structure/course-offering/${id}/status/${status}`
        );
        return response.data;
    },

    // ==============================================
    // CLASS SECTION APIs
    // ==============================================
    /**
     * Register class sections (Registrar, Dean, Program Chair)
     */
    async registerClassSection(
        classSections: ClassSectionRequest[]
    ): Promise<ClassSectionResponse[]> {
        const response = await securedRequest.post<ClassSectionResponse[]>(
            `/academic-structure/register/class-section`,
            classSections
        );
        return response.data;
    },

    /**
     * Assign professor to class sections (Registrar, Dean, Program Chair)
     */
    async assignClassSectionProfessor(
        request: ProfessorClassSectionRequest
    ): Promise<ProfessorClassSectionFormattedResponse[]> {
        const response = await securedRequest.post<ProfessorClassSectionFormattedResponse[]>(
            `/academic-structure/assign/professor/class-section`,
            request
        );
        return response.data;
    },

    // ==============================================
    // CLASS SCHEDULE APIs
    // ==============================================
    /**
     * Assign schedule to class section (Registrar, Dean, Program Chair)
     */
    async assignScheduleClassSection(
        classSchedule: ClassScheduleRequest
    ): Promise<ClassScheduleResponse> {
        const response = await securedRequest.post<ClassScheduleResponse>(
            `/academic-structure/assign/schedule/class-section`,
            classSchedule
        );
        return response.data;
    },

    /**
     * List class schedules by section (Registrar, Dean)
     */
    async listClassScheduleBySection(
        classSectionId: string
    ): Promise<ClassScheduleResponse[]> {
        const response = await securedRequest.get<ClassScheduleResponse[]>(
            `/academic-structure/list-class-schedules/class-section/${classSectionId}`
        );
        return response.data;
    },
};