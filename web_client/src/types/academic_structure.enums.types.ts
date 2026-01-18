/**
 * Date Written: 1/18/2026 at 10:50 AM
 */

// ==============================================
// CURRICULUM ENUMS
// ==============================================
export const CurriculumStatus = {
    DRAFT: "Draft",
    ACTIVE: "Active",
    RETIRED: "Retired",
} as const;
export type CurriculumStatus = (typeof CurriculumStatus)[keyof typeof CurriculumStatus];

// ==============================================
// SEMESTER ENUMS
// ==============================================
export const SemesterPeriod = {
    FIRST: "FIRST",
    SECOND: "SECOND",
    SUMMER: "SUMMER",
} as const;
export type SemesterPeriod = (typeof SemesterPeriod)[keyof typeof SemesterPeriod];

// ==============================================
// TERM ENUMS
// ==============================================
export const TermStatus = {
    DRAFT: "DRAFT",
    OPEN: "OPEN",
    CLOSED: "CLOSED",
    ARCHIVED: "ARCHIVED",
} as const;
export type TermStatus = (typeof TermStatus)[keyof typeof TermStatus];

// ==============================================
// COURSE OFFERING ENUMS
// ==============================================
export const CourseOfferingStatus = {
    PENDING: "PENDING",
    APPROVED: "APPROVED",
    CANCELLED: "CANCELLED",
} as const;
export type CourseOfferingStatus = (typeof CourseOfferingStatus)[keyof typeof CourseOfferingStatus];

// ==============================================
// CLASS SECTION ENUMS
// ==============================================
export const ClassSectionStatus = {
    OPEN: "OPEN",
    CLOSE: "CLOSE",
    CANCELLED: "CANCELLED",
} as const;
export type ClassSectionStatus = (typeof ClassSectionStatus)[keyof typeof ClassSectionStatus];

// ==============================================
// PROFESSOR STATUS ENUMS
// ==============================================
export const ProfessorStatus = {
    ACTIVE: "ACTIVE",
    NOT_ACTIVE: "NOT_ACTIVE",
    SUSPENDED: "SUSPENDED",
    ON_LEAVE: "ON_LEAVE",
} as const;
export type ProfessorStatus = (typeof ProfessorStatus)[keyof typeof ProfessorStatus];

// ==============================================
// DEAN STATUS ENUMS
// ==============================================
export const DeanStatus = {
    ACTIVE: "ACTIVE",
    NOT_ACTIVE: "NOT_ACTIVE",
    SUSPENDED: "SUSPENDED",
    ON_LEAVE: "ON_LEAVE",
} as const;
export type DeanStatus = (typeof DeanStatus)[keyof typeof DeanStatus];

// ==============================================
// PROGRAM CHAIR STATUS ENUMS
// ==============================================
export const ProgramChairStatus = {
    ACTIVE: "ACTIVE",
    NOT_ACTIVE: "NOT_ACTIVE",
    SUSPENDED: "SUSPENDED",
    ON_LEAVE: "ON_LEAVE",
} as const;
export type ProgramChairStatus = (typeof ProgramChairStatus)[keyof typeof ProgramChairStatus];