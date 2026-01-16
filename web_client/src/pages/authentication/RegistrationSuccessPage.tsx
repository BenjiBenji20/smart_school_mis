/**
 * Date Written: 1/16/2026 at 10:18 PM
 */
import { useLocation, useNavigate } from "react-router";
import { RegistrationSuccessContent } from "@/components/registration/success/RegistrartionSuccessContent";
import { type BaseUserResponse } from "@/types/authentication.types";
import { useEffect } from "react";

export function RegistrationSuccessPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const user = location.state?.user as BaseUserResponse | undefined;

    // Redirect if no user data
    useEffect(() => {
        if (!user) {
            navigate('/register/student');
        }
    }, [user, navigate]);

    if (!user) {
        return null;
    }

    return <RegistrationSuccessContent user={user} />;
}