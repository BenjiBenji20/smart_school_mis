/**
 * Date Written: 1/16/2026 at 4:03 PM
 */
import React, { useState } from 'react';
import { RegistrationFormSteps } from '@/components/ui/RegistrationFormSteps';
import { StepNavigation } from '@/components/ui/StepNavigation';
import { CredentialStep } from './CredentialStep';
import { type CredentialValidator } from '@/types/authentication.types';

interface BaseAuthenticationFormProps {
    faceRecognitionStep?: React.ReactNode;
    onSubmit: (data: CredentialValidator) => Promise<void>;
    isLoading?: boolean;
    title?: string;
    subtitle?: string;
    enableFaceRecognition?: boolean;
}

export function BaseAuthenticationForm({
    faceRecognitionStep,
    onSubmit,
    isLoading = false,
    title = "Welcome Back",
    subtitle = "Sign in to your account",
    enableFaceRecognition = false,
}: BaseAuthenticationFormProps) {
    const totalSteps = enableFaceRecognition ? 2 : 1;
    const [currentStep, setCurrentStep] = useState(0);
    const [formData, setFormData] = useState<CredentialValidator>({
        email: '',
        password: '',
    });
    const [errors, setErrors] = useState<Record<string, string>>({});

    const handleFieldChange = (field: keyof CredentialValidator, value: string) => {
        setFormData(prev => ({ ...prev, [field]: value }));
        if (errors[field]) {
            setErrors(prev => ({ ...prev, [field]: '' }));
        }
    };

    const validateCredentials = () => {
        const newErrors: Record<string, string> = {};

        if (!formData.email.trim()) {
            newErrors.email = "Email is required";
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = "Invalid email format";
        }

        if (!formData.password) {
            newErrors.password = "Password is required";
        } else if (formData.password.length < 8) {
            newErrors.password = "Password must be at least 8 characters";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleNext = () => {
        if (currentStep === 0) {
            if (!validateCredentials()) return;

            if (enableFaceRecognition) {
                setCurrentStep(1);
            } else {
                handleSubmit();
            }
        } else {
            handleSubmit();
        }
    };

    const handleBack = () => {
        if (currentStep > 0) {
            setCurrentStep(prev => prev - 1);
        }
    };

    const handleSubmit = async () => {
        if (!validateCredentials()) return;

        try {
            await onSubmit(formData);
        } catch (error) {
            console.error('Authentication failed:', error);
        }
    };

    return (
        <div className="w-full space-y-6">
            <div className="space-y-2">
                <h2 className="text-3xl font-bold text-foreground">{title}</h2>
                <p className="text-muted-foreground">{subtitle}</p>
            </div>

            {enableFaceRecognition && (
                <RegistrationFormSteps
                    currentStep={currentStep}
                    totalSteps={totalSteps}
                    stepLabels={["Enter Credentials", "Face Recognition"]}
                />
            )}

            <div className="w-full">
                {currentStep === 0 ? (
                    <CredentialStep
                        data={formData}
                        onChange={handleFieldChange}
                        errors={errors}
                    />
                ) : (
                    faceRecognitionStep
                )}
            </div>

            <StepNavigation
                currentStep={currentStep}
                totalSteps={totalSteps}
                onNext={handleNext}
                onBack={handleBack}
                isNextDisabled={isLoading}
                isLoading={isLoading}
                showBack={currentStep > 0 && enableFaceRecognition}
                nextButtonLabel="Next Step"
                submitButtonLabel="Sign In" 
            />
        </div>
    );
}