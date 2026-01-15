/**
 * Date Written: 1/15/2026 at 1:29 PM
 */
import cmuImage from '@/assets/cmu.jpg'
import cmuLogo from '@/assets/cmu-logo.png'

export function RegistrationImageSection() {
    return (
        <div className="relative h-full w-full overflow-hidden text-white">

            {/* Background Image */}
            <div
                className="absolute inset-0 bg-cover bg-center"
                style={{ backgroundImage: `url(${cmuImage})` }}
            />

            {/* Overlay */}
            <div className="absolute inset-0 bg-gradient-to-b from-black/30 via-black/45 to-black/80" />

            {/* Content */}
            <div className="relative z-10 h-full px-14 py-12 flex flex-col">

                {/* Header (top-left) */}
                <div className="flex items-center gap-3">
                    <img
                        src={cmuLogo}
                        alt="CMU Logo"
                        className="h-11 w-11 rounded-md bg-white p-1"
                    />
                    <div>
                        <p className="text-sm font-semibold leading-none">
                            City of Malabon
                        </p>
                        <p className="text-xs opacity-80">
                            University
                        </p>
                    </div>
                </div>

                {/* Hero text (left, not centered) */}
                <div className="mt-24 max-w-xl">
                    <h1 className="text-5xl font-bold leading-tight tracking-tight">
                        <span className="block">Honoring the Past,</span>
                        <span className="block text-cyan-400">
                            Shaping the Future
                        </span>
                    </h1>

                    <p className="mt-6 text-base text-white/90 leading-relaxed">
                        Advancing academic excellence and community service
                        through innovative learning and character development.
                    </p>
                </div>

                {/* Spacer */}
                <div className="flex-1" />

                {/* Footer */}
                <p className="text-xs text-white/70">
                    © {new Date().getFullYear()} City of Malabon University
                </p>
            </div>
        </div>
    )
}
