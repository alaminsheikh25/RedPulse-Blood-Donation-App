import { Link, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../store/auth";

const nav = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/donors", label: "Donors" },
  { to: "/requests", label: "Requests" },
  { to: "/inventory", label: "Inventory" },
  { to: "/hospitals", label: "Hospitals" },
  { to: "/appointments", label: "Appointments" },
  { to: "/campaigns", label: "Campaigns" },
  { to: "/notifications", label: "Notifications" },
  { to: "/reports", label: "Reports" },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">RedPulse</div>
        <nav>
          {nav.map((n) => (
            <Link key={n.to} to={n.to}>
              {n.label}
            </Link>
          ))}
        </nav>
        <div className="sidebar-footer">
          <div className="user">{user?.full_name}</div>
          <button
            onClick={() => {
              logout();
              navigate("/login");
            }}
          >
            Sign out
          </button>
        </div>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
