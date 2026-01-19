import type { AllowedEnrollSectionResponse } from "@/types/enrollments_and_gradings.types";

export const dummyAllowedSections: AllowedEnrollSectionResponse[] = [
    {
        class_section_id: "cs101-001",
        course_code: "CS 101",
        title: "Introduction to Computer Science",
        units: 3,
        section_code: "CS101-001",
        day_of_week: 1, // Monday
        start_time: "08:30:00",
        end_time: "10:00:00",
        room_code: "L-301",
        assigned_professor: "Dr. Sarah Johnson"
    },
    {
        class_section_id: "cs102-001",
        course_code: "CS 102",
        title: "Data Structures & Algorithms",
        units: 4,
        section_code: "CS102-001",
        day_of_week: 2, // Tuesday
        start_time: "10:00:00",
        end_time: "12:00:00",
        room_code: "L-302",
        assigned_professor: "Prof. Michael Chen"
    },
    {
        class_section_id: "cs102-002",
        course_code: "CS 102",
        title: "Data Structures & Algorithms",
        units: 4,
        section_code: "CS102-002",
        day_of_week: 4, // Thursday
        start_time: "13:00:00",
        end_time: "15:00:00",
        room_code: "L-303",
        assigned_professor: "Prof. Michael Chen"
    },
    {
        class_section_id: "cs210-001",
        course_code: "CS 210",
        title: "Software Engineering",
        units: 3,
        section_code: "CS210-001",
        day_of_week: 3, // Wednesday
        start_time: "09:00:00",
        end_time: "10:30:00",
        room_code: "A-102",
        assigned_professor: "Dr. Emily Rodriguez"
    },
    {
        class_section_id: "cs210-002",
        course_code: "CS 210",
        title: "Software Engineering",
        units: 3,
        section_code: "CS210-002",
        day_of_week: 5, // Friday
        start_time: "14:00:00",
        end_time: "15:30:00",
        room_code: "A-103",
        assigned_professor: "Dr. Emily Rodriguez"
    },
    {
        class_section_id: "cs305-001",
        course_code: "CS 305",
        title: "Advanced Database Systems",
        units: 3,
        section_code: "CS305-001",
        day_of_week: 2, // Tuesday
        start_time: "13:00:00",
        end_time: "14:30:00",
        room_code: "L-305",
        assigned_professor: "Prof. Robert Kim"
    },
    {
        class_section_id: "cs305-002",
        course_code: "CS 305",
        title: "Advanced Database Systems",
        units: 3,
        section_code: "CS305-002",
        day_of_week: 4, // Thursday
        start_time: "10:30:00",
        end_time: "12:00:00",
        room_code: "L-306",
        assigned_professor: "Prof. Robert Kim"
    },
    {
        class_section_id: "math101-001",
        course_code: "MATH 101",
        title: "Calculus I",
        units: 4,
        section_code: "MATH101-001",
        day_of_week: 1, // Monday
        start_time: "10:30:00",
        end_time: "12:00:00",
        room_code: "M-201",
        assigned_professor: "Dr. James Wilson"
    },
    {
        class_section_id: "math101-002",
        course_code: "MATH 101",
        title: "Calculus I",
        units: 4,
        section_code: "MATH101-002",
        day_of_week: 3, // Wednesday
        start_time: "13:00:00",
        end_time: "14:30:00",
        room_code: "M-202",
        assigned_professor: "Dr. James Wilson"
    },
    {
        class_section_id: "eng101-001",
        course_code: "ENG 101",
        title: "Technical Writing",
        units: 3,
        section_code: "ENG101-001",
        day_of_week: 5, // Friday
        start_time: "08:00:00",
        end_time: "09:30:00",
        room_code: "H-101",
        assigned_professor: "Prof. Lisa Thompson"
    },
    {
        class_section_id: "phy201-001",
        course_code: "PHY 201",
        title: "Physics for Engineers",
        units: 4,
        section_code: "PHY201-001",
        day_of_week: 2, // Tuesday
        start_time: "15:00:00",
        end_time: "17:00:00",
        room_code: "S-301",
        assigned_professor: "Dr. Andrew Park"
    },
    {
        class_section_id: "phy201-002",
        course_code: "PHY 201",
        title: "Physics for Engineers",
        units: 4,
        section_code: "PHY201-002",
        day_of_week: 4, // Thursday
        start_time: "08:00:00",
        end_time: "10:00:00",
        room_code: "S-302",
        assigned_professor: "Dr. Andrew Park"
    },
    {
        class_section_id: "ethics101-001",
        course_code: "ETHICS 101",
        title: "Professional Ethics",
        units: 2,
        section_code: "ETHICS101-001",
        day_of_week: 1, // Monday
        start_time: "14:00:00",
        end_time: "15:30:00",
        room_code: "H-201",
        assigned_professor: "Prof. Maria Santos"
    },
    {
        class_section_id: "elective-cs-001",
        course_code: "CS 399",
        title: "Special Topics in AI",
        units: 3,
        section_code: "CS399-001",
        day_of_week: 3, // Wednesday
        start_time: "15:00:00",
        end_time: "16:30:00",
        room_code: "L-401",
        assigned_professor: "Dr. Alan Turing (Guest)"
    }
];

// Dummy term data for testing
export const dummyCurrentTerm = {
    id: "term-2024-2",
    created_at: "2024-01-15T00:00:00Z",
    academic_year_start: 2024,
    academic_year_end: 2025,
    enrollment_start: "2024-05-01T00:00:00Z",
    enrollment_end: "2024-05-30T23:59:59Z",
    semester_period: "SECOND_SEMESTER",
    status: "ACTIVE"
};

// Mock API functions for testing
export const mockEnrollmentApi = {
    async getAllowedSections(): Promise<AllowedEnrollSectionResponse[]> {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        return dummyAllowedSections;
    },

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async enrollStudentClassSection(studentId: string, classSectionId: string): Promise<any> {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1500));

        const section = dummyAllowedSections.find(s => s.class_section_id === classSectionId);

        if (!section) {
            throw new Error("Section not found");
        }

        // Simulate random success/failure for testing
        const isSuccess = Math.random() > 0.2; // 80% success rate

        if (isSuccess) {
            return {
                message: `Successfully enrolled in ${section.course_code} - ${section.title}`,
                status_code: 200,
                data: {
                    enrollment_id: `enroll-${Date.now()}`,
                    student_id: studentId,
                    class_section_id: classSectionId,
                    enrolled_at: new Date().toISOString()
                }
            };
        } else {
            // Simulate various error scenarios
            const errors = [
                "Schedule conflict with existing enrollment",
                "Section is already full",
                "Prerequisite not satisfied",
                "Maximum units exceeded",
                "Enrollment period has ended"
            ];
            const randomError = errors[Math.floor(Math.random() * errors.length)];

            throw {
                response: {
                    data: {
                        message: randomError,
                        status_code: 400
                    }
                }
            };
        }
    }
};