import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { cn } from "@/lib/utils";

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const navLinks = [
    { to: "/", label: "Home" },
    { to: "/events", label: "Events" },
    { to: "/contact", label: "Contact" },
  ];

  const linkClass = ({
    isActive,
  }: {
    isActive: boolean;
  }) =>
    cn(
      "text-sm transition-colors",
      isActive
        ? "text-white underline underline-offset-4"
        : "text-zinc-400 hover:text-white"
    );

  return (
    <nav className="sticky top-0 z-50 bg-black text-white">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Left — brand */}
        <Link to="/" className="text-xl font-bold tracking-tight">
          Proup
        </Link>

        {/* Center — desktop nav */}
        <div className="hidden items-center gap-6 md:flex">
          {navLinks.map((l) => (
            <NavLink key={l.to} to={l.to} className={linkClass} end={l.to === "/"}>
              {l.label}
            </NavLink>
          ))}
        </div>

        {/* Right — auth actions (desktop) */}
        <div className="hidden items-center gap-4 md:flex">
          {!isAuthenticated ? (
            <>
              <Link
                to="/login"
                className="rounded-md border border-zinc-700 px-4 py-1.5 text-sm text-zinc-300 transition-colors hover:bg-zinc-800 hover:text-white"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="rounded-md bg-white px-4 py-1.5 text-sm font-medium text-black transition-colors hover:bg-zinc-200"
              >
                Register
              </Link>
            </>
          ) : (
            <>
              {user?.role === "student" && (
                <NavLink to="/student/achievements" className={linkClass}>
                  Achievements
                </NavLink>
              )}
              {user?.role === "organizer" && (
                <NavLink to="/organizer/dashboard" className={linkClass}>
                  Dashboard
                </NavLink>
              )}
              <span className="text-sm text-zinc-400">{user?.email}</span>
              <button
                onClick={logout}
                className="rounded-md px-3 py-1.5 text-sm text-zinc-300 transition-colors hover:bg-zinc-800 hover:text-white"
              >
                Logout
              </button>
            </>
          )}
        </div>

        {/* Mobile hamburger */}
        <button
          className="inline-flex items-center justify-center md:hidden"
          onClick={() => setMobileOpen((prev) => !prev)}
          aria-label="Toggle menu"
        >
          {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile dropdown */}
      {mobileOpen && (
        <div className="border-t border-zinc-800 px-4 pb-4 pt-2 md:hidden">
          <div className="flex flex-col gap-3">
            {navLinks.map((l) => (
              <NavLink
                key={l.to}
                to={l.to}
                className={linkClass}
                end={l.to === "/"}
                onClick={() => setMobileOpen(false)}
              >
                {l.label}
              </NavLink>
            ))}

            {!isAuthenticated ? (
              <>
                <Link
                  to="/login"
                  className="text-sm text-zinc-400 transition-colors hover:text-white"
                  onClick={() => setMobileOpen(false)}
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="text-sm text-zinc-400 transition-colors hover:text-white"
                  onClick={() => setMobileOpen(false)}
                >
                  Register
                </Link>
              </>
            ) : (
              <>
                {user?.role === "student" && (
                  <NavLink
                    to="/student/achievements"
                    className={linkClass}
                    onClick={() => setMobileOpen(false)}
                  >
                    Achievements
                  </NavLink>
                )}
                {user?.role === "organizer" && (
                  <NavLink
                    to="/organizer/dashboard"
                    className={linkClass}
                    onClick={() => setMobileOpen(false)}
                  >
                    Dashboard
                  </NavLink>
                )}
                <span className="text-sm text-zinc-400">{user?.email}</span>
                <button
                  onClick={() => {
                    logout();
                    setMobileOpen(false);
                  }}
                  className="text-left text-sm text-zinc-400 transition-colors hover:text-white"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
