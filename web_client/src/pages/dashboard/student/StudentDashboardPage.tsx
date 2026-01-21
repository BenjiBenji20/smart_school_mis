/**
 * Date Written: 1/16/2026 at 8:08 PM
 */

import cmuLogo from '@/assets/cmu-logo.png'
import type { StudentResponse } from '@/types/authentication.types';
import { DashboardLayout } from '@/components/layout/DashboarLayout';
import { EnrollmentHeader } from '@/components/student/EnrollmentTab/EnrollmentHeader';
import type { TermResponse } from '@/types/academic_structure.types';
import { EnrollmentTable } from '@/components/student/EnrollmentTab/EnrollmentTable';
import { dummyAllowedSections, dummyCurrentTerm } from '@/dummy/dummy_enrollment_data';
import { studentSidebarSections } from '@/components/dashboard/Sidebar/sidebar_sections';
import { useEffect, useState } from 'react';
import { Loader2 } from 'lucide-react';
import { studentApi } from '@/api/v1/student_api';


interface StudentDashboardPageProps {
    isSidebarOpen?: boolean;
    studentId: string;
}

function StudentDashboardPageContent({ isSidebarOpen = true, studentId }: StudentDashboardPageProps) {
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
                        alert("Enrollment successful!)");
                    }}
                    isSidebarOpen={isSidebarOpen}
                />
            </div>
        </>
    );
}

// Export the wrapper that gets injected with isSidebarOpen
export default function StudentDashboardPage() {
    const [user, setUser] = useState<StudentResponse>();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const studentData = await studentApi.getCurrentStudent();
            setUser(studentData)
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (err: any) {
            setError(err.response?.data?.message || "Failed to load student data");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                <span className="ml-2">Loading available enrollment...</span>
            </div>
        );
    }

    return (
        <>
            <title>CMU | Dashboard</title>
            {
                error || !user ? (
                    <div className="text-center py-8 text-red-500">
                        Error: {error}
                    </div>
                ) : (
                    <DashboardLayout
                        user={user}
                        sidebarSections={studentSidebarSections}
                        pageTitle="Student Dashboard / Overview"
                        universityLogo={cmuLogo}
                        onLogout={() => console.log('Logout')}
                    >
                        <StudentDashboardPageContent studentId={user.id} />
                    </DashboardLayout>
                )
            }
        </>
    );
}