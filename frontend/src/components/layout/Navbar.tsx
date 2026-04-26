"use client";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="border-b bg-card">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-6">
            <Link href="/" className="text-xl font-bold text-foreground hover:text-primary transition">
              H2V-Trust
            </Link>
            <div className="flex gap-4">
              <Link href="/dashboard" className="text-sm font-medium text-foreground hover:text-primary transition">
                Dashboard
              </Link>
              <Link href="/auditor" className="text-sm font-medium text-foreground hover:text-primary transition">
                Auditor
              </Link>
              <Link href="/producer" className="text-sm font-medium text-foreground hover:text-primary transition">
                Produtor
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}