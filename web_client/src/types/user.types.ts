import type { BaseUserRequest } from "./authentication.types";

export interface StudentRequest extends BaseUserRequest {
    last_school_attended?: string;
    program_enrolled_date?: Date;
    year_level: number;
    program: string;
}

