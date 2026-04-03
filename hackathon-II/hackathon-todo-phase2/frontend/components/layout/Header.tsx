// frontend/components/layout/Header.tsx
'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';
import { useSession, signoutUser } from '../../lib/auth';
import Sheet from '../ui/Sheet';

const Header: React.FC = () => {
  const { data: session, isLoading } = useSession();
  const router = useRouter();
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const profileRef = useRef<HTMLDivElement>(null);

  const handleSignOut = async () => {
    setMobileMenuOpen(false);
    setProfileOpen(false);
    await signoutUser();
    router.push('/auth/signin');
    router.refresh();
  };

  // Close menus on route change
  useEffect(() => {
    setMobileMenuOpen(false);
    setProfileOpen(false);
  }, [pathname]);

  // Close profile dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (profileRef.current && !profileRef.current.contains(e.target as Node)) {
        setProfileOpen(false);
      }
    };
    if (profileOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [profileOpen]);

  const isActive = (href: string) => pathname === href;

  const mobileNavLinkClasses = (href: string) =>
    `flex items-center gap-3 w-full px-4 py-3 rounded-xl text-sm font-medium transition-colors duration-200 ${
      isActive(href)
        ? 'bg-brand-50 text-brand-700'
        : 'text-gray-700 hover:bg-gray-50'
    }`;

  return (
    <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-lg border-b border-gray-200/60">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        {/* Logo */}
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-brand-500 to-violet-600 flex items-center justify-center">
              <svg className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" strokeWidth="2.5" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
            </div>
            <span className="text-lg font-bold text-gray-900 tracking-tight">Todoist</span>
          </Link>
        </div>

        {/* Desktop Right */}
        <div className="hidden sm:flex items-center gap-3">
          {isLoading ? (
            <div className="spinner h-5 w-5" />
          ) : session ? (
            <>
              {pathname !== '/tasks' && (
                <Link href="/tasks" className="btn-primary text-sm !px-4 !py-2">Dashboard</Link>
              )}

              {/* Avatar + Dropdown */}
              <div className="relative" ref={profileRef}>
                <button
                  onClick={() => setProfileOpen(!profileOpen)}
                  className="h-9 w-9 rounded-full bg-gradient-to-br from-brand-400 to-violet-500 flex items-center justify-center text-white text-sm font-bold ring-2 ring-transparent hover:ring-brand-200 transition-all duration-200 focus:outline-none focus:ring-brand-300"
                  aria-label="User menu"
                >
                  {(session.user?.name || session.user?.email || 'U').charAt(0).toUpperCase()}
                </button>

                {/* Dropdown */}
                <div
                  className={`absolute right-0 mt-2 w-64 rounded-xl bg-white border border-gray-200 shadow-lg ring-1 ring-black/5 transition-all duration-200 origin-top-right ${
                    profileOpen
                      ? 'opacity-100 scale-100 pointer-events-auto'
                      : 'opacity-0 scale-95 pointer-events-none'
                  }`}
                >
                  {/* User info */}
                  <div className="px-4 py-4 border-b border-gray-100">
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-full bg-gradient-to-br from-brand-400 to-violet-500 flex items-center justify-center text-white text-sm font-bold shrink-0">
                        {(session.user?.name || session.user?.email || 'U').charAt(0).toUpperCase()}
                      </div>
                      <div className="min-w-0">
                        <p className="text-sm font-semibold text-gray-900 truncate">{session.user?.name || 'User'}</p>
                        <p className="text-xs text-gray-500 truncate">{session.user?.email}</p>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="py-1.5">
                    <button
                      onClick={handleSignOut}
                      className="flex items-center gap-2.5 w-full px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors"
                    >
                      <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
                      </svg>
                      Sign Out
                    </button>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <>
              <Link href="/auth/signin" className="btn-ghost text-sm">Sign In</Link>
              <Link href="/auth/signup" className="btn-primary text-sm !px-4 !py-2">Get Started</Link>
            </>
          )}
        </div>

        {/* Mobile Hamburger */}
        <button
          onClick={() => setMobileMenuOpen(true)}
          className="sm:hidden h-9 w-9 rounded-lg flex items-center justify-center text-gray-600 hover:bg-gray-100 transition-colors"
          aria-label="Open menu"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>
        </button>
      </div>

      {/* Mobile Sheet */}
      <Sheet open={mobileMenuOpen} onClose={() => setMobileMenuOpen(false)} side="right" title="Menu">
        <div className="flex flex-col h-full">
          {/* Navigation */}
          <nav className="flex-1 px-3 py-4 space-y-1">
            <Link href="/" className={mobileNavLinkClasses('/')}>
              <svg className="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955a1.126 1.126 0 011.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
              </svg>
              Home
            </Link>

            {session && (
              <Link href="/tasks" className={mobileNavLinkClasses('/tasks')}>
                <svg className="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25z" />
                </svg>
                My Tasks
              </Link>
            )}

            <div className="my-3 border-t border-gray-100" />

            {isLoading ? (
              <div className="flex justify-center py-6">
                <div className="spinner h-5 w-5" />
              </div>
            ) : session ? (
              <>
                {/* User info card */}
                <div className="mx-1 mb-3 p-4 rounded-xl bg-gray-50 border border-gray-100">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-full bg-gradient-to-br from-brand-400 to-violet-500 flex items-center justify-center text-white text-sm font-bold shrink-0">
                      {(session.user?.name || session.user?.email || 'U').charAt(0).toUpperCase()}
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-gray-900 truncate">{session.user?.name || 'User'}</p>
                      <p className="text-xs text-gray-500 truncate">{session.user?.email}</p>
                    </div>
                  </div>
                </div>

                {pathname !== '/tasks' && (
                  <Link
                    href="/tasks"
                    className="flex items-center gap-3 w-full px-4 py-3 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-brand-500 to-violet-600 hover:from-brand-600 hover:to-violet-700 transition-all shadow-sm"
                  >
                    <svg className="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
                    </svg>
                    Go to Dashboard
                  </Link>
                )}
              </>
            ) : (
              <div className="space-y-2 px-1">
                <Link
                  href="/auth/signup"
                  className="flex items-center justify-center w-full py-3 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-brand-500 to-violet-600 hover:from-brand-600 hover:to-violet-700 transition-all shadow-sm"
                >
                  Get Started
                </Link>
                <Link
                  href="/auth/signin"
                  className="flex items-center justify-center w-full py-3 rounded-xl text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 transition-colors"
                >
                  Sign In
                </Link>
              </div>
            )}
          </nav>

          {/* Bottom sign-out */}
          {session && !isLoading && (
            <div className="px-3 py-4 border-t border-gray-100">
              <button
                onClick={handleSignOut}
                className="flex items-center gap-3 w-full px-4 py-3 rounded-xl text-sm font-medium text-red-600 hover:bg-red-50 transition-colors"
              >
                <svg className="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
                </svg>
                Sign Out
              </button>
            </div>
          )}
        </div>
      </Sheet>
    </header>
  );
};

export default Header;