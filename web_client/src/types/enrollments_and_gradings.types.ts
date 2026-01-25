/**
 * Date Written: 1/18/2026 at 11:15 AM
 */

import { EnrollmentStatus } from './enrollments_and_gradings.enums.types';
import type { GenericResponse } from './academic_structure.types';
import type { SemesterPeriod } from './academic_structure.enums.types';

// ==============================================
// ENROLLMENT INTERFACES
// ==============================================
export interface UpdateEnrollmentStatus {
    status: EnrollmentStatus;
    enrollment_ids: string[];
}

export interface EnrollmentResponse {
    enrollment_id: string;
    student_id: string;
    class_section_id: string;
    term_id: string;
    program_id: string;
    enrollment_status: EnrollmentStatus;
    section_code: string;
    course_code: string;
    title: string;
    units: number;
    day_of_week: number | null;
    start_time: string | null; // time as string from backend "HH:MM:SS"
    end_time: string | null; // time as string from backend "HH:MM:SS"
    room_code: string | null;
    semester_period: SemesterPeriod;
    academic_year_start: number;
    academic_year_end: number;
    program_code: string | null;
    student_name: string | null;
    assigned_professor: string | null;
    request_log: GenericResponse | null;
}


export interface AllowedEnrollSectionResponse {
    class_section_id: string;
    course_code: string;
    title: string;
    units: number;
    section_code: string;
    day_of_week: number | null;
    start_time: string | null;
    end_time: string | null;
    room_code: string | null;
    assigned_professor: string | null;
}
