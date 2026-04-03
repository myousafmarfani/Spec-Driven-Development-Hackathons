// frontend/middleware.ts
import { NextRequest, NextResponse } from 'next/server';

// Define protected routes
const protectedRoutes = ['/tasks', '/chat'];

export function middleware(request: NextRequest) {
  // Check if the current route is protected
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // Get the token from cookies
  const token = request.cookies.get('jwt_token')?.value;

  // If it's a protected route, check authentication
  if (isProtectedRoute) {
    // Check if user is authenticated (token exists)
    if (!token) {
      // Redirect to signin if not authenticated
      const signInUrl = new URL('/auth/signin', request.url);
      signInUrl.searchParams.set('return', request.nextUrl.pathname);
      return NextResponse.redirect(signInUrl);
    }
  } else if (request.nextUrl.pathname.startsWith('/auth')) {
    // If user is trying to access auth pages but already has a token,
    // redirect to tasks (prevent accessing login/signup when already logged in)
    if (token && (request.nextUrl.pathname === '/auth/signin' || request.nextUrl.pathname === '/auth/signup')) {
      const tasksUrl = new URL('/tasks', request.url);
      return NextResponse.redirect(tasksUrl);
    }
  }

  // Allow access to public routes or authenticated access to protected routes
  return NextResponse.next();
}

// Define which routes the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};