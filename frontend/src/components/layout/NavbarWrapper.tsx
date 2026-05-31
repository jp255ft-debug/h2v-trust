"use client";
import { usePathname } from "next/navigation";
import Navbar from "./Navbar";

export default function NavbarWrapper() {
  const pathname = usePathname();

  // Oculta a Navbar na tela de login (com fallback startsWith para query params)
  if (pathname === "/login" || pathname?.startsWith("/login")) {
    return null;
  }

  return <Navbar />;
}
