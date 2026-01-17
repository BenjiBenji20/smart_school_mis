/**
 * Date Written: 1/17/2026 at 10:55 AM
 */

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import { Link } from 'react-router';

interface UserAvatarProps {
    firstName: string;
    lastName: string;
    email: string;
    role?: string;
    imageUrl?: string | null;
    className?: string;
    showStatus?: boolean;
    isActive?: boolean;
    showInfo?: boolean;
    size?: 'default' | 'lg';
    profileLink?: string;
}

// Array of consistent colors for fallback avatars
const fallbackColors = [
    'bg-blue-600',
    'bg-green-600',
    'bg-purple-600',
    'bg-amber-600',
    'bg-rose-600',
    'bg-indigo-600',
    'bg-teal-600',
    'bg-pink-600',
];

export function UserAvatar({
    firstName,
    lastName,
    email,
    role = 'User',
    imageUrl,
    className,
    showStatus = true,
    isActive = true,
    showInfo = false,
    size = 'default',
    profileLink = '/profile',
}: UserAvatarProps) {
    // Generate consistent color based on email
    const getColorFromEmail = (email: string): string => {
        const hash = email.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
        return fallbackColors[hash % fallbackColors.length];
    };

    // Generate initials from first and last name
    const getInitials = (): string => {
        const firstInitial = firstName?.charAt(0)?.toUpperCase() || '';
        const lastInitial = lastName?.charAt(0)?.toUpperCase() || '';
        return firstInitial + lastInitial || email?.charAt(0)?.toUpperCase() || 'U';
    };

    // Get user's full name
    const getFullName = (): string => {
        return `${firstName} ${lastName}`.trim();
    };

    // Format role for display
    const formatRole = (role: string): string => {
        return role.charAt(0).toUpperCase() + role.slice(1).toLowerCase();
    };

    // Size classes
    const sizeClasses = {
        default: {
            avatar: 'h-10 w-10',
            text: 'text-base',
            status: 'h-2.5 w-2.5',
            name: 'text-sm font-medium',
            role: 'text-xs',
            container: 'gap-3',
        },
        lg: {
            avatar: 'h-12 w-12',
            text: 'text-lg',
            status: 'h-3 w-3',
            name: 'text-base font-semibold',
            role: 'text-sm',
            container: 'gap-4',
        }
    };

    const currentSize = sizeClasses[size];

    // Avatar content (reusable)
    const avatarContent = (
        <>
            <div className="relative">
                <Avatar className={cn(currentSize.avatar, "shadow-sm", "transition-transform hover:scale-105")}>
                    <AvatarImage
                        src={imageUrl || undefined}
                        alt={getFullName()}
                        className="object-cover"
                    />
                    <AvatarFallback
                        className={cn(
                            "text-white font-semibold",
                            currentSize.text,
                            getColorFromEmail(email)
                        )}
                    >
                        {getInitials()}
                    </AvatarFallback>
                </Avatar>

                {/* Status indicator (green dot) */}
                {showStatus && (
                    <div
                        className={cn(
                            "absolute bottom-0 right-0 rounded-full border-2 border-background",
                            "transition-all duration-200",
                            currentSize.status,
                            isActive ? 'bg-green-500' : 'bg-gray-400'
                        )}
                    />
                )}
            </div>

            {/* User info (name and role) */}
            {showInfo && (
                <div className="flex flex-col">
                    <span className={cn("text-foreground", currentSize.name)}>
                        {getFullName()}
                    </span>
                    <span className={cn("text-muted-foreground", currentSize.role)}>
                        {formatRole(role)}
                    </span>
                </div>
            )}
        </>
    );

    // Clickable with Link (navigation)
    return (
        <Link
            to={profileLink}
            className={cn(
                "flex items-center",
                currentSize.container, "hover:opacity-90 transition-opacity",
                className
            )}
            aria-label={`Go to ${getFullName()}'s profile`}
        >
            {avatarContent}
        </Link>
    );
}
