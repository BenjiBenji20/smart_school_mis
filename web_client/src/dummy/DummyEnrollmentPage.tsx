// app/student/enrollment/page.tsx
"use client";

import { useState, useEffect } from "react";
import { EnrollmentHeader } from "@/components/StudentEnrollment/EnrollmentHeader";
import { EnrollmentTable } from "@/components/StudentEnrollment/EnrollmentTable";
import { Loader2 } from "lucide-react";
import type { AllowedEnrollSectionResponse } from "@/types/enrollments_and_gradings.types";
import type { TermResponse } from "@/types/academic_structure.types";
import { dummyCurrentTerm } from "@/dummy/dummy_enrollment_data";
import { mockEnrollmentApi } from "@/dummy/dummy_enrollment_data";

// Create a custom hook to simulate API calls
function useMockEnrollment() {
    const [sections, setSections] = useState<AllowedEnrollSectionResponse[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchSections = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await mockEnrollmentApi.getAllowedSections();
            setSections(data);
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (err: any) {
            setError(err.response?.data?.message || "Failed to load sections");
        } finally {
            setLoading(false);
        }
    };

    const enrollStudent = async (studentId: string, classSectionId: string) => {
        // eslint-disable-next-line no-useless-catch
        try {
            return await mockEnrollmentApi.enrollStudentClassSection(studentId, classSectionId);
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (err: any) {
            throw err;
        }
    };

    return { sections, loading, error, fetchSections, enrollStudent };
}

export default function StudentEnrollmentPage() {
    const { sections, loading, error, fetchSections } = useMockEnrollment();
    const studentId = "2024-84921"; // From your user object

    useEffect(() => {
        fetchSections();
    }, []);

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
            <EnrollmentHeader term={dummyCurrentTerm as TermResponse} />

            <div>
                <h2 className="text-lg font-semibold mb-4">Available Sections</h2>
                {error ? (
                    <div className="text-center py-8 text-red-500">
                        Error: {error}
                    </div>
                ) : (
                    <EnrollmentTable
                        sections={sections}
                        studentId={studentId}
                        onEnrollmentSuccess={() => {
                            console.log("Enrollment successful!");
                            // Optionally refresh the list
                            // fetchSections();
                        }}
                    />
                )}
            </div>
        </div>
    );
}