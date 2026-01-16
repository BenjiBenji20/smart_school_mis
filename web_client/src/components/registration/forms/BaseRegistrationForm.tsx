/**
 * Date Written: 1/15/2026 at 1:41 PM
 */

import React, { useState } from 'react';
import { RegistrationFormSteps } from '@/components/ui/RegistrationFormSteps';
import { StepNavigation } from '@/components/ui/StepNavigation';
import { PersonalInfoStep } from './steps/PersonalInfoStep';
import { type EmployeeRegistrationFormData } from '@/types/authentication.types';

interface BaseRegistrationFormProps {
    accountInfoStep: React.ReactNode;
    totalSteps?: number;
    stepLabels?: string[];
    onSubmit: (data: Omit<EmployeeRegistrationFormData, 'confirmPassword'>) => Promise<void>;
    isLoading?: boolean;
    title?: string;
}

export function BaseRegistrationForm({
    accountInfoStep,
    totalSteps = 2,
    stepLabels = ["Personal Information", "Account Information"],
    onSubmit,
    isLoading = false,
    title,
}: BaseRegistrationFormProps) {
    const [currentStep, setCurrentStep] = useState(0);
    const [formData, setFormData] = useState<EmployeeRegistrationFormData>({
        first_name: '',
        middle_name: null,
        last_name: '',
        suffix: null,
        age: undefined,
        gender: 'Male',
        complete_address: '',
        email: '',
        cellphone_number: '',
        password: '',
        confirmPassword: '',
        role: undefined,
    });
    const [errors, setErrors] = useState<Record<string, string>>({});

    const handleFieldChange = (field: keyof EmployeeRegistrationFormData, value: unknown) => {
        setFormData(prev => ({ ...prev, [field]: value }));
        if (errors[field]) {
            setErrors(prev => ({ ...prev, [field]: '' }));
        }
    };

    const validateCurrentStep = () => {
        const newErrors: Record<string, string> = {};

        if (currentStep === 0) {
            if (!formData.first_name.trim()) newErrors.first_name = "First name is required";
            if (!formData.last_name.trim()) newErrors.last_name = "Last name is required";
            if (!formData.gender) newErrors.gender = "Gender is required";
            if (formData.age && (formData.age < 16 || formData.age > 100)) {
                newErrors.age = "Age must be between 16 and 100";
            }
        } else if (currentStep === 1) {
            if (!formData.email.trim()) newErrors.email = "Email is required";
            else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = "Invalid email format";

            if (!formData.cellphone_number.trim()) newErrors.cellphone_number = "Phone number is required";
            else if (!/^[0-9+\-\s]{10,}$/.test(formData.cellphone_number)) {
                newErrors.cellphone_number = "Invalid phone number format";
            }

            if (!formData.password) newErrors.password = "Password is required";
            else if (formData.password.length < 8) newErrors.password = "Password must be at least 8 characters";

            if (formData.password !== formData.confirmPassword) {
                newErrors.confirmPassword = "Passwords do not match";
            }
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleNext = () => {
        if (validateCurrentStep()) {
            if (currentStep < totalSteps - 1) {
                setCurrentStep(prev => prev + 1);
            } else {
                handleSubmit();
            }
        }
    };

    const handleBack = () => {
        if (currentStep > 0) {
            setCurrentStep(prev => prev - 1);
        }
    };

    const handleSubmit = async () => {
        if (validateCurrentStep()) {
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            const { confirmPassword, ...submitData } = formData;
            try {
                await onSubmit(submitData);
            } catch (error) {
                console.error('Registration failed:', error);
            }
        }
    };

    // Clone the accountInfoStep element and inject the props
    const accountInfoStepWithProps = React.isValidElement(accountInfoStep)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        ? React.cloneElement(accountInfoStep as React.ReactElement<any>, {
            data: formData,
            onChange: handleFieldChange,
            errors: errors,
        })
        : accountInfoStep;

    return (
        <div className="w-full space-y-6">
            <div className="space-y-2">
                <h2 className="text-3xl font-bold text-foreground">{title}</h2>
                <p className="text-muted-foreground">
                    Please provide your information to register
                </p>
            </div>
            <RegistrationFormSteps
                currentStep={currentStep}
                totalSteps={totalSteps}
                stepLabels={stepLabels}
            />

            <div className="w-full py-6">
                {currentStep === 0 ? (
                    <PersonalInfoStep
                        data={formData}
                        onChange={handleFieldChange}
                        errors={errors}
                    />
                ) : (
                    accountInfoStepWithProps
                )}
            </div>

            <StepNavigation
                currentStep={currentStep}
                totalSteps={totalSteps}
                onNext={handleNext}
                onBack={handleBack}
                isNextDisabled={isLoading}
                isLoading={isLoading}
                showBack={currentStep > 0}
            />
        </div>
    );
}