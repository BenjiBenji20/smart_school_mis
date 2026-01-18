/**
 * Date Written: 1/15/2026 at 1:54 PM
 */
import { useState } from 'react';
import { RegistrationLayout } from '@/components/registration/layout/RegistrationLayout';
import { BaseRegistrationForm } from '@/components/registration/forms/BaseRegistrationForm';
import { EmployeeAccountInfoStep } from '@/components/registration/forms/steps/EmployeeAccountInfoStep';
import { type EmployeeRegistrationFormData } from '@/types/authentication.types';
import { register } from '@/api/v1/authentication_api';
import { toast } from 'sonner';
import type { UserRole } from '@/types/user_state.enums.types';
import { useNavigate } from 'react-router';

export default function EmployeeRegistrationPage() {
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (data: Omit<EmployeeRegistrationFormData, 'confirmPassword'>) => {
        // Validate role is selected
        if (!data.role) {
            toast.error("Validation Error", {
                description: "Please select a role",
            });
            return;
        }

        setIsLoading(true);
        try {
            const response = await register(data);

            toast.success("Registration Successful!", {
                description: "Your employee account has been created. An administrator will review your registration.",
            });

            // Redirect to success page
            navigate("/register/success", {
                state: { user: response }  
            });
        } catch (error: unknown) {
            const errorMessage =
                error instanceof Object &&
                    'response' in error &&
                    error.response instanceof Object &&
                    'data' in error.response &&
                    error.response.data instanceof Object &&
                    'message' in error.response.data
                    ? (error.response.data.message as string)
                    : "An error occurred. Please try again.";

            toast.error("Registration Failed", {
                description: errorMessage,
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <RegistrationLayout>
            <div className="w-full space-y-8">
                <BaseRegistrationForm
                    accountInfoStep={<EmployeeAccountInfoStep data={{
                        email: '',
                        cellphone_number: '',
                        password: '',
                        confirmPassword: '',
                        role: undefined
                        // eslint-disable-next-line @typescript-eslint/no-unused-vars
                    }} onChange={function (_field: 'confirmPassword' | 'email' | 'cellphone_number' | 'password' | 'role', _value: string | UserRole): void {
                        throw new Error('Function not implemented.');
                    }} />}
                    onSubmit={(data) => handleSubmit(data as Omit<EmployeeRegistrationFormData, 'confirmPassword'>)}
                    isLoading={isLoading}
                    title="Employee Account Registration"
                    stepLabels={["Personal Information", "Employee Account"]}
                />
                <div className="pt-6 border-t text-center">
                    <p className="text-sm text-muted-foreground">
                        Already have an account?{' '}
                        <a href="/login" className="text-primary hover:underline font-medium">
                            Sign in here
                        </a>
                    </p>
                    <p className="text-xs text-muted-foreground mt-2">
                        Are you a student?{' '}
                        <a href="/register/student" className="text-secondary hover:underline">
                            Register as student
                        </a>
                    </p>
                </div>
            </div>
        </RegistrationLayout>
    );
}