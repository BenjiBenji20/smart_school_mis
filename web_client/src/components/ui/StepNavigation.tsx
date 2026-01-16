/**
 * Date Written: 1/15/2026 at 1:36 PM
 */
import { Button } from '@/components/ui/button';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StepNavigationProps {
    currentStep: number;
    totalSteps: number;
    onNext: () => void;
    onBack: () => void;
    isNextDisabled?: boolean;
    isLoading?: boolean;
    nextButtonLabel?: string;
    backButtonLabel?: string;
    submitButtonLabel?: string; 
    showBack?: boolean;
}

export function StepNavigation({
    currentStep,
    totalSteps,
    onNext,
    onBack,
    isNextDisabled = false,
    isLoading = false,
    nextButtonLabel = "Next Step",
    backButtonLabel = "Back",
    submitButtonLabel = "Create Account", 
    showBack = true,
}: StepNavigationProps) {
    const isLastStep = currentStep === totalSteps - 1;

    return (
        <div className={cn(
            "flex items-center gap-4 pt-6 w-full",
            !showBack && "justify-end"
        )}>
            {showBack && (
                <Button
                    type="button"
                    variant="outline"
                    onClick={onBack}
                    className="gap-2"
                    disabled={isLoading}
                >
                    <ArrowLeft className="h-4 w-4" />
                    {backButtonLabel}
                </Button>
            )}

            <Button
                type="button"
                onClick={onNext}
                disabled={isNextDisabled || isLoading}
                className={cn(
                    "gap-2",
                    !showBack ? "w-full" : "flex-1"
                )}
            >
                {isLoading ? (
                    <>
                        <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                        Processing...
                    </>
                ) : (
                    <>
                        {isLastStep ? submitButtonLabel : nextButtonLabel}
                        {!isLastStep && <ArrowRight className="h-4 w-4" />}
                    </>
                )}
            </Button>
        </div>
    );
}