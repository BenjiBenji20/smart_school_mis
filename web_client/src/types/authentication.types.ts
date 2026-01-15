/**
 * Date Written: 1/15/2026 at 9:29 AM
 */

import { UserGender, type UserRole, type UserStatus } from "./user_state.types";

// Base Response 
export interface BaseUserResponse {
    id: string;
    created_at: Date;

    first_name: string;
    middle_name: string;
    last_name: string;
    suffix: string | null;
    age: number;
    gender: UserGender;
    complete_address: string;

    email: string;
    cellphone_number: string;
    role: UserRole | null;
    is_active: boolean;
}

// Base Request 
export interface BaseUserRequest {
    email: string;
    cellphone_number: string;
    password: string;
    role?: UserRole | null;

    first_name: string;
    middle_name?: string | null;
    last_name: string;
    suffix?: string | null;
    age?: number;
    gender: UserGender;
    complete_address?: string;
}

// Credential Validator 
export interface CredentialValidator {
    email: string;
    password: string;
}

// Registration Passwords for 2 different users
export interface RegistrationFormData extends Omit<BaseUserRequest, 'role'> {
  confirmPassword: string;
}

export interface EmployeeRegistrationFormData extends BaseUserRequest {
  confirmPassword: string;
}

// Student Response 
export interface StudentResponse extends BaseUserResponse {
    university_code: string;
    status: UserStatus;
    last_school_attended: string | null;
    program_enrolled_date: Date | null;
    year_level: number;
}

// Validation Class
export class BaseUserRequestValidator {
    // Unicode letter pattern (basic approximation - full Unicode support requires different approach)
    private static readonly NAME_PATTERN = /^[\p{L}][\p{L}\p{M}'\- ]*$/u;
    private static readonly ADDRESS_PATTERN = /^[\p{L}\p{N}][\p{L}\p{N}\p{M}'\-\s.,#]*$/u;
    private static readonly EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    private static readonly PHONE_PATTERN = /^\d{11,13}$/;

    static validateEmail(email: string): void {
        const trimmed = email.trim();

        if (!this.EMAIL_PATTERN.test(trimmed)) {
            throw new Error("Must be a valid email address");
        }

        if (trimmed.length > 100) {
            throw new Error("Email must be less than 100 characters");
        }
    }

    static validateCellphoneNumber(cellphone_number: string): void {
        if (!this.PHONE_PATTERN.test(cellphone_number)) {
            throw new Error("Cellphone number must be between 11 and 13 digits");
        }
    }

    static validatePassword(password: string): void {
        if (password.length < 8 || password.length > 50) {
            throw new Error("Password must be between 8 and 50 characters");
        }
    }

    static validateFirstName(first_name: string): void {
        const trimmed = first_name.trim();

        if (trimmed.length > 50) {
            throw new Error("First name must be at most 50 characters");
        }

        if (!this.NAME_PATTERN.test(trimmed)) {
            throw new Error(`Must be valid name format: ${first_name}`);
        }
    }

    static validateMiddleName(middle_name: string | null | undefined): void {
        if (!middle_name) return;

        const trimmed = middle_name.trim();

        if (trimmed.length > 50) {
            throw new Error("Middle name must be at most 50 characters");
        }

        if (!this.NAME_PATTERN.test(trimmed)) {
            throw new Error(`Must be valid name format: ${middle_name}`);
        }
    }

    static validateLastName(last_name: string): void {
        const trimmed = last_name.trim();

        if (trimmed.length > 50) {
            throw new Error("Last name must be at most 50 characters");
        }

        if (!this.NAME_PATTERN.test(trimmed)) {
            throw new Error(`Must be valid name format: ${last_name}`);
        }
    }

    static validateSuffix(suffix: string | null | undefined): void {
        if (!suffix) return;

        if (suffix.length > 4) {
            throw new Error("Suffix must be at most 4 characters");
        }
    }

    static validateAge(age: number): void {
        if (age <= 0 || age > 120) {
            throw new Error("Age must be between 1 and 120");
        }
    }

    static validateGender(gender: UserGender): void {
        const validGenders = Object.values(UserGender);
        if (!validGenders.includes(gender)) {
            throw new Error("Gender must be Male or Female only");
        }
    }

    static validateCompleteAddress(complete_address: string): void {
        const trimmed = complete_address.trim();

        if (trimmed.length > 255) {
            throw new Error("Complete address must be at most 255 characters");
        }

        if (!this.ADDRESS_PATTERN.test(trimmed)) {
            throw new Error(`Must be valid address format: ${complete_address}`);
        }
    }

    static validate(user: BaseUserRequest): void {
        this.validateEmail(user.email);
        this.validateCellphoneNumber(user.cellphone_number);
        this.validatePassword(user.password);
        this.validateFirstName(user.first_name);
        this.validateMiddleName(user.middle_name);
        this.validateLastName(user.last_name);
        this.validateSuffix(user.suffix);
        this.validateAge(user.age ?? 18);
        this.validateGender(user.gender);
        this.validateCompleteAddress(user.complete_address ?? "Malabon City");
    }
}

// Credential Validator
export class AuthCredentialValidator {
    static validate(credentials: CredentialValidator): void {
        BaseUserRequestValidator.validateEmail(credentials.email);
        BaseUserRequestValidator.validatePassword(credentials.password);
    }
}