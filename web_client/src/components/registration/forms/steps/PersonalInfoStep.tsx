/**
 * Date Written: 1/15/2026 at 1:38 PM
 */

import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { FormFieldWrapper } from '../FormFieldWrapper';
import { UserGender } from '@/types/user_state.enums.types';

interface PersonalInfoStepProps {
    data: {
        first_name: string;
        middle_name?: string | null;
        last_name: string;
        suffix?: string | null;
        age?: number;
        gender: UserGender;
        complete_address?: string;
    };
    onChange: (field: keyof PersonalInfoStepProps['data'], value: unknown) => void;
    errors?: Record<string, string>;
}

export function PersonalInfoStep({
    data,
    onChange,
    errors = {},
}: PersonalInfoStepProps) {
    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormFieldWrapper label="First Name" required error={errors.first_name}>
                    <Input
                        value={data.first_name}
                        onChange={(e) => onChange('first_name', e.target.value)}
                        placeholder="Juan"
                    />
                </FormFieldWrapper>

                <FormFieldWrapper label="Middle Name" error={errors.middle_name}>
                    <Input
                        value={data.middle_name || ''}
                        onChange={(e) => onChange('middle_name', e.target.value || null)}
                        placeholder="Santos"
                    />
                </FormFieldWrapper>

                <FormFieldWrapper label="Last Name" required error={errors.last_name}>
                    <Input
                        value={data.last_name}
                        onChange={(e) => onChange('last_name', e.target.value)}
                        placeholder="Dela Cruz"
                    />
                </FormFieldWrapper>

                <FormFieldWrapper label="Suffix" error={errors.suffix}>
                    <Input
                        value={data.suffix || ''}
                        onChange={(e) => onChange('suffix', e.target.value || null)}
                        placeholder="Jr., III, etc."
                    />
                </FormFieldWrapper>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormFieldWrapper label="Age" error={errors.age}>
                    <Input
                        type="number"
                        value={data.age || ''}
                        onChange={(e) => onChange('age', e.target.value ? parseInt(e.target.value) : undefined)}
                        placeholder="18"
                        min="16"
                        max="100"
                    />
                </FormFieldWrapper>

                <FormFieldWrapper label="Gender" required error={errors.gender}>
                    <RadioGroup
                        value={data.gender}
                        onValueChange={(value) => onChange('gender', value as UserGender)}
                        className="flex space-x-4"
                    >
                        <div className="flex items-center space-x-2">
                            <RadioGroupItem value={UserGender.MALE} id="male" />
                            <Label htmlFor="male">Male</Label>
                        </div>
                        <div className="flex items-center space-x-2">
                            <RadioGroupItem value={UserGender.FEMALE} id="female" />
                            <Label htmlFor="female">Female</Label>
                        </div>
                    </RadioGroup>
                </FormFieldWrapper>
            </div>

            <FormFieldWrapper label="Complete Address" error={errors.complete_address}>
                <Input
                    value={data.complete_address || ''}
                    onChange={(e) => onChange('complete_address', e.target.value)}
                    placeholder="Street, Barangay, City, Province"
                />
            </FormFieldWrapper>
        </div>
    );
}