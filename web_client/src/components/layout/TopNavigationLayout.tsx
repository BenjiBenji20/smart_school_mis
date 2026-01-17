/**
 * Date Written: 1/17/2026 at 10:30 AM
 */

import { useState } from 'react';
import { UserAvatar } from '@/components/ui/UserAvatar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search, Menu, Bell } from 'lucide-react';
import { cn } from '@/lib/utils';
import { type BaseUserResponse } from '@/types/authentication.types';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface TopNavigationProps {
    user: BaseUserResponse;
    onLogout?: () => void;
    onToggleSidebar?: () => void;
    className?: string;
    pageTitle?: string;
    isSidebarOpen?: boolean
}

export function TopNavigation({
    user,
    onLogout,
    onToggleSidebar,
    className,
    pageTitle = "Dashboard / Overview",
    isSidebarOpen = false
}: TopNavigationProps) {
    const [searchQuery, setSearchQuery] = useState('');

    const getFullName = (): string => {
        const { first_name, last_name } = user;
        return `${first_name} ${last_name}`.trim();
    };

    const formatRole = (role: string | null): string => {
        if (!role) return 'User';
        return role;
    };

    return (
        <header className={cn(
            "sticky top-0 z-40 w-full border-b border-border bg-background/80 backdrop-blur-md supports-[backdrop-filter]:bg-background/60",
            className
        )}>
            <div className="flex h-16 items-center gap-4 px-4 md:px-2">
                {/* LEFT: Menu Button + Page Title - 30% width */}
                <div className={cn(
                    "flex items-center gap-3 min-w-0",
                    isSidebarOpen ? "w-[50%]" : "w-[30%]"
                )}>
                    {onToggleSidebar && (
                        <Button
                            variant="ghost"
                            size="icon"
                            className="lg:hidden shrink-0"
                            onClick={onToggleSidebar}
                        >
                            <Menu className="h-5 w-5" />
                            <span className="sr-only">Toggle sidebar</span>
                        </Button>
                    )}
                    <h1 className="hidden lg:block text-l text-foreground truncate">
                        {pageTitle}
                    </h1>
                </div>

                {/* RIGHT: Search + Notifications + Avatar - 70% width */}
                <div className={cn(
                    "flex items-center gap-3 justify-end",
                    isSidebarOpen ? "w-[30%]" : "w-[62%]"
                )}>
                    {/* Search Bar */}
                    <div className="flex-1 max-w-sm">
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                            <Input
                                type="search"
                                placeholder="Search..."
                                className="w-full pl-10 pr-4 bg-muted/50"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </div>
                    </div>

                    {/* Notifications */}
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon" className="shrink-0">
                                <Bell className="h-5 w-5" />
                                <span className="sr-only">Notifications</span>
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" className="w-80">
                            <DropdownMenuLabel>Notifications</DropdownMenuLabel>
                            <DropdownMenuSeparator />
                            <div className="max-h-80 overflow-auto p-1">
                                <div className="space-y-2">
                                    <div className="rounded-lg p-3 hover:bg-accent cursor-pointer">
                                        <div className="space-y-1">
                                            <p className="text-sm font-medium">Camera Required</p>
                                            <p className="text-xs text-muted-foreground">
                                                CS 101 - 10:00 AM (2 hours)
                                            </p>
                                        </div>
                                    </div>
                                    <div className="rounded-lg p-3 hover:bg-accent cursor-pointer">
                                        <div className="space-y-1">
                                            <p className="text-sm font-medium">MATH 55 - Linear Algebra</p>
                                            <p className="text-xs text-muted-foreground">
                                                Dec 18, 2025 • 1:00 PM (1.5 hours)
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem className="cursor-pointer justify-center text-sm">
                                View all notifications
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>

                    {/* Desktop: Avatar with Info */}
                    <div className="hidden md:block shrink-0">
                        <UserAvatar
                            firstName={user.first_name}
                            lastName={user.last_name}
                            email={user.email}
                            role={formatRole(user.role)}
                            imageUrl={null}
                            showStatus={true}
                            isActive={user.is_active}
                            showInfo={true}
                            profileLink="/profile"
                        />
                    </div>

                    {/* Mobile: Avatar + Menu */}
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="md:hidden p-1 h-auto shrink-0">
                                <UserAvatar
                                    firstName={user.first_name}
                                    lastName={user.last_name}
                                    email={user.email}
                                    role={formatRole(user.role)}
                                    imageUrl={null}
                                    showStatus={true}
                                    isActive={user.is_active}
                                    showInfo={false}
                                    profileLink="/profile"
                                />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" className="w-56">
                            <DropdownMenuLabel className="font-normal">
                                <div className="flex flex-col space-y-1">
                                    <p className="text-sm font-medium leading-none">
                                        {getFullName()}
                                    </p>
                                    <p className="text-xs leading-none text-muted-foreground">
                                        {user.email}
                                    </p>
                                    <div className="flex items-center gap-2 pt-1">
                                        <div className={cn(
                                            "h-2 w-2 rounded-full",
                                            user.is_active ? "bg-green-500" : "bg-gray-400"
                                        )} />
                                        <span className="text-xs text-muted-foreground">
                                            {formatRole(user.role)}
                                        </span>
                                    </div>
                                </div>
                            </DropdownMenuLabel>
                            <DropdownMenuSeparator />
                            <DropdownMenuGroup>
                                <DropdownMenuItem className="cursor-pointer">
                                    <span>Profile</span>
                                </DropdownMenuItem>
                                <DropdownMenuItem className="cursor-pointer">
                                    <span>Settings</span>
                                </DropdownMenuItem>
                            </DropdownMenuGroup>
                            <DropdownMenuSeparator />
                            {onLogout && (
                                <DropdownMenuItem
                                    className="cursor-pointer text-destructive"
                                    onClick={onLogout}
                                >
                                    <span>Log out</span>
                                </DropdownMenuItem>
                            )}
                        </DropdownMenuContent>
                    </DropdownMenu>
                </div>
            </div>

            {/* Mobile Page Title */}
            <div className="lg:hidden border-t border-border px-4 py-3">
                <h1 className="text-lg font-semibold text-foreground">
                    {pageTitle}
                </h1>
            </div>
        </header>
    );
}