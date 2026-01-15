/**
 * Date Written: 1/15/2026 at 1:29 PM
 */
import React from 'react';
import { cn } from '@/lib/utils';

interface RegistrationFormStepsProps {
    currentStep: number;
    totalSteps: number;
    stepLabels?: string[];
    className?: string;
}

export function RegistrationFormSteps({
    currentStep,
    totalSteps,
    stepLabels = [],
    className,
}: RegistrationFormStepsProps) {
    return (
        <div className={cn("flex items-center justify-between w-full", className)}>
            {Array.from({ length: totalSteps }).map((_, index) => (
                <React.Fragment key={index}>
                    <div className="flex flex-col items-center gap-2">
                        <div
                            className={cn(
                                "w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold transition-all",
                                index === currentStep
                                    ? "bg-primary text-primary-foreground"
                                    : index < currentStep
                                        ? "bg-primary/20 text-primary"
                                        : "bg-muted text-muted-foreground"
                            )}
                        >
                            {index + 1}
                        </div>
                        {stepLabels[index] && (
                            <span 
                                className={cn(
                                    "text-sm font-medium transition-colors whitespace-nowrap",
                                    index === currentStep
                                        ? "text-primary"
                                        : "text-muted-foreground"
                                )}
                            >
                                {stepLabels[index]}
                            </span>
                        )}
                    </div>
                    
                    {index < totalSteps - 1 && (
                        <div
                            className={cn(
                                "flex-1 h-0.5 mx-4 transition-colors",
                                index < currentStep ? "bg-primary" : "bg-muted"
                            )}
                        />
                    )}
                </React.Fragment>
            ))}
        </div>
    );
}