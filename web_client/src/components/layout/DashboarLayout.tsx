/**
 * Date Written: 1/17/2026 at 11:38 AM
 * Updated: 1/17/2026 at 12:00 PM - Fixed responsive margin
 */
import { SidebarProvider, useSidebar } from '@/components/ui/sidebar';
import { SidebarLayout } from '@/components/dashboard/Sidebar/SidebarLayout';
import { MobileSidebar } from '@/components/dashboard/Sidebar/MobileSidebar';
import { TopNavigation } from '@/components/layout/TopNavigationLayout';
import { type BaseUserResponse, type StudentResponse } from '@/types/authentication.types';
import { type ReactNode } from 'react';
import { cn } from '@/lib/utils';
import React from 'react';

interface DashboardLayoutProps {
    user: BaseUserResponse | StudentResponse;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    sidebarSections: any[];
    children: ReactNode;
    pageTitle?: string;
    universityLogo?: string;
    onLogout?: () => void;
}

// Inner component that can use the sidebar context
function DashboardLayoutInner({
    user,
    sidebarSections,
    children,
    pageTitle = "Dashboard",
    universityLogo,
    onLogout,
}: DashboardLayoutProps) {
    const { open, setOpen } = useSidebar();

    return (
        <div className="min-h-screen w-full bg-background overflow-x-hidden">
            {/* Desktop Sidebar - Fixed */}
            <div className="hidden lg:block fixed left-0 top-0 h-screen z-30">
                <SidebarLayout
                    sections={sidebarSections}
                    universityName="City of Malabon University"
                    universityLogo={universityLogo}
                    onLogout={onLogout}
                    collapsed={!open}
                    onCollapseChange={(collapsed) => setOpen(!collapsed)}
                />
            </div>

            {/* Main Content - Responsive margin based on sidebar state */}
            <div className={cn(
                "w-full transition-all duration-300",
                open ? "lg:ml-64" : "lg:ml-15",
                "ml-0"
            )}>
                {/* Top Navigation */}
                <TopNavigation
                    user={user}
                    pageTitle={pageTitle}
                    onLogout={onLogout}
                    onToggleSidebar={() => setOpen(!open)}
                    isSidebarOpen={open}
                />

                {/* Mobile Sidebar - Hidden on desktop */}
                <div className="lg:hidden">
                    <MobileSidebar
                        sections={sidebarSections}
                        universityName="City of Malabon University"
                        universityLogo={universityLogo}
                        onLogout={onLogout}
                    />
                </div>

                {/* Page Content */}
                <main className="p-4 md:p-6 lg:p-8">
                    {/* Clone children and pass isSidebarOpen prop */}
                    {React.Children.map(children, child => {
                        if (React.isValidElement(child)) {
                            return React.cloneElement(child, {
                                isSidebarOpen: open
                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                            } as any);
                        }
                        return child;
                    })}
                </main>
            </div>
        </div>
    );
}

export function DashboardLayout(props: DashboardLayoutProps) {
    return (
        <SidebarProvider defaultOpen={true}>
            <DashboardLayoutInner {...props} />
        </SidebarProvider>
    );
}