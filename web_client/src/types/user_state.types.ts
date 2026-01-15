export type UserRole =
    | "Administrator"
    | "Registrar"
    | "Dean"
    | "Program Chair"
    | "Professor"
    | "Student";

export type UserStatus =
    | "Approved"
    | "Rejected"
    | "Pending";

export const UserGender = {
    MALE: "Male",
    FEMALE: "Female",
} as const;

export type UserGender = typeof UserGender[keyof typeof UserGender];

