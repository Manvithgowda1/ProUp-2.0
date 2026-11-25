import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="bg-black text-white py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
          {/* Col 1 — Brand */}
          <div>
            <h2 className="text-xl font-bold tracking-tight">Proup</h2>
            <p className="mt-2 text-sm text-zinc-400">
              Professional Upgrade — Meet. Compete. Get Hired.
            </p>
          </div>

          {/* Col 2 — Quick Links */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider">
              Quick Links
            </h3>
            <ul className="mt-4 space-y-2">
              {[
                { to: "/", label: "Home" },
                { to: "/events", label: "Events" },
                { to: "/contact", label: "Contact" },
              ].map((l) => (
                <li key={l.to}>
                  <Link
                    to={l.to}
                    className="text-sm text-zinc-400 transition-colors hover:text-white"
                  >
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Col 3 — For Students */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider">
              For Students
            </h3>
            <ul className="mt-4 space-y-2">
              {[
                { to: "/events", label: "Browse Events" },
                { to: "/student/achievements", label: "Achievements" },
                { to: "#", label: "Career Resources" },
              ].map((l) => (
                <li key={l.label}>
                  <Link
                    to={l.to}
                    className="text-sm text-zinc-400 transition-colors hover:text-white"
                  >
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Col 4 — For Organizers */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider">
              For Organizers
            </h3>
            <ul className="mt-4 space-y-2">
              {[
                { to: "/organizer/create-event", label: "Create Event" },
                { to: "/organizer/dashboard", label: "Dashboard" },
                { to: "/organizer/analytics", label: "Analytics" },
              ].map((l) => (
                <li key={l.label}>
                  <Link
                    to={l.to}
                    className="text-sm text-zinc-400 transition-colors hover:text-white"
                  >
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-8 border-t border-zinc-800 pt-8 text-center text-sm text-zinc-500">
          © 2024 Proup. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
