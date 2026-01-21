/**
 * Date Written: 1/19/2026 at 12:01 PM
 */

import type { TermResponse } from "@/types/academic_structure.types";
import { CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Calendar, CalendarDays, School } from "lucide-react";
import { format } from "date-fns";
import { cn } from "@/lib/utils";

interface EnrollmentHeaderProps {
    term: TermResponse;
    title?: string;
    isSidebarOpen?: boolean
}

export function EnrollmentHeader({ term, title = "Student Enrollment", isSidebarOpen = false }: EnrollmentHeaderProps) {
    const formatDate = (dateString: string) => {
        try {
            return format(new Date(dateString), "MMM dd, yyyy");
        } catch {
            return dateString;
        }
    };

    const getStatusColor = (status: string) => {
        switch (status.toLowerCase()) {
            case "active":
                return "bg-green-500";
            case "upcoming":
                return "bg-blue-500";
            case "completed":
                return "bg-gray-500";
            default:
                return "bg-gray-500";
        }
    };

    const formatSemesterPeriod = (period: string) => {
        const periodMap: Record<string, string> = {
            "FIRST": "First Semester",
            "SECOND": "Second Semester",
            "SUMMER": "Summer Term"
        };
        return periodMap[period] || period;
    };

    return (
        // 1210px when sidebar open

        <div className={cn("mb-8 border-none shadow-sm",
            isSidebarOpen ? "max-w-[1220px]" : "max-w-[1400px]")
        }>
            <CardContent className="px-2">
                <div className="space-y-4">
                    {/* Title and Status */}
                    <div className="flex items-start justify-between">
                        <h1 className="text-lg font-bold">{title}
                            <Badge className={`text-xs ${getStatusColor(term.status)} ml-4`}>
                                {term.status}
                            </Badge>
                        </h1>
                    </div>

                    {/* Vertical Info Items */}
                    <div className="space-y-2.5">
                        <div className="flex items-center space-x-2">
                            <School className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
                            <div className="text-sm">
                                <span className="text-muted-foreground">Academic Year: </span>
                                <span className="font-medium">{term.academic_year_start} - {term.academic_year_end}</span>
                            </div>
                        </div>

                        <div className="flex items-center space-x-2">
                            <CalendarDays className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
                            <div className="text-sm">
                                <span className="text-muted-foreground">Semester Period: </span>
                                <span className="font-medium">{formatSemesterPeriod(term.semester_period)}</span>
                            </div>
                        </div>

                        <div className="flex items-center space-x-2">
                            <Calendar className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
                            <div className="text-sm">
                                <span className="text-muted-foreground">Enrollment Date: </span>
                                <span className="font-medium">
                                    {formatDate(term.enrollment_start)} to {formatDate(term.enrollment_end)}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </CardContent>
        </div>
    );
}