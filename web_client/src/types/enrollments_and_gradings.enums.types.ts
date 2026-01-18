/**
 * Date Written: 1/18/2026 at 11:17 AM
 * Enrollment Enums
 */

export const EnrollmentStatus = {
    PENDING: "PENDING",
    APPROVED: "APPROVED",
    REJECTED: "REJECTED",
} as const;
export type EnrollmentStatus = (typeof EnrollmentStatus)[keyof typeof EnrollmentStatus];