/**
 * Date Written: 1/15/2026 at 1:34 PM
 */
import React from 'react';
import { cn } from '@/lib/utils';
import { Label } from "@/components/ui/label"

interface FormFieldWrapperProps {
    label: string;
    required?: boolean;
    error?: string;
    children: React.ReactNode;
    className?: string;
}

export function FormFieldWrapper({
    label,
    required = false,
    error,
    children,
    className,
}: FormFieldWrapperProps) {
    return (
        <div className={cn("w-full space-y-2 text-left", className)}>
            <Label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                {label}
                {required && <span className="text-destructive ml-1">*</span>}
            </Label>
            <div className="w-full">
                {children}
            </div>
            {error && (
                <p className="text-sm text-destructive">{error}</p>
            )}
        </div>
    );
}