"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

export default function Navbar() {
  const pathname = usePathname();
  const { user } = useAuth();
  const role = user?.role;

  const isActive = (path: string) => {
    if (path === "/producer") return pathname === "/producer";
    return pathname.startsWith(path);
  };

  return (
    <nav className="border-b bg-card">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-6">
            <Link href="/" className="text-xl font-bold text-foreground hover:text-primary transition">
              H2V-Trust
            </Link>
            <div className="flex gap-4">
              <Link href="/dashboard" className={`text-sm font-medium transition ${isActive("/dashboard") ? "text-primary" : "text-foreground hover:text-primary"}`}>
                Dashboard
              </Link>

              {(role === "admin" || role === "auditor") && (
                <Link href="/auditor" className={`text-sm font-medium transition ${isActive("/auditor") ? "text-primary" : "text-foreground hover:text-primary"}`}>
                  Auditor
                </Link>
              )}

              {(role === "admin" || role === "operator") && (
                <Link href="/producer" className={`text-sm font-medium transition ${isActive("/producer") ? "text-primary" : "text-foreground hover:text-primary"}`}>
                  Produtor
                </Link>
              )}

              {role === "admin" && (
                <Link href="/admin" className={`text-sm font-medium transition ${isActive("/admin") ? "text-primary" : "text-foreground hover:text-primary"}`}>
                  Admin
                </Link>
              )}
            </div>
          </div>
        </div>
        {/* Submenu do Produtor */}
        {(role === "admin" || role === "operator") && pathname.startsWith("/producer") && (
          <div className="flex gap-4 mt-3 pt-3 border-t">
            <Link href="/producer" className={`text-xs font-medium transition ${pathname === "/producer" ? "text-primary" : "text-muted-foreground hover:text-primary"}`}>
              📊 Painel
            </Link>
            <Link href="/producer/batches" className={`text-xs font-medium transition ${isActive("/producer/batches") ? "text-primary" : "text-muted-foreground hover:text-primary"}`}>
              📦 Lotes
            </Link>
            <Link href="/producer/certificates" className={`text-xs font-medium transition ${isActive("/producer/certificates") ? "text-primary" : "text-muted-foreground hover:text-primary"}`}>
              🏅 Certificados
            </Link>
            <Link href="/producer/delegation" className={`text-xs font-medium transition ${isActive("/producer/delegation") ? "text-primary" : "text-muted-foreground hover:text-primary"}`}>
              🤝 Delegação
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
