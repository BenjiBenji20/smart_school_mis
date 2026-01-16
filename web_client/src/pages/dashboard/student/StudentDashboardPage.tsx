/**
 * Date Written: 1/16/2026 at 8:08 PM
 */

import { SidebarLayout } from '../../../components/dashboard/Sidebar/SidebarLayout';
import { MobileSidebar } from '../../../components/dashboard/Sidebar/MobileSidebar';
import { sidebarIcons } from '../../../components/dashboard/icon_constants';
import { SidebarProvider } from '../../../components/ui/sidebar';
import cmuLogo from '@/assets/cmu-logo.png'

// Student menu sections
const sections = [
    {
        title: "STUDENT MENU",
        items: [
            {
                title: "Dashboard",
                url: "/student/dashboard",
                icon: sidebarIcons.Dashboard,
                isActive: true,
            },
            {
                title: "Academics",
                url: "#",
                icon: sidebarIcons.Academics,
                submenu: [
                    {
                        title: "Enrollment",
                        url: "/student/enrollment",
                        badge: "3",
                    },
                    {
                        title: "Courses",
                        url: "/student/courses",
                    },
                    {
                        title: "Grades",
                        url: "/student/grades",
                        isActive: true,
                    },
                    {
                        title: "Schedule",
                        url: "/student/schedule",
                    },
                ],
            },
            {
                title: "Assignments",
                url: "#",
                icon: sidebarIcons.Submissions,
                badge: "2",
                submenu: [
                    {
                        title: "Pending",
                        url: "/student/assignments/pending",
                        badge: "2",
                    },
                    {
                        title: "Submitted",
                        url: "/student/assignments/submitted",
                    },
                    {
                        title: "Graded",
                        url: "/student/assignments/graded",
                    },
                ],
            },
            {
                title: "AI Tools",
                url: "#",
                icon: sidebarIcons['AI Analytics'],
                submenu: [
                    {
                        title: "AI Analytics",
                        url: "/student/ai-analytics",
                    },
                    {
                        title: "AI Assistant",
                        url: "/student/ai-assistant",
                    },
                    {
                        title: "Study Planner",
                        url: "/student/study-planner",
                    },
                ],
            },
            {
                title: "Records",
                url: "/student/records",
                icon: sidebarIcons.Records,
            },
            {
                title: "Settings",
                url: "/student/settings",
                icon: sidebarIcons.Settings,
            },
            {
                title: "Help Center",
                url: "/student/help",
                icon: sidebarIcons.Help,
            },
        ],
    }
];

export default function StudentDashboardPage() {
    const handleLogout = () => {
        console.log('Logging out...');
        // Implement logout logic
    };

    return (
        <SidebarProvider >
            <div className="flex min-h-screen">
                {/* Desktop Sidebar */}
                <div className="hidden lg:block">
                    <SidebarLayout
                        sections={sections}
                        universityName="City of Malabon University"
                        universityLogo={cmuLogo}
                        onLogout={handleLogout}
                    />
                </div>

                {/* Mobile Sidebar Trigger */}
                <div className="lg:hidden fixed top-4 left-4 z-50">
                    <MobileSidebar
                        sections={sections}
                        universityName="City of Malabon University"
                        universityLogo={cmuLogo}
                        onLogout={handleLogout}
                    />
                </div>

                {/* Main Content */}
                <div className="flex-1 p-6">
                    <h1 className="text-2xl font-bold">Welcome back, Alex!</h1>
                    {/* Your dashboard content here */}
                </div>
            </div>
        </SidebarProvider>

    );
}
