/**
 * Date Written: 1/16/2026 at 8:49 PM
 */

import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import { type SidebarSubMenuItem } from '@/types/sidebar.types';

interface SubmenuProps {
    title: string;
    icon: React.ReactNode;
    submenu: SidebarSubMenuItem[];
    isActive?: boolean;
    badge?: string | number;
    isCollapsed: boolean;
}

export function Submenu({
    title,
    icon,
    submenu,
    isActive = false,
    badge,
    isCollapsed,
}: SubmenuProps) {
    const [isOpen, setIsOpen] = useState(isActive);

    if (isCollapsed) {
        return (
            <div className="relative">
                <button
                    className={cn(
                        "flex h-9 w-9 items-center justify-center rounded-md transition-colors",
                        "hover:bg-accent hover:text-accent-foreground",
                        isActive && "bg-primary/10 text-primary"
                    )}
                    title={title}
                >
                    {icon}
                </button>
                {isActive && (
                    <div className="absolute -left-4 top-1/2 h-6 w-1 -translate-y-1/2 rounded-r-full bg-primary" />
                )}
            </div>
        );
    }

    return (
        <div className="space-y-1">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={cn(
                    "flex w-full items-center justify-between rounded-md px-3 py-2 text-sm",
                    "transition-colors hover:bg-accent hover:text-accent-foreground",
                    isActive && "bg-primary/10 text-primary"
                )}
            >
                <div className="flex items-center gap-3">
                    {icon}
                    <span>{title}</span>
                </div>
                <div className="flex items-center gap-2">
                    {badge && (
                        <span className="flex h-5 min-w-5 items-center justify-center rounded-full bg-muted px-1 text-xs">
                            {badge}
                        </span>
                    )}
                    <ChevronDown
                        className={cn(
                            "h-4 w-4 transition-transform",
                            isOpen && "rotate-180"
                        )}
                    />
                </div>
            </button>

            {isOpen && (
                <div className="ml-6 space-y-1 border-l border-border pl-3">
                    {submenu.map((item) => (
                        <a
                            key={item.title}
                            href={item.url}
                            className={cn(
                                "flex items-center justify-between rounded-md px-3 py-1.5 text-sm",
                                "transition-colors hover:bg-accent hover:text-accent-foreground",
                                item.isActive && "bg-primary/10 text-primary font-medium"
                            )}
                        >
                            <span>{item.title}</span>
                            {item.badge && (
                                <span className="flex h-5 min-w-5 items-center justify-center rounded-full bg-muted px-1 text-xs">
                                    {item.badge}
                                </span>
                            )}
                        </a>
                    ))}
                </div>
            )}
        </div>
    );
}