/**
 * Date Written: 1/18/2026 at 11:15 AM
 */

import { EnrollmentStatus } from './enrollments_and_gradings.enums.types';
import type { ClassSectionResponse, TermResponse, GenericResponse } from './academic_structure.types';
import type { StudentResponse } from './authentication.types';

// ==============================================
// ENROLLMENT INTERFACES
// ==============================================
export interface UpdateEnrollmentStatus {
    status: EnrollmentStatus;
    enrollment_ids: string[];
}

export interface EnrollmentResponse {
    status: EnrollmentStatus;
    student: StudentResponse;
    class_section: ClassSectionResponse;
    term: TermResponse;
    request_log?: GenericResponse | null;
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
