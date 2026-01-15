/**
 * Date Written: 1/15/2026 at 1:46 PM
 */
import { useState } from 'react';
import { RegistrationLayout } from '@/components/registration/layout/RegistrationLayout';
import { BaseRegistrationForm } from '@/components/registration/forms/BaseRegistrationForm';
import { StudentAccountInfoStep } from '@/components/registration/forms/steps/StudentAccountInfoStep';
import { type RegistrationFormData } from '@/types/authentication.types';
import { register } from '@/api/v1/authentication_api';
import { toast } from 'sonner';

export default function StudentRegistrationPage() {
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (data: Omit<RegistrationFormData, "confirmPassword">) => {
        setIsLoading(true);
        try {
            // Add student role
            const studentData = {
                ...data,
                role: 'Student' as const
            };

            await register(studentData);

            toast.success("Registration Successful!", {
                description: "Your student account has been created. Please check your email for verification.",
            });

            // Redirect to login or dashboard
            // router.push('/login');
        } catch (error: unknown) {
            const errorMessage = error instanceof Error ? error.message : "An error occurred. Please try again.";

            toast.error("Registration Failed", {
                description: errorMessage,
            });
        } finally {
            setIsLoading(false);
        }
    };

    const accountInfoStep = (
        <StudentAccountInfoStep
            data={{
                email: '',
                cellphone_number: '',
                password: '',
                confirmPassword: '',
            }}
            onChange={() => { }}
            errors={{}}
        />
    );

    return (
        <RegistrationLayout>
            <div className="w-full space-y-8">
                <BaseRegistrationForm
                    accountInfoStep={accountInfoStep}
                    onSubmit={handleSubmit}
                    isLoading={isLoading}
                    stepLabels={["Personal Information", "Student Account"]}
                />
                <div className="pt-6 border-t text-center">
                    <p className="text-sm text-muted-foreground">
                        Already have an account?{' '}
                        <a href="/login" className="text-primary hover:underline font-medium">
                            Sign in here
                        </a>
                    </p>
                    <p className="text-xs text-muted-foreground mt-2">
                        Are you a university employee?{' '}
                        <a href="/register/employee" className="text-secondary hover:underline">
                            Register as employee
                        </a>
                    </p>
                </div>
            </div>
        </RegistrationLayout>
    );
}