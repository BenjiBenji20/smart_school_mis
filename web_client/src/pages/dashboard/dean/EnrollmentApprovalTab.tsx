/**
 * Date Written: 1/23/2026 at 4:47 PM
 */

"use client";

import { useState, useEffect } from "react";
import { EnrollmentHeader } from "../../../components/enrollment/EnrollmentTab/EnrollmentHeader";
import { Loader2 } from "lucide-react";
import type { EnrollmentResponse } from "@/types/enrollments_and_gradings.types";
import { DashboardLayout } from "@/components/layout/DashboarLayout";
import cmuLogo from '@/assets/cmu-logo.png'
import { deanSidebarSections } from '@/components/dashboard/Sidebar/sidebar_sections';
import type { TermResponse } from "@/types/academic_structure.types";
import { studentApi } from "@/api/v1/student_api";
import type { DeanResponse } from "@/types/authentication.types";
import { enrollmentApi } from "@/api/v1/enrollments_and_gradings_api";
import { EnrollmentApprovalTable } from "@/components/enrollment/EnrollmentTab/EnrollmentApprovalTable";
import { deanApi } from "@/api/v1/dean_api";

interface DeanEnrollmentApprovalTabContentProps {
    isSidebarOpen?: boolean;
}

function DeanEnrollmentApprovalTabContent({ isSidebarOpen }: DeanEnrollmentApprovalTabContentProps) {
    const [enrollmentData, setEnrollmentData] = useState<EnrollmentResponse[]>([]);
    const [currentTerm, setCurrentTerm] = useState<TermResponse>();

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const enrollmentDataData = await enrollmentApi.getAllEnrollments();
            setEnrollmentData(enrollmentDataData);

            const currentTermData = await studentApi.getMyNextTerm();
            setCurrentTerm(currentTermData)

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
                error || !currentTerm ? (
                    <div className="text-center py-8 text-red-500">
                        Error: {error}
                    </div>
                ) : (
                    <div className="space-y-6">
                        <EnrollmentHeader
                            term={currentTerm}
                            isSidebarOpen={isSidebarOpen}
                        />

                        <div>
                            <EnrollmentApprovalTable
                                enrollmentData={enrollmentData}
                                isSidebarOpen={isSidebarOpen}
                                onEnrollmentSuccess={handleEnrollmentSuccess}
                                tableTitle="Enrollment Queue"
                            />
                        </div>
                    </div>
                )
            }
        </>
    );
}


// Export the wrapper that gets injected with isSidebarOpen
export default function DeanEnrollmentApprovalTab() {
    const [user, setUser] = useState<DeanResponse>();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const deanData = await deanApi.getCurrentDean();
            setUser(deanData)
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
                        sidebarSections={deanSidebarSections}
                        pageTitle="Dean / Enrollment Approval"
                        universityLogo={cmuLogo}
                        onLogout={() => console.log('Logout')}
                    >
                        <DeanEnrollmentApprovalTabContent />
                    </DashboardLayout>
                )
            }
        </>
    );
}
