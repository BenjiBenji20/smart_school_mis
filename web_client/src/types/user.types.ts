/**
 * Date Written: 1/15/2026 at 9:29 AM
 */

import type { BaseUserRequest } from "./authentication.types";

export interface StudentRequest extends BaseUserRequest {
    last_school_attended?: string;
    program_enrolled_date?: Date;
    year_level: number;
    program: string;
}

