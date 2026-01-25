/**
 * Date Written: 1/24/2026 11:26 AM
 */

import securedRequest from './authentication_api';
import type { DeanResponse } from '@/types/authentication.types';

export const deanApi = {
    async getCurrentDean(): Promise<DeanResponse> {
        const response = await securedRequest.get<DeanResponse>(
            `/dean/get/current-dean`
        );
        return response.data;
    },

}

