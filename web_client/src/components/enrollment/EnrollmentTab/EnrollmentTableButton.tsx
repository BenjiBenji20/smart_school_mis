/**
 * Date: 1/21/2026 at 4:53 PM 
 */

import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface EnrollmentTableButtonProps {
    classSectionId: string;
    tableRowId: string | null;
    isForEnrollment?: boolean;
    action: (classSectionId: string) => Promise<void>;
    className?: string;
    disabled?: boolean;
}

export function EnrollmentTableButton({
    classSectionId,
    tableRowId,
    isForEnrollment = true,
    action,
    className,
    disabled = false
}: EnrollmentTableButtonProps) {
    const isEnrolling = tableRowId === classSectionId;
    
    return (
        <Button
            size="sm"
            onClick={() => action(classSectionId)}
            disabled={isEnrolling || disabled}
            className={cn("h-7 px-3 text-xs", className)}
        >
            {isEnrolling ? (
                <>
                    <Loader2 className="mr-1 h-3 w-3 animate-spin" />
                    {isForEnrollment ? "Enrolling" : "Removing"}
                </>
            ) : (
                isForEnrollment ? "Enroll" : "Remove"
            )}
        </Button>
    );
}