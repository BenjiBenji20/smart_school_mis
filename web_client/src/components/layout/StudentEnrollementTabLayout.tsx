// components/enrollment/EnrollmentTab.tsx
"use client";

import { useState, useEffect } from "react";
import { EnrollmentHeader } from "../StudentEnrollment/EnrollmentHeader";
import { EnrollmentTable } from "../StudentEnrollment/EnrollmentTable";
import { Loader2 } from "lucide-react";
import { enrollmentApi } from "@/api/v1/enrollments_and_gradings_api";
import type { TermResponse } from "@/types/academic_structure.types";
import type { AllowedEnrollSectionResponse } from "@/types/enrollments_and_gradings.types";

interface EnrollmentTabProps {
    currentTerm: TermResponse;
    studentId: string;
    isSidebarOpen?: boolean
}

export function StudentEnrollmentTabLayout({ currentTerm, studentId, isSidebarOpen }: EnrollmentTabProps) {
    const [sections, setSections] = useState<AllowedEnrollSectionResponse[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchSections = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await enrollmentApi.getAllowedSections();
            setSections(data);
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (err: any) {
            setError(err.response?.data?.message || "Failed to load sections");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSections();
    }, []);

    const handleEnrollmentSuccess = () => {
        // Refresh the sections list after successful enrollment
        fetchSections();
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                <span className="ml-2">Loading available sections...</span>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <EnrollmentHeader
                term={currentTerm}
                isSidebarOpen={isSidebarOpen}
            />

            <div>
                {error ? (
                    <div className="text-center py-8 text-red-500">
                        Error: {error}
                    </div>
                ) : (
                    <EnrollmentTable
                        sections={sections}
                        studentId={studentId}
                        onEnrollmentSuccess={handleEnrollmentSuccess}
                        isSidebarOpen={isSidebarOpen}
                    />
                )}
            </div>
        </div>
    );
}