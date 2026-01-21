/**
 * Date Written: 1/16/2026 at 3:40 PM
 */
import { useState } from 'react';
import { BaseAuthenticationForm } from '@/components/authentication/BaseAuthenticationForm';
import { FaceRecognitionStep } from '@/components/authentication/FaceRecognition';
import { type CredentialValidator } from '@/types/authentication.types';
import { authenticate } from '@/api/v1/authentication_api';
import { toast } from 'sonner';
import { useNavigate } from 'react-router';
import { AuthenticationLayout } from '@/components/authentication/AuthenticationLayout';

export default function UserAuthenticationPage() {
    const [isLoading, setIsLoading] = useState(false);
    const [capturedImage, setCapturedImage] = useState<string | null>(null);
    const navigate = useNavigate();

    const handleSubmit = async (data: CredentialValidator) => {
        setIsLoading(true);
        try {
            // Include face recognition data if captured
            const loginData = {
                ...data,
            };

            const response = await authenticate(loginData);
            console.log(response)


            // Determine route based on role
            let fullRoute = "/dashboard";

            if (response.role == 'Student') {
                fullRoute = "/student/dashboard";
            } else if (response.role == 'Administrator') {
                fullRoute = "/administrator/dashboard";
            } else if (response.role == 'Dean') {
                fullRoute = "/dean/dashboard";
            } else if (response.role == 'Registrar') {
                fullRoute = "/registrar/dashboard";
            } else if (response.role == 'Program Chair') {
                fullRoute = "/program-chair/dashboard";
            }

            toast.success("Login Successful!", {
                description: "Welcome back to City of Malabon University",
            });

            // Redirect to dashboard based on user role
            navigate(fullRoute, {
                state: { user: response }
            });

        } catch (error: unknown) {
            const errorMessage = error instanceof Error
                ? error.message
                : "Invalid credentials. Please try again.";

            toast.error("Login Failed", {
                description: errorMessage,
            });
        } finally {
            setIsLoading(false);
        }
    };

    const handleFaceCapture = (imageData: string) => {
        setCapturedImage(imageData);
        toast.success("Face captured successfully!");
    };

    const faceRecognitionStep = (
        <FaceRecognitionStep onCapture={handleFaceCapture} />
    );

    return (
        <AuthenticationLayout>
            <div className="w-full space-y-8">
                <BaseAuthenticationForm
                    faceRecognitionStep={faceRecognitionStep}
                    onSubmit={handleSubmit}
                    isLoading={isLoading}
                    title="Sign In"
                    subtitle="Enter your credentials to access your account"
                    enableFaceRecognition={true} // Set to false to disable face recognition
                />

                <div className="pt-6 border-t text-center space-y-3">
                    <p className="text-sm text-muted-foreground">
                        Don't have an account?{' '}
                        <a href="/register/student" className="text-primary hover:underline font-medium">
                            Register as Student
                        </a>
                        {' or '}
                        <a href="/register/employee" className="text-primary hover:underline font-medium">
                            Employee
                        </a>
                    </p>

                    <p className="text-xs text-muted-foreground">
                        Having trouble logging in?{' '}
                        <a href="/support" className="text-secondary hover:underline">
                            Contact Support
                        </a>
                    </p>
                </div>
            </div>
        </AuthenticationLayout>
    );
}
