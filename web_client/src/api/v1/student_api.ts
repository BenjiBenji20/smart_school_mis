/**
 * Date Written: 1/19/2026 6:20 PM
 */

import type { TermResponse } from '@/types/academic_structure.types';
import securedRequest from './authentication_api';
import type {
    AllowedEnrollSectionResponse,
} from '@/types/enrollments_and_gradings.types'
import type { StudentResponse } from '@/types/authentication.types';

export const studentApi = {
    async getCurrentStudent(): Promise <StudentResponse> {
        const response = await securedRequest.get<StudentResponse>(
            `/student/get/current-student`
        );
        return response.data;
    },

    async getMyEnrollment(): Promise <AllowedEnrollSectionResponse[]> {
        const response = await securedRequest.get<AllowedEnrollSectionResponse[]>(
            `/student/get/enrollments`
        );
        return response.data;
    },

    /**
     * 
     *  Get the current enrolled term of student
     */
    async getMyCurrentTerm(): Promise <TermResponse> {
        const response = await securedRequest.get<TermResponse>(
            `/student/get/current-term`
        );
        return response.data;
    },

    /**
     * 
     *  Get the next term of student that needed to be enrolled
     */
    async getMyNextTerm(): Promise <TermResponse> {
        const response = await securedRequest.get<TermResponse>(
            `/student/get/next-term`
        );
        return response.data;
    }
}

