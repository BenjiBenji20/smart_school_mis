/**
 * Date Written: 1/19/2026 at 12:00 PM
 */

"use client";

import { useState, useMemo } from "react";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { AlertCircle, Search } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import type { AllowedEnrollSectionResponse } from "@/types/enrollments_and_gradings.types";
import { enrollmentApi } from "@/api/v1/enrollments_and_gradings_api";
import { cn } from "@/lib/utils";
import { EnrollmentTableButton } from "./EnrollmentTableButton";
import { studentApi } from "@/api/v1/student_api";

interface EnrollmentTableProps {
    sections: AllowedEnrollSectionResponse[];
    studentId: string;
    onEnrollmentSuccess?: () => void;
    isSidebarOpen?: boolean;
    isForEnrollment?: boolean;
    tableTitle?: string;
}

export function EnrollmentTable({
    sections,
    studentId,
    onEnrollmentSuccess,
    isSidebarOpen,
    isForEnrollment,
    tableTitle
}: EnrollmentTableProps) {
    const [enrollingId, setEnrollingId] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState("");

    const formatTime = (time: string | null) => {
        if (!time) return "TBA";
        try {
            return new Date(`1970-01-01T${time}`).toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit',
                hour12: true
            });
        } catch {
            return time;
        }
    };

    const getDayName = (day: number | null) => {
        if (!day) return "TBA";
        const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
        return days[day - 1] || `Day ${day}`;
    };

    const handleEnroll = async (classSectionId: string) => {
        setEnrollingId(classSectionId);
        setError(null);
        setSuccess(null);

        try {
            await enrollmentApi.enrollStudentClassSection(studentId, classSectionId);
            setSuccess("Successfully enrolled in the course!");
            if (onEnrollmentSuccess) {
                onEnrollmentSuccess();
            }
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (err: any) {
            setError(err.response?.data?.message || "Failed to enroll. Please try again.");
        } finally {
            setEnrollingId(null);
        }
    };

    const handleRemove = async (classSectionId: string) => {
        setEnrollingId(classSectionId);
        setError(null);
        setSuccess(null);

        try {
            await studentApi.removeEnrollment(classSectionId);
            setSuccess("Removed the course.");
            if (onEnrollmentSuccess) {
                onEnrollmentSuccess();
            }
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (err: any) {
            setError(err.response?.data?.message || "Failed to remove enrollment. Please try again.");
        } finally {
            setEnrollingId(null);
        }
    };

    // Filter sections based on search query
    const filteredSections = useMemo(() => {
        if (!searchQuery.trim()) return sections;

        const query = searchQuery.toLowerCase();
        return sections.filter(section =>
            section.course_code?.toLowerCase().includes(query) ||
            section.title.toLowerCase().includes(query) ||
            section.section_code.toLowerCase().includes(query) ||
            section.assigned_professor?.toLowerCase().includes(query) ||
            section.room_code?.toLowerCase().includes(query)
        );
    }, [sections, searchQuery]);

    return (
        <div className={cn(
            "rounded-md bg-card border space-y-4",
            isSidebarOpen ? "max-w-[1220px]" : "max-w-[1400px]"
        )}>
            {error && (
                <Alert variant="destructive" className="py-2 px-3">
                    <AlertCircle className="h-3.5 w-3.5" />
                    <AlertDescription className="text-xs ml-2">{error}</AlertDescription>
                </Alert>
            )}

            {success && (
                <Alert className="bg-green-50 text-green-800 border-green-200 py-2 px-3">
                    <AlertCircle className="h-3.5 w-3.5" />
                    <AlertDescription className="text-xs ml-2">{success}</AlertDescription>
                </Alert>
            )}

            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 py-4 px-8">
                <h2 className="text-lg font-bold">{tableTitle}</h2>
                <div className="relative w-full sm:w-auto sm:min-w-[250px]">
                    <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-muted-foreground" />
                    <Input
                        type="search"
                        placeholder="Search courses..."
                        className="pl-9 h-8 text-xs"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </div>
            </div>

            <div className="overflow-hidden p-8">
                <div className="overflow-x-auto">
                    <div className="min-w-full inline-block align-middle">
                        <div className="overflow-x-auto max-h-[270px]">
                            <Table className={cn(
                                "rounded-md bg-card border space-y-4",
                                isSidebarOpen ? "max-w-[1220px]" : "max-w-[1400px]"
                            )}>
                                <TableHeader className="sticky top-0 bg-background z-10 border-b bg-card">
                                    <TableRow>
                                        <TableHead className="w-[120px] text-xs font-semibold py-2.5 px-3">Course Code</TableHead>
                                        <TableHead className="text-xs font-semibold py-2.5 px-3">Course Title</TableHead>
                                        <TableHead className="w-[80px] text-xs font-semibold py-2.5 px-3">Units</TableHead>
                                        <TableHead className="w-[80px] text-xs font-semibold py-2.5 px-3">Section</TableHead>
                                        <TableHead className="w-[80px] text-xs font-semibold py-2.5 px-3">Day</TableHead>
                                        <TableHead className="w-[140px] text-xs font-semibold py-2.5 px-3">Time</TableHead>
                                        <TableHead className="w-[80px] text-xs font-semibold py-2.5 px-3">Room</TableHead>
                                        <TableHead className="text-xs font-semibold py-2.5 px-3">Faculty</TableHead>
                                        <TableHead className="w-[100px] text-right text-xs font-semibold py-2.5 px-3">Action</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {filteredSections.length === 0 ? (
                                        <TableRow>
                                            <TableCell colSpan={9} className="text-center py-4 px-3 text-xs text-muted-foreground">
                                                {searchQuery ? "No sections match your search." : "No available sections for enrollment"}
                                            </TableCell>
                                        </TableRow>
                                    ) : (
                                        filteredSections.map((section, index) => (
                                            <TableRow key={`${section.class_section_id}_${index}`} className="hover:bg-muted/50 border-b">
                                                <TableCell className="py-2.5 px-3 text-xs font-medium">
                                                    {section.course_code || "N/A"}
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    {section.title}
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3">
                                                    <Badge variant="outline" className="text-xs">
                                                        {section.units} units
                                                    </Badge>
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    {section.section_code}
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    {getDayName(section.day_of_week)}
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    {section.start_time && section.end_time
                                                        ? `${formatTime(section.start_time)} - ${formatTime(section.end_time)}`
                                                        : "TBA"
                                                    }
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    {section.room_code || "TBA"}
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    {section.assigned_professor || "TBA"}
                                                </TableCell>
                                                <TableCell>
                                                    <EnrollmentTableButton
                                                        classSectionId={section.class_section_id}
                                                        tableRowId={enrollingId}
                                                        action={isForEnrollment ? handleEnroll : handleRemove}
                                                        isForEnrollment={isForEnrollment}
                                                    />
                                                </TableCell>
                                            </TableRow>
                                        ))
                                    )}
                                </TableBody>
                            </Table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}