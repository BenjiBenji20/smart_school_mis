/**
 * Date Written: 1/16/2026 at 8:00 PM
 */

import { type LucideIcon } from 'lucide-react';

export interface SidebarSubMenuItem {
    title: string;
    url: string;
    isActive?: boolean;
    badge?: string | number;
}

export interface SidebarMenuItem {
    title: string;
    url: string;
    icon: LucideIcon;
    badge?: string | number;
    isActive?: boolean;
    submenu?: SidebarSubMenuItem[];
}

export interface SidebarMenuSection {
    title: string;
    items: SidebarMenuItem[];
}

export interface SidebarUser {
    name: string;
    email: string;
    avatar?: string;
    role: string;
    id: string;
}

export interface SidebarProps {
    sections: SidebarMenuSection[];
    universityName?: string;
    universityLogo?: string;
    onLogout?: () => void;
    collapsed?: boolean;
    onCollapseChange?: (collapsed: boolean) => void;
}