/**
 * Date Written: 1/15/2026 at 1:29 PM - FIXED TO MATCH UI
 */
import React from 'react';
import { cn } from '@/lib/utils';
import { RegistrationImageSection } from './RegistrationImageSection';

interface RegistrationLayoutProps {
    children: React.ReactNode;
    className?: string;
    title?: string;
    subtitle?: string;
    showFooter?: boolean;
}

export function RegistrationLayout({
    children,
    className,
    title,
    subtitle,
    showFooter = true,
}: RegistrationLayoutProps) {
    return (
        <div className="min-h-screen bg-background">
            <div className="flex flex-col lg:flex-row min-h-screen">
                {/* Left Image Section - Hidden on mobile, shown on lg+ */}
                <div className="hidden lg:block lg:w-1/2 fixed inset-y-0 left-0">
                    <RegistrationImageSection />
                </div>
                {/* Right Form Section - Takes the other half */}
                <div className="flex-1 lg:ml-[60%] flex flex-col">

                    {/* Mobile Header - Only shown on small screens */}
                    <div className="lg:hidden py-8 px-6 text-center bg-background">
                        <h1 className="text-2xl font-bold text-primary">City of Malabon University</h1>
                        <p className="text-muted-foreground mt-2">Honoring the Past, Shaping the Future</p>
                    </div>

                    {/* Main Form Content */}
                    <div className={cn(
                        "flex-1 flex items-center justify-center p-4 sm:p-6 md:p-8",
                        className
                    )}>
                        <div className="w-full max-w-md">
                            {children}
                        </div>
                    </div>

                    {/* Footer - Only shown if enabled */}
                    {showFooter && (
                        <div className="py-4 px-6 text-center text-sm text-muted-foreground border-t">
                            <p>© {new Date().getFullYear()} City of Malabon University</p>
                            <p className="mt-1 text-xs">
                                Advancing academic excellence and community service through innovative learning and character development.
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}