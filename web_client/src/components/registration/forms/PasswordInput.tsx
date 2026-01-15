/**
 * Date Written: 1/15/2026 at 1:35 PM
 */
import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Eye, EyeOff } from 'lucide-react';
import { FormFieldWrapper } from './FormFieldWrapper';

interface PasswordInputProps {
    label: string;
    value: string;
    onChange: (value: string) => void;
    required?: boolean;
    error?: string;
    placeholder?: string;
}

export function PasswordInput({
    label,
    value,
    onChange,
    required,
    error,
    placeholder = "••••••••",
}: PasswordInputProps) {
    const [showPassword, setShowPassword] = useState(false);
    
    return (
        <FormFieldWrapper label={label} required={required} error={error}>
            <div className="relative w-full">
                <Input
                    type={showPassword ? "text" : "password"}
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    placeholder={placeholder}
                    className="pr-10 w-full"
                />
                <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    className="absolute right-0 top-0 h-full px-3 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                    tabIndex={-1}
                >
                    {showPassword ? (
                        <EyeOff className="h-4 w-4 text-muted-foreground" />
                    ) : (
                        <Eye className="h-4 w-4 text-muted-foreground" />
                    )}
                </Button>
            </div>
        </FormFieldWrapper>
    );
}