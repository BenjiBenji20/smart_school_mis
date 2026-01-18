/**
 * Date Written: 1/18/2026 11:25 AM
 */

import securedRequest from './authentication_api';
import { type ClassSectionResponse } from '@/types/academic_structure.types';
import { EnrollmentStatus } from '@/types/enrollments_and_gradings.enums.types';
import type { 
    EnrollmentResponse, 
    UpdateEnrollmentStatus 
} from '@/types/enrollments_and_gradings.types'

// REST API calls
export const enrollmentApi = {
    /**
     * Get allowed sections for student to enroll
     */
    async getAllowedSections(): Promise<ClassSectionResponse[]> {
        const response = await securedRequest.get<ClassSectionResponse[]>(
            `/enrollment/allowed-sections`
        );
        return response.data;
    },

    /**
     * Enroll student in a class section
     */
    async enrollStudentClassSection(
        studentId: string,
        classSectionId: string
    ): Promise<EnrollmentResponse> {
        const response = await securedRequest.post<EnrollmentResponse>(
            `/enrollment/student/${studentId}/class_section/${classSectionId}`
        );
        return response.data;
    },

    /**
     * Get all enrollments (Registrar only)
     */
    async getAllEnrollments(): Promise<EnrollmentResponse[]> {
        const response = await securedRequest.get<EnrollmentResponse[]>(
            `/enrollment/get-enrollments`
        );
        return response.data;
    },

    /**
     * Get filtered enrollments (Registrar only)
     */
    async getFilteredEnrollments(params: {
        department_id?: string;
        program_id?: string;
        class_section_id?: string;
        term_id?: string;
    }): Promise<EnrollmentResponse[]> {
        const queryParams = new URLSearchParams();

        if (params.department_id) queryParams.append('department_id', params.department_id);
        if (params.program_id) queryParams.append('program_id', params.program_id);
        if (params.class_section_id) queryParams.append('class_section_id', params.class_section_id);
        if (params.term_id) queryParams.append('term_id', params.term_id);

        const response = await securedRequest.get<EnrollmentResponse[]>(
            `/enrollment/filter?${queryParams.toString()}`
        );
        return response.data;
    },

    /**
     * Update enrollment status (Registrar only)
     */
    async updateEnrollmentStatus(
        data: UpdateEnrollmentStatus
    ): Promise<EnrollmentResponse[]> {
        const response = await securedRequest.patch<EnrollmentResponse[]>(
            `/enrollment/status`,
            data
        );
        return response.data;
    },

    /**
     * List enrollments by status (Registrar only)
     */
    async listEnrollmentsByStatus(
        enrollmentStatus: EnrollmentStatus
    ): Promise<EnrollmentResponse[]> {
        const response = await securedRequest.get<EnrollmentResponse[]>(
            `/enrollment/list/status/${enrollmentStatus}`
        );
        return response.data;
    },
};