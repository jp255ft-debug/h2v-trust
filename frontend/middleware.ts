import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Rotas protegidas que exigem autenticação
const PROTECTED_ROUTES = ["/admin", "/producer", "/auditor"];

// Rotas públicas (não exigem autenticação)
const PUBLIC_ROUTES = ["/login", "/api/auth/login"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Verificar se a rota é protegida
  const isProtected = PROTECTED_ROUTES.some((route) =>
    pathname.startsWith(route)
  );

  // Verificar se a rota é pública
  const isPublic = PUBLIC_ROUTES.some((route) => pathname.startsWith(route));

  // Se for uma rota de API do Next.js, não bloquear
  if (pathname.startsWith("/_next") || pathname.startsWith("/api/health")) {
    return NextResponse.next();
  }

  // Se for uma rota protegida, verificar token
  if (isProtected && !isPublic) {
    // Verificar cookie definido pelo useAuth após login bem-sucedido
    const token = request.cookies.get("h2v_admin_token")?.value;

    if (!token) {
      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("redirect", pathname);
      return NextResponse.redirect(loginUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/admin/:path*", "/producer/:path*", "/auditor/:path*", "/login"],
};
