/**
 * Date Written: 1/15/2026 at 1:37 PM
 */

import { z } from 'zod';
import { UserGender } from '@/types/user_state.enums.types';

export const personalInfoSchema = z.object({
    first_name: z.string().min(1, "First name is required"),
    middle_name: z.string().optional().nullable(),
    last_name: z.string().min(1, "Last name is required"),
    suffix: z.string().optional().nullable(),
    age: z.number().min(16, "Must be at least 16 years old").optional(),
    gender: z.enum([UserGender.MALE, UserGender.FEMALE]),
    complete_address: z.string().min(5, "Address must be at least 5 characters").optional(),
});

export const accountInfoSchema = z.object({
    email: z.string().email("Invalid email address"),
    cellphone_number: z.string()
        .min(10, "Phone number must be at least 10 digits")
        .regex(/^[0-9+\-\s]+$/, "Invalid phone number format"),
    password: z.string()
        .min(8, "Password must be at least 8 characters")
        .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
        .regex(/[a-z]/, "Password must contain at least one lowercase letter")
        .regex(/[0-9]/, "Password must contain at least one number"),
    confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
});

export const employeeSchema = z.object({
    role: z.enum(["Administrator", "Registrar", "Dean", "Program Chair", "Professor"]),
});

export const studentRegistrationSchema = personalInfoSchema.and(
    accountInfoSchema.omit({ confirmPassword: true })
);

export const employeeRegistrationSchema = personalInfoSchema.and(
    accountInfoSchema.omit({ confirmPassword: true })
).and(employeeSchema);