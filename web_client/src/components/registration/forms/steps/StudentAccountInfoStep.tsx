/**
 * Date Written: 1/15/2026 at 1:39 PM
 */

import { Input } from '@/components/ui/input';
import { PasswordInput } from '../PasswordInput';
import { FormFieldWrapper } from '../FormFieldWrapper';

interface StudentAccountInfoStepProps {
    data: {
        email: string;
        cellphone_number: string;
        password: string;
        confirmPassword: string;
    };
    onChange: (field: keyof StudentAccountInfoStepProps['data'], value: string) => void;
    errors?: Record<string, string>;
}

export function StudentAccountInfoStep({
    data,
    onChange,
    errors = {},
}: StudentAccountInfoStepProps) {
    return (
        <div className="space-y-6">
            <FormFieldWrapper label="University Email" required error={errors.email}>
                <Input
                    type="email"
                    value={data.email}
                    onChange={(e) => onChange('email', e.target.value)}
                    placeholder="student@cityofmalabonuniversity.edu.ph"
                />
            </FormFieldWrapper>

            <FormFieldWrapper label="Cellphone Number" required error={errors.cellphone_number}>
                <Input
                    value={data.cellphone_number}
                    onChange={(e) => onChange('cellphone_number', e.target.value)}
                    placeholder="09123456789"
                />
            </FormFieldWrapper>

            <PasswordInput
                label="Password"
                value={data.password}
                onChange={(value) => onChange('password', value)}
                required
                error={errors.password}
            />

            <PasswordInput
                label="Confirm Password"
                value={data.confirmPassword}
                onChange={(value) => onChange('confirmPassword', value)}
                required
                error={errors.confirmPassword}
            />
        </div>
    );
}