/**
 * Date Written: 1/19/2026 at 4:06 PM
 */

import { sidebarIcons } from '../../../components/dashboard/icon_constants';

// Student menu sections
export const studentSidebarSections = [
    {
        title: "STUDENT MENU",
        items: [
            {
                title: "Dashboard",
                url: "/student/dashboard",
                icon: sidebarIcons.Dashboard,
            },
            {
                title: "Academics",
                url: "#",
                icon: sidebarIcons.Academics,
                submenu: [
                    {
                        title: "Enrollment",
                        url: "/student/enrollment",
                        badge: "3",
                    }
                ],
            },
            // {
            //     title: "Assignments",
            //     url: "#",
            //     icon: sidebarIcons.Submissions,
            //     badge: "2",
            //     submenu: [
            //         {
            //             title: "Pending",
            //             url: "/student/assignments/pending",
            //             badge: "2",
            //         },
            //         {
            //             title: "Submitted",
            //             url: "/student/assignments/submitted",
            //         },
            //         {
            //             title: "Graded",
            //             url: "/student/assignments/graded",
            //         },
            //     ],
            // },
            // {
            //     title: "AI Tools",
            //     url: "#",
            //     icon: sidebarIcons['AI Analytics'],
            //     submenu: [
            //         {
            //             title: "AI Analytics",
            //             url: "/student/ai-analytics",
            //         },
            //         {
            //             title: "AI Assistant",
            //             url: "/student/ai-assistant",
            //         },
            //         {
            //             title: "Study Planner",
            //             url: "/student/study-planner",
            //         },
            //     ],
            // },
            // {
            //     title: "Records",
            //     url: "/student/records",
            //     icon: sidebarIcons.Records,
            // },
            // {
            //     title: "Settings",
            //     url: "/student/settings",
            //     icon: sidebarIcons.Settings,
            // },
            // {
            //     title: "Help Center",
            //     url: "/student/help",
            //     icon: sidebarIcons.Help,
            // },
        ],
    }
];
