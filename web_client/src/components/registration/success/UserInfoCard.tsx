/**
 * Date Written: 1/16/2026 at 10:18 PM
 */

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { User, Mail, Phone, MapPin, Calendar, IdCard } from "lucide-react";
import { type BaseUserResponse } from "@/types/authentication.types";

interface UserInfoCardProps {
    user: BaseUserResponse;
}

export function UserInfoCard({ user }: UserInfoCardProps) {
    const fullName = `${user.first_name} ${user.middle_name ? user.middle_name + " " : ""}${user.last_name}${user.suffix ? " " + user.suffix : ""}`;

    return (
        <Card className="w-full max-w-2xl mx-auto shadow-lg">
            <CardHeader>
                <CardTitle className="text-2xl text-navy-900">Registered Information</CardTitle>
                <CardDescription>Please review your details. Your account is pending approval.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <User className="h-5 w-5 text-gray-600" />
                        <div>
                            <p className="text-sm text-gray-600">Full Name</p>
                            <p className="font-medium">{fullName}</p>
                        </div>
                    </div>
                    {user.role && (
                        <Badge variant="secondary" className="bg-teal-100 text-teal-800">
                            {user.role}
                        </Badge>
                    )}
                </div>

                <Separator />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="flex items-center gap-3">
                        <Mail className="h-5 w-5 text-gray-600" />
                        <div>
                            <p className="text-sm text-gray-600">Email</p>
                            <p className="font-medium">{user.email}</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3">
                        <Phone className="h-5 w-5 text-gray-600" />
                        <div>
                            <p className="text-sm text-gray-600">Cellphone</p>
                            <p className="font-medium">{user.cellphone_number}</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3">
                        <MapPin className="h-5 w-5 text-gray-600" />
                        <div>
                            <p className="text-sm text-gray-600">Address</p>
                            <p className="font-medium">{user.complete_address}</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3">
                        <Calendar className="h-5 w-5 text-gray-600" />
                        <div>
                            <p className="text-sm text-gray-600">Age & Gender</p>
                            <p className="font-medium">{user.age} years • {user.gender}</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3">
                        <IdCard className="h-5 w-5 text-gray-600" />
                        <div>
                            <p className="text-sm text-gray-600">Registration Date</p>
                            <p className="font-medium">{new Date(user.created_at).toLocaleDateString()}</p>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}