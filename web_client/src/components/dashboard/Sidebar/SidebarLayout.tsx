/**
 * Date Written: 1/16/2026 at 8:00 PM
 */

import React from 'react';
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuItem,
    SidebarMenuButton,
    SidebarSeparator,
} from '@/components/ui/sidebar';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { LogOut, ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';
import { type SidebarProps } from '@/types/sidebar.types';
import { Submenu } from '@/components/ui/SidebarSubmenu';
import { useLocation } from 'react-router';

export function SidebarLayout({
    sections,
    universityName = "City of Malabon University",
    universityLogo,
    onLogout,
    collapsed = false,
    onCollapseChange,
}: SidebarProps) {
    const location = useLocation();
    const currentPath = location.pathname;

    // Function to check if a menu item is active
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const isMenuItemActive = (url: string, submenu?: Array<any>) => {
        if (url === currentPath) return true;

        // Check submenu items
        if (submenu) {
            return submenu.some(subItem => subItem.url === currentPath);
        }

        return false;
    };

    // Process sections to add dynamic isActive
    const processedSections = sections.map(section => ({
        ...section,
        items: section.items.map(item => ({
            ...item,
            isActive: isMenuItemActive(item.url, item.submenu),
            // Process submenu items too
            submenu: item.submenu?.map(subItem => ({
                ...subItem,
                isActive: subItem.url === currentPath
            }))
        }))
    }));

    const [isCollapsed, setIsCollapsed] = React.useState(collapsed);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [openSubmenus, setOpenSubmenus] = React.useState<Record<string, boolean>>({});

    const toggleCollapse = () => {
        const newCollapsed = !isCollapsed;
        setIsCollapsed(newCollapsed);
        onCollapseChange?.(newCollapsed);
    };

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const toggleSubmenu = (title: string) => {
        setOpenSubmenus(prev => ({
            ...prev,
            [title]: !prev[title]
        }));
    };

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const renderMenuItem = (item: any) => {
        // If item has submenu, render Submenu component
        if (item.submenu && item.submenu.length > 0) {
            return (
                <Submenu
                    key={item.title}
                    title={item.title}
                    icon={<item.icon className="h-4 w-4" />}
                    submenu={item.submenu}
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    isActive={item.isActive || item.submenu.some((sub: any) => sub.isActive)}
                    badge={item.badge}
                    isCollapsed={isCollapsed}
                />
            );
        }

        // Regular menu item
        return (
            <SidebarMenuItem key={item.title}>
                <SidebarMenuButton
                    asChild
                    isActive={item.isActive}
                    className={cn(
                        "transition-colors hover:bg-accent hover:text-accent-foreground",
                        item.isActive && "bg-primary/10 text-primary"
                    )}
                >
                    <a href={item.url} className="relative">
                        <item.icon className={cn(
                            "h-4 w-4",
                            isCollapsed ? "mx-auto" : "mr-3"
                        )} />
                        {!isCollapsed && <span>{item.title}</span>}

                        {/* Badge */}
                        {item.badge && !isCollapsed && (
                            <Badge
                                variant="secondary"
                                className="ml-auto h-5 min-w-5 px-1"
                            >
                                {item.badge}
                            </Badge>
                        )}

                        {/* Active Indicator */}
                        {item.isActive && !isCollapsed && (
                            <div className="absolute -left-4 top-1/2 h-6 w-1 -translate-y-1/2 rounded-r-full bg-primary" />
                        )}
                    </a>
                </SidebarMenuButton>
            </SidebarMenuItem>
        );
    };

    return (
        <Sidebar
            collapsible="icon"
            className={cn(
                "border-r border-border bg-card",
                "transition-all duration-300",
                isCollapsed ? "w-24" : "w-64"
            )}
        >
            {/* Collapse Toggle Button */}
            <div className="absolute -right-3 top-6 z-50">
                <Button
                    variant="outline"
                    size="icon"
                    className="h-6 w-6 rounded-full border-2 border-background bg-background"
                    onClick={toggleCollapse}
                >
                    {isCollapsed ? (
                        <ChevronRight className="h-3 w-3" />
                    ) : (
                        <ChevronLeft className="h-3 w-3" />
                    )}
                </Button>
            </div>

            {/* Header with University Logo and Name */}
            <SidebarHeader className={cn(
                "border-b border-border",
                isCollapsed ? "p-2" : "p-4"  // Reduce padding when collapsed
            )}>
                <div className="flex items-center gap-3">
                    {/* University Logo */}
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
                        {universityLogo ? (
                            <img
                                src={universityLogo}
                                alt={universityName}
                                className="h-8 w-8 object-contain"
                            />
                        ) : (
                            <span className="text-lg font-bold text-primary-foreground">CMU</span>
                        )}
                    </div>

                    {/* University Name - Hidden when collapsed */}
                    {!isCollapsed && (
                        <div className="flex flex-col">
                            <h2 className="text-base font-bold tracking-tight text-foreground">
                                {universityName}
                            </h2>
                        </div>
                    )}
                </div>
            </SidebarHeader>

            {/* Menu Sections */}
            <SidebarContent className={cn(
                "flex-1",
                isCollapsed ? "p-0" : "p-4"
            )}>
                {processedSections.map((section, index) => (
                    <React.Fragment key={section.title}>
                        <SidebarGroup>
                            {/* Section Title - Hidden when collapsed */}
                            {!isCollapsed && section.title && (
                                <SidebarGroupLabel className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                                    {section.title}
                                </SidebarGroupLabel>
                            )}

                            <SidebarGroupContent>
                                <SidebarMenu>
                                    {section.items.map(renderMenuItem)}
                                </SidebarMenu>
                            </SidebarGroupContent>
                        </SidebarGroup>

                        {/* Separator between sections (except last) */}
                        {index < processedSections.length - 1 && !isCollapsed && (
                            <SidebarSeparator className="my-4" />
                        )}
                    </React.Fragment>
                ))}
            </SidebarContent>

            {/* Footer with Logout Button */}
            <SidebarFooter className="border-t border-border p-4">
                <Button
                    variant="ghost"
                    size={isCollapsed ? "icon" : "default"}
                    className={cn(
                        "w-full justify-start text-muted-foreground hover:bg-destructive/10 hover:text-destructive",
                        isCollapsed && "justify-center"
                    )}
                    onClick={onLogout}
                >
                    <LogOut className={cn("h-4 w-4", !isCollapsed && "mr-2")} />
                    {!isCollapsed && "Logout"}
                </Button>
            </SidebarFooter>
        </Sidebar>
    );
}