import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const isAuthenticated = request.cookies.get("revix_session")?.value === "demo";
  const isDashboard = request.nextUrl.pathname.startsWith("/dashboard");

  if (isDashboard && !isAuthenticated) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"]
};
