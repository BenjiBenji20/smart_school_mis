/**
 * Date Written: 1/23/2026 at 4:45 PM
 */

import { Alert, AlertDescription } from "@/components/ui/alert";
import { Input } from "@/components/ui/input";
import { TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, Search, Table } from "lucide-react";
import type { EnrollmentResponse } from "@/types/enrollments_and_gradings.types";
import { useMemo, useState } from "react";
import { Checkbox } from "@radix-ui/react-checkbox";
import { Button } from "@/components/ui/button";
import { EnrollmentStatus } from "@/types/enrollments_and_gradings.enums.types";
import { enrollmentApi } from "@/api/v1/enrollments_and_gradings_api";

interface EnrollmentApprovalTableProps {
    enrollmentData: EnrollmentResponse[];
    onEnrollmentSuccess?: () => void;
    isSidebarOpen?: boolean;
    tableTitle?: string;
}

export function EnrollmentApprovalTable({
    enrollmentData,
    onEnrollmentSuccess,
    isSidebarOpen,
    tableTitle,
}: EnrollmentApprovalTableProps) {
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [selectedEnrollments, setSelectedEnrollments] = useState<Set<string>>(new Set());
    const [isUpdating, setIsUpdating] = useState(false);

    // formatters
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

    // Filter sections based on search query
    const filteredEnrollment = useMemo(() => {
        if (!searchQuery.trim()) return enrollmentData;

        const query = searchQuery.toLowerCase();
        return enrollmentData.filter(enrollment =>
            enrollment.enrollment_status.toLowerCase().includes(query) ||
            enrollment.section_code.toLowerCase().includes(query) ||
            enrollment.course_code.toLowerCase().includes(query) ||
            enrollment.title.toLowerCase().includes(query) ||
            enrollment.semester_period.toLowerCase().includes(query)
        );
    }, [enrollmentData, searchQuery]);

    // Toggle individual checkbox
    const handleToggleEnrollment = (enrollmentId: string) => {
        setSelectedEnrollments(prev => {
            const newSet = new Set(prev);
            if (newSet.has(enrollmentId)) {
                newSet.delete(enrollmentId);
            } else {
                newSet.add(enrollmentId);
            }
            return newSet;
        });
    };

    // Toggle all checkboxes
    const handleToggleAll = () => {
        if (selectedEnrollments.size === filteredEnrollment.length) {
            setSelectedEnrollments(new Set());
        } else {
            setSelectedEnrollments(new Set(filteredEnrollment.map(e => e.enrollment_id)));
        }
    };

    // Update enrollment status
    const handleUpdateStatus = async (status: EnrollmentStatus) => {
        if (selectedEnrollments.size === 0) {
            setError("Please select at least one enrollment to update.");
            return;
        }

        setIsUpdating(true);
        setError(null);
        setSuccess(null);

        try {
            await enrollmentApi.updateEnrollmentStatus({
                status,
                enrollment_ids: Array.from(selectedEnrollments)
            });

            setSuccess(`Successfully ${status.toLowerCase()} ${selectedEnrollments.size} enrollment(s).`);
            setSelectedEnrollments(new Set()); // Clear selection

            if (onEnrollmentSuccess) {
                onEnrollmentSuccess();
            }
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (err: any) {
            setError(err.response?.data?.message || `Failed to update enrollment status. Please try again.`);
        } finally {
            setIsUpdating(false);
        }
    };

    const allSelected = filteredEnrollment.length > 0 && selectedEnrollments.size === filteredEnrollment.length;
    const someSelected = selectedEnrollments.size > 0 && selectedEnrollments.size < filteredEnrollment.length;

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
                        placeholder="Search enrollments..."
                        className="pl-9 h-8 text-xs"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </div>
            </div>

            <div className="overflow-hidden px-8">
                <div className="overflow-x-auto">
                    <div className="min-w-full inline-block align-middle">
                        <div className="overflow-x-auto max-h-[270px]">
                            <Table className={cn(
                                "rounded-md bg-card border space-y-4",
                                isSidebarOpen ? "max-w-[1220px]" : "max-w-[1400px]"
                            )}>
                                <TableHeader className="sticky top-0 bg-background z-10 border-b bg-card">
                                    <TableRow>
                                        <TableHead className="w-[50px] text-xs font-semibold py-2.5 px-3">
                                            <Checkbox
                                                checked={allSelected}
                                                onCheckedChange={handleToggleAll}
                                                aria-label="Select all"
                                                className={someSelected ? "data-[state=checked]:bg-primary" : ""}
                                            />
                                        </TableHead>
                                        <TableHead className="w-[120px] text-xs font-semibold py-2.5 px-3">Student Name</TableHead>
                                        <TableHead className="w-[120px] text-xs font-semibold py-2.5 px-3">Course Code</TableHead>
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
                                    {filteredEnrollment.length === 0 ? (
                                        <TableRow>
                                            <TableCell colSpan={8} className="text-center py-4 px-3 text-xs text-muted-foreground">
                                                {searchQuery ? "No enrollments match your search." : "No pending enrollments"}
                                            </TableCell>
                                        </TableRow>
                                    ) : (
                                        filteredEnrollment.map((enrollment, index) => (
                                            <TableRow key={`${enrollment.enrollment_id}_${index}`} className="hover:bg-muted/50 border-b">
                                                <TableCell className="py-2.5 px-3 text-xs font-medium">
                                                    {enrollment.student_name}
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    {enrollment.course_code || "N/A"}
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3">
                                                    <Badge variant="outline" className="text-xs">
                                                        {enrollment.units} units
                                                    </Badge>
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    {getDayName(enrollment.day_of_week)}
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    {enrollment.start_time && enrollment.end_time
                                                        ? `${formatTime(enrollment.start_time)} - ${formatTime(enrollment.end_time)}`
                                                        : "TBA"
                                                    }
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    {enrollment.room_code || "TBA"}
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    {enrollment.assigned_professor || "TBA"}
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3">
                                                    <Checkbox
                                                        checked={selectedEnrollments.has(enrollment.enrollment_id)}
                                                        onCheckedChange={() => handleToggleEnrollment(enrollment.enrollment_id)}
                                                        aria-label={`Select ${enrollment.student_name}`}
                                                    />
                                                </TableCell>
                                                <TableCell className="py-2.5 px-3 text-xs">
                                                    <Badge
                                                        variant="outline"
                                                        className={cn(
                                                            "text-xs",
                                                            enrollment.enrollment_status === "APPROVED" && "bg-green-50 text-green-700 border-green-200",
                                                            enrollment.enrollment_status === "PENDING" && "bg-yellow-50 text-yellow-700 border-yellow-200",
                                                            enrollment.enrollment_status === "REJECTED" && "bg-red-50 text-red-700 border-red-200"
                                                        )}
                                                    >
                                                        {enrollment.enrollment_status}
                                                    </Badge>
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

            {/* Action Buttons */}
            <div className="flex items-center justify-between px-8 py-4 border-t">
                <div className="text-xs text-muted-foreground">
                    {selectedEnrollments.size > 0
                        ? `${selectedEnrollments.size} enrollment(s) selected`
                        : "No enrollments selected"
                    }
                </div>
                <div className="flex gap-2">
                    <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleUpdateStatus(EnrollmentStatus.APPROVED)}
                        disabled={selectedEnrollments.size === 0 || isUpdating}
                        className="text-xs h-8"
                    >
                        {isUpdating ? "Updating..." : "Approve"}
                    </Button>
                    <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleUpdateStatus(EnrollmentStatus.PENDING)}
                        disabled={selectedEnrollments.size === 0 || isUpdating}
                        className="text-xs h-8"
                    >
                        {isUpdating ? "Updating..." : "Set to Pending"}
                    </Button>
                    <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => handleUpdateStatus(EnrollmentStatus.REJECTED)}
                        disabled={selectedEnrollments.size === 0 || isUpdating}
                        className="text-xs h-8"
                    >
                        {isUpdating ? "Updating..." : "Reject"}
                    </Button>
                </div>
            </div>
        </div>
    );
}