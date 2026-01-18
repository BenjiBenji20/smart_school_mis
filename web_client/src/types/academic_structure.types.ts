/**
 * Date Written: 1/18/2026 at 10:51 AM
 */

import type { 
    ClassSectionStatus, 
    CourseOfferingStatus, 
    CurriculumStatus, 
    ProfessorStatus, 
    SemesterPeriod, 
    TermStatus 
} from "./academic_structure.enums.types"
import { type BaseUserResponse } from './authentication.types';

// ==============================================
// GENERIC RESPONSE
// ==============================================
export interface GenericResponse {
    message: string;
    status_code?: number;
}

// ==============================================
// BUILDING INTERFACES
// ==============================================
export interface BuildingRequest {
    name: string;
    room_capacity: number;
}

export interface BuildingResponse {
    id: string;
    created_at: string;
    name: string;
    room_capacity: number;
    request_log?: GenericResponse | null;
}

// ==============================================
// ROOM INTERFACES
// ==============================================
export interface RoomRequest {
    room_code?: string | null;
    building_id: string;
}

export interface RoomResponse {
    id: string;
    created_at: string;
    room_code?: string | null;
    building_details: BuildingResponse;
    request_log?: GenericResponse | null;
}

// ==============================================
// DEPARTMENT INTERFACES
// ==============================================
export interface DepartmentRequest {
    title: string;
    department_code?: string | null;
    description?: string | null;
}

export interface DepartmentResponse {
    id: string;
    created_at: string;
    title: string;
    department_code?: string | null;
    description?: string | null;
    request_log?: GenericResponse | null;
}

// ==============================================
// PROGRAM INTERFACES
// ==============================================
export interface ProgramRequest {
    title: string;
    program_code?: string | null;
    description?: string | null;
    department_id?: string | null;
}

export interface ProgramResponse {
    id: string;
    created_at: string;
    title: string;
    program_code?: string | null;
    description?: string | null;
    department_details?: DepartmentResponse | null;
    request_log?: GenericResponse | null;
}

// ==============================================
// CURRICULUM INTERFACES
// ==============================================
export interface CurriculumRequest {
    title: string;
    effective_from: number;
    effective_to?: number | null;
    status: CurriculumStatus;
    program_id: string;
}

export interface CurriculumResponse {
    id: string;
    created_at: string;
    title: string;
    effective_from: number;
    effective_to?: number | null;
    status: CurriculumStatus;
    program_details?: ProgramResponse | null;
    request_log?: GenericResponse | null;
}

// ==============================================
// COURSE INTERFACES
// ==============================================
export interface CourseRequest {
    title: string;
    course_code?: string | null;
    units: number;
    description?: string | null;
}

export interface CourseResponse {
    id: string;
    created_at: string;
    title: string;
    course_code?: string | null;
    units: number;
    description?: string | null;
    request_log?: GenericResponse | null;
}

// ==============================================
// CURRICULUM COURSE INTERFACES
// ==============================================
export interface CurriculumCourseRequest {
    year_level: number;
    semester: number;
    is_required: boolean;
    curriculum_id: string;
    course_id: string;
}

export interface CurriculumCourseResponse {
    id: string;
    created_at: string;
    is_required: boolean;
    curriculum_details: CurriculumResponse;
    course_details: CourseResponse;
    request_log?: GenericResponse | null;
}

// ==============================================
// TERM INTERFACES
// ==============================================
export interface TermRequest {
    academic_year_start: number;
    academic_year_end: number;
    enrollment_start: string;
    enrollment_end: string;
    semester_period: SemesterPeriod;
    status?: TermStatus;
}

export interface TermResponse {
    id: string;
    created_at: string;
    academic_year_start: number;
    academic_year_end: number;
    enrollment_start: string;
    enrollment_end: string;
    semester_period: SemesterPeriod;
    status: TermStatus;
    request_log?: GenericResponse | null;
}

// ==============================================
// COURSE OFFERING INTERFACES
// ==============================================
export interface CourseOfferingRequest {
    term_id: string;
    curriculum_course_id: string;
    status?: CourseOfferingStatus;
}

export interface CourseOfferingResponse {
    id: string;
    created_at: string;
    term_details: TermResponse;
    curriculum_course_details: CurriculumCourseResponse;
    status: CourseOfferingStatus;
    request_log?: GenericResponse | null;
}

// ==============================================
// CLASS SECTION INTERFACES
// ==============================================
export interface ClassSectionRequest {
    course_offering_id: string;
    section_code: string;
    student_capacity: number;
    status?: ClassSectionStatus;
}

export interface ClassSectionResponse {
    id: string;
    created_at: string;
    section_code: string;
    student_capacity: number;
    current_student_cnt: number;
    status: ClassSectionStatus;
    course_offering_details: CourseOfferingResponse;
    request_log?: GenericResponse | null;
}

// ==============================================
// PROFESSOR CLASS SECTION INTERFACES
// ==============================================
export interface ProfessorClassSectionRequest {
    prof_id: string;
    class_section_ids: string[];
}

export interface ProfessorClassSectionResponse {
    id: string;
    created_at: string;
    course_offering_id: string;
    professor_id: string;
    professor_status: ProfessorStatus;
    first_name: string;
    middle_name?: string | null;
    last_name: string;
    suffix?: string | null;
    university_code: string;
    class_section_id: string;
    section_code: string;
    room_number?: number | null;
    student_capacity: number;
    time_schedule?: string | null;
    class_section_status: ClassSectionStatus;
    request_log?: GenericResponse | null;
}

export interface ProfessorClassSectionFormattedResponse {
    id: string;
    created_at: string;
    professor_details: BaseUserResponse;
    professor_status: ProfessorStatus;
    university_code: string;
    course_offering_details: CourseOfferingResponse;
    class_section_details: ClassSectionResponse;
    request_log?: GenericResponse | null;
}

// ==============================================
// CLASS SCHEDULE INTERFACES
// ==============================================
export interface ClassScheduleRequest {
    class_section_id: string;
    room_id: string;
    day_of_week: number; // 1=Mon, 7=Sun
    start_time: string; // time as string "HH:MM:SS"
    end_time: string; // time as string "HH:MM:SS"
}

export interface ClassScheduleResponse {
    id: string;
    created_at: string;
    day_of_week: number;
    start_time: string;
    end_time: string;
    class_section_details: ClassSectionResponse;
    room_details: RoomResponse;
    request_log?: GenericResponse | null;
}
