/**
 * Date Written: 1/15/2026 at 1:40 PM
 */
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { PasswordInput } from '@/components/registration/forms/PasswordInput';
import { FormFieldWrapper } from '@/components/registration/forms/FormFieldWrapper';
import { UserRole } from '@/types/user_state.enums.types';

const EMPLOYEE_ROLES = [
    UserRole.ADMINISTRATOR,
    UserRole.REGISTRAR,
    UserRole.DEAN,
    UserRole.PROGRAM_CHAIR,
    UserRole.PROFESSOR,
] as const;

interface EmployeeAccountInfoStepProps {
    data: {
        email: string;
        cellphone_number: string;
        password: string;
        confirmPassword: string;
        role?: UserRole;
    };
    onChange: (field: keyof EmployeeAccountInfoStepProps['data'], value: string | UserRole) => void;
    errors?: Record<string, string>;
}

export function EmployeeAccountInfoStep({
    data,
    onChange,
    errors = {},
}: EmployeeAccountInfoStepProps) {
    return (
        <div className="space-y-6">
            <FormFieldWrapper label="University Email" required error={errors.email}>
                <Input
                    type="email"
                    value={data.email}
                    onChange={(e) => onChange('email', e.target.value)}
                    placeholder="employee@cityofmalabonuniversity.edu.ph"
                />
            </FormFieldWrapper>

            <FormFieldWrapper label="Cellphone Number" required error={errors.cellphone_number}>
                <Input
                    value={data.cellphone_number}
                    onChange={(e) => onChange('cellphone_number', e.target.value)}
                    placeholder="09123456789"
                />
            </FormFieldWrapper>

            <FormFieldWrapper label="Role" required error={errors.role}>
                <Select
                    value={data.role || ''}
                    onValueChange={(value) => onChange('role', value as UserRole)}
                >
                    <SelectTrigger>
                        <SelectValue placeholder="Select your role" />
                    </SelectTrigger>
                    <SelectContent>
                        {EMPLOYEE_ROLES.map((role) => (
                            <SelectItem key={role} value={role}>
                                {role}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </FormFieldWrapper>

            <PasswordInput
                label="Password"
                value={data.password}
                onChange={(value: string) => onChange('password', value)}
                required
                error={errors.password}
            />

            <PasswordInput
                label="Confirm Password"
                value={data.confirmPassword}
                onChange={(value: string) => onChange('confirmPassword', value)}
                required
                error={errors.confirmPassword}
            />
        </div>
    );
}