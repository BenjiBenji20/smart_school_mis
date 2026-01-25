/**
 * Date Written: 1/24/2026 11:28 AM
 */

import securedRequest from './authentication_api';
import type { ProgramChairResponse } from '@/types/authentication.types';

export const programChairApi = {
    async getCurrentProgramChair(): Promise<ProgramChairResponse> {
        const response = await securedRequest.get<ProgramChairResponse>(
            `/program_chair/get/current-program-chair`
        );
        return response.data;
    },

}
