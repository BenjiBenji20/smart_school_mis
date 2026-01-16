/**
 * Date Written: 1/16/2026
 */

import {
    Sheet,
    SheetContent,
    SheetTrigger,
    SheetTitle,
    SheetDescription,
} from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";
import { Menu } from "lucide-react";
import { SidebarLayout } from "./SidebarLayout";
import { type SidebarProps } from "@/types/sidebar.types";

export function MobileSidebar({
    sections,
    universityName = "City of Malabon University",
    universityLogo,
    onLogout,
}: SidebarProps) {
    return (
        <Sheet>
            <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="lg:hidden">
                    <Menu className="h-5 w-5" />
                </Button>
            </SheetTrigger>

            <SheetContent
                side="left"
                className="w-64 p-0"
            >
                {/* REQUIRED for accessibility */}
                <SheetTitle className="sr-only">
                    {universityName} Navigation
                </SheetTitle>

                <SheetDescription className="sr-only">
                    Main navigation menu for {universityName}
                </SheetDescription>

                <div className="h-full">
                    <SidebarLayout
                        sections={sections}
                        universityName={universityName}
                        universityLogo={universityLogo}
                        onLogout={onLogout}
                        collapsed={false}
                    />
                </div>
            </SheetContent>
        </Sheet>
    );
}
