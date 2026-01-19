/**
 * Date Written: 1/16/2026 at 8:08 PM
 */

import { sidebarIcons } from '../../../components/dashboard/icon_constants';
import cmuLogo from '@/assets/cmu-logo.png'
import type { BaseUserResponse } from '@/types/authentication.types';
import { DashboardLayout } from '@/components/layout/DashboarLayout';
import { EnrollmentHeader } from '@/components/StudentEnrollment/EnrollmentHeader';
import type { TermResponse } from '@/types/academic_structure.types';
import { EnrollmentTable } from '@/components/StudentEnrollment/EnrollmentTable';
import { dummyAllowedSections, dummyCurrentTerm } from '@/dummy/dummy_enrollment_data';

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

// Test only
const user = {
    id: '2024-84921',
    created_at: new Date(),
    first_name: 'Alex',
    middle_name: 'M.',
    last_name: 'Rivera',
    suffix: null,
    age: 21,
    gender: 'Male',
    complete_address: '123 University Ave',
    email: 'alex.rivera@cityofmalabonuniversity.edu.ph',
    cellphone_number: '09123456789',
    role: 'Student',
    is_active: true,
} as BaseUserResponse;

interface StudentDashboardPageProps {
    isSidebarOpen?: boolean; // This will be injected by DashboardLayout
}

function StudentDashboardPageContent({ isSidebarOpen = true }: StudentDashboardPageProps) {
    const studentId = "2024-84921";

    return (
        <>
            <EnrollmentHeader
                term={dummyCurrentTerm as TermResponse}
                isSidebarOpen={isSidebarOpen}
            />
            <div>
                <EnrollmentTable
                    sections={dummyAllowedSections}
                    studentId={studentId}
                    onEnrollmentSuccess={() => {
                        alert("Enrollment successful! (This is a demo)");
                    }}
                    isSidebarOpen={isSidebarOpen}
                />
            </div>
        </>
    );
}

// Export the wrapper that gets injected with isSidebarOpen
export default function StudentDashboardPage() {
    return (
        <DashboardLayout
            user={user}
            sidebarSections={sections}
            pageTitle="Student Dashboard / Overview"
            universityLogo={cmuLogo}
            onLogout={() => console.log('Logout')}
        >
            <StudentDashboardPageContent />
        </DashboardLayout>
    );
}