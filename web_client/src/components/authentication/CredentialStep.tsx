/**
 * Date Written: 1/16/2026 at 4:00 PM
 */
import { Input } from '@/components/ui/input';
import { PasswordInput } from '../registration/forms/PasswordInput';
import { FormFieldWrapper } from '../registration/forms/FormFieldWrapper';
import { type CredentialValidator } from '@/types/authentication.types';

interface CredentialStepProps {
    data: CredentialValidator;
    onChange: (field: keyof CredentialValidator, value: string) => void;
    errors?: Record<string, string>;
}

export function CredentialStep({
    data,
    onChange,
    errors = {},
}: CredentialStepProps) {
    return (
        <div className="w-full space-y-6">
            <FormFieldWrapper label="Email Address" required error={errors.email}>
                <Input
                    type="email"
                    value={data.email}
                    onChange={(e) => onChange('email', e.target.value)}
                    placeholder="your.email@example.com"
                    className="w-full"
                    autoComplete="email"
                />
            </FormFieldWrapper>

            <PasswordInput
                label="Password"
                value={data.password}
                onChange={(value) => onChange('password', value)}
                required
                error={errors.password}
                placeholder="Enter your password"
            />

            <div className="flex items-center justify-between text-sm">
                <a href="/forgot-password" className="text-primary hover:underline">
                    Forgot password?
                </a>
            </div>
        </div>
    );
}