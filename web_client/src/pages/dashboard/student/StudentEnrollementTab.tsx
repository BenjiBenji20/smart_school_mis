/**
 * Date Written: 1/19/2026 at 9:08 AM
 */

"use client";

import { useState, useEffect } from "react";
import { EnrollmentHeader } from "../../../components/student/EnrollmentTab/EnrollmentHeader";
import { EnrollmentTable } from "../../../components/student/EnrollmentTab/EnrollmentTable";
import { Loader2 } from "lucide-react";
import { enrollmentApi } from "@/api/v1/enrollments_and_gradings_api";
import type { AllowedEnrollSectionResponse } from "@/types/enrollments_and_gradings.types";
import { DashboardLayout } from "@/components/layout/DashboarLayout";
import cmuLogo from '@/assets/cmu-logo.png'
import { studentSidebarSections } from '@/components/dashboard/Sidebar/sidebar_sections';
import type { TermResponse } from "@/types/academic_structure.types";
import { studentApi } from "@/api/v1/student_api";
import type { StudentResponse } from "@/types/authentication.types";

interface StudentEnrollTabContentProps {
    isSidebarOpen?: boolean;
    studentId: string;
}

function StudentEnrollmentTabContent({ isSidebarOpen, studentId }: StudentEnrollTabContentProps) {
    const [allowedSections, setAllowedSections] = useState<AllowedEnrollSectionResponse[]>([]);
    const [nextTerm, setNextTerm] = useState<TermResponse>();

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const allowedSectionsData = await enrollmentApi.getAllowedSections();
            setAllowedSections(allowedSectionsData);

            const nextTermData = await studentApi.getMyNextTerm();
            setNextTerm(nextTermData)

            // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (err: any) {
            setError(err.response?.data?.message || "Failed to load enrollment data");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleEnrollmentSuccess = () => {
        // Refresh the enrollment list after successful enrollment
        fetchData();
    };

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

            {
                error || !nextTerm ? (
                    <div className="text-center py-8 text-red-500">
                        Error: {error}
                    </div>
                ) : (
                    <div className="space-y-6">
                        <EnrollmentHeader
                            term={nextTerm}
                            isSidebarOpen={isSidebarOpen}
                        />

                        <div>
                            <EnrollmentTable
                                sections={allowedSections}
                                studentId={studentId}
                                onEnrollmentSuccess={handleEnrollmentSuccess}
                                isSidebarOpen={isSidebarOpen}
                                isForEnrollment={true}
                                tableTitle="Available Sections"
                            />
                        </div>
                    </div>
                )
            }
        </>
    );
}


// Export the wrapper that gets injected with isSidebarOpen
export default function StudentEnrollmentTab() {
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
            <title>CMU | Enrollment</title>
            {
                error || !user ? (
                    <div className="text-center py-8 text-red-500">
                        Error: {error}
                    </div>
                ) : (
                    <DashboardLayout
                        user={user}
                        sidebarSections={studentSidebarSections}
                        pageTitle="Student / Enrollment"
                        universityLogo={cmuLogo}
                        onLogout={() => console.log('Logout')}
                    >
                        <StudentEnrollmentTabContent studentId={user.id} />
                    </DashboardLayout>
                )
            }
        </>
    );
}
