/**
 * Date Written: 1/15/2026 at 9:29 AM
 */

export const UserRole = {
    ADMINISTRATOR: "Administrator",
    REGISTRAR: "Registrar",
    DEAN: "Dean",
    PROGRAM_CHAIR: "Program Chair",
    PROFESSOR: "Professor",
    STUDENT: "Student",
} as const;

export type UserRole = (typeof UserRole)[keyof typeof UserRole];


export type UserStatus =
    | "Approved"
    | "Rejected"
    | "Pending";

export const UserGender = {
    MALE: "Male",
    FEMALE: "Female",
} as const;

export type UserGender = typeof UserGender[keyof typeof UserGender];
