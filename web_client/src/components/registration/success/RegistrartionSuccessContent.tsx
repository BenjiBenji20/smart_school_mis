/**
 * Date Written: 1/16/2026 at 10:18 PM
 */

import { CheckCircle2, Clock, User, Mail, Phone, MapPin, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { type BaseUserResponse } from "@/types/authentication.types";
import { Link } from "react-router";
import cmuLogo from '@/assets/cmu-logo.png';

interface RegistrationSuccessContentProps {
    user: BaseUserResponse;
}

export function RegistrationSuccessContent({ user }: RegistrationSuccessContentProps) {
    const fullName = `${user.first_name} ${user.middle_name ? user.middle_name + " " : ""}${user.last_name}${user.suffix ? " " + user.suffix : ""}`;

    const formatDate = (dateString: string | Date) => {
        const date = typeof dateString === 'string' ? new Date(dateString) : dateString;
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="min-h-screen bg-background flex items-center justify-center p-6 md:p-10">
            <div className="w-full max-w-3xl">
                <Card>
                    <CardHeader className="pb-6">
                        <div className="flex items-start justify-between">
                            <div className="flex items-center gap-4">
                                <img
                                    src={cmuLogo}
                                    alt="City of Malabon University Logo"
                                    className="h-16 object-contain"
                                />
                                <div>
                                    <CardTitle className="text-2xl font-bold">Registration Successful</CardTitle>
                                    <CardDescription className="text-base mt-1">
                                        Your account is pending approval
                                    </CardDescription>
                                </div>
                            </div>
                            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
                                <CheckCircle2 className="h-7 w-7 text-green-600" />
                            </div>
                        </div>
                    </CardHeader>

                    <CardContent className="space-y-6">
                        {/* Pending Status Alert */}
                        <Alert className="border-amber-200 bg-amber-50">
                            <Clock className="h-4 w-4 text-amber-600" />
                            <AlertDescription className="text-amber-800">
                                Your account is now pending admin approval. You will receive an email notification once your account is activated.
                            </AlertDescription>
                        </Alert>

                        {/* Account Details Section */}
                        <div className="space-y-4">
                            <div className="grid grid-cols-1 gap-3">
                                {/* Full Name with Role Badge */}
                                <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                                    <User className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                                    <p className="text-sm font-medium flex-1">{fullName}</p>
                                    {user.role && (
                                        <Badge variant="secondary" className="bg-primary/10 text-primary flex-shrink-0">
                                            {user.role}
                                        </Badge>
                                    )}
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    {/* Email */}
                                    <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                                        <Mail className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                                        <p className="text-sm text-muted-foreground truncate">{user.email}</p>
                                    </div>

                                    {/* Phone */}
                                    <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                                        <Phone className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                                        <p className="text-sm text-muted-foreground">{user.cellphone_number}</p>
                                    </div>
                                </div>

                                {/* Address */}
                                <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                                    <MapPin className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                                    <p className="text-sm text-muted-foreground">{user.complete_address}</p>
                                </div>

                                {/* Age & Gender */}
                                <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                                    <Calendar className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                                    <p className="text-sm text-muted-foreground">{user.age} years old • {user.gender}</p>
                                </div>
                            </div>
                        </div>

                        {/* Registration Time */}
                        <div className="pt-4 border-t">
                            <p className="text-xs text-muted-foreground">
                                Registered on {formatDate(user.created_at)}
                            </p>
                        </div>

                        {/* What's Next Section */}
                        <div className="space-y-3">
                            <h3 className="font-semibold text-sm text-muted-foreground uppercase tracking-wide">
                                What's Next?
                            </h3>
                            <ul className="space-y-2 text-sm text-muted-foreground">
                                <li className="flex items-start gap-2">
                                    <span className="text-primary mt-0.5">•</span>
                                    <span>An administrator will review your registration request</span>
                                </li>
                                <li className="flex items-start gap-2">
                                    <span className="text-primary mt-0.5">•</span>
                                    <span>You will receive an email notification once approved</span>
                                </li>
                                <li className="flex items-start gap-2">
                                    <span className="text-primary mt-0.5">•</span>
                                    <span>After approval, you can login with your credentials</span>
                                </li>
                            </ul>
                        </div>

                        {/* Action Buttons */}
                        <div className="flex flex-col sm:flex-row gap-3 pt-4">
                            <Button asChild className="flex-1">
                                <Link to="/">Return to Home</Link>
                            </Button>
                            <Button asChild variant="outline" className="flex-1">
                                <Link to="/login">Go to Login</Link>
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}