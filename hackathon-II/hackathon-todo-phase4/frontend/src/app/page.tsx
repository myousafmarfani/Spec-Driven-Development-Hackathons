// frontend/app/page.tsx
'use client';

import Link from 'next/link';
import { useSession } from '../lib/auth';
import Header from '../components/layout/Header';

export default function HomePage() {
  const { data: session, isPending } = useSession();

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      {/* Hero */}
      <main className="flex-1 flex flex-col">
        <section className="relative overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 -z-10">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-gradient-to-br from-brand-100/60 via-violet-100/40 to-transparent rounded-full blur-3xl" />
            <div className="absolute bottom-0 right-0 w-[400px] h-[400px] bg-gradient-to-tl from-amber-100/40 to-transparent rounded-full blur-3xl" />
          </div>

          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-24 sm:pt-28 sm:pb-32 text-center">
            <div className="animate-fade-in">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-brand-50 border border-brand-200 text-brand-700 text-xs font-semibold mb-6">
                <span className="h-1.5 w-1.5 rounded-full bg-brand-500 animate-pulse" />
                Todoist - Smart Task Management
              </span>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-gray-900 leading-tight">
                Organize your work,<br />
                <span className="gradient-text">simplify your life</span>
              </h1>

              <p className="mt-6 max-w-2xl mx-auto text-lg sm:text-xl text-gray-500 leading-relaxed">
                Get organized with our super-fast task manager, <br />
                powered by Next.js and FastAPI. Add, follow, and finish your to-dos.
              </p>

              <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
                {session ? (
                  <Link href="/tasks" className="btn-primary !px-8 !py-3 text-base">
                    Go to Dashboard
                    <svg className="ml-2 h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" /></svg>
                  </Link>
                ) : (
                  <>
                    <Link href="/auth/signup" className="btn-primary !px-8 !py-3 text-base">
                      Start Free
                      <svg className="ml-2 h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" /></svg>
                    </Link>
                    <Link href="/auth/signin" className="btn-secondary !px-8 !py-3 text-base">
                      Sign In
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* Tech Stack */}
        <section className="py-16 border-t border-gray-100">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-6">Powered by</p>
            <div className="flex flex-wrap items-center justify-center gap-x-8 gap-y-4 text-sm font-medium text-gray-400">
              <span>Next.js 16</span>
              <span className="hidden sm:inline text-gray-200">|</span>
              <span>React 19</span>
              <span className="hidden sm:inline text-gray-200">|</span>
              <span>FastAPI</span>
              <span className="hidden sm:inline text-gray-200">|</span>
              <span>PostgreSQL</span>
              <span className="hidden sm:inline text-gray-200">|</span>
              <span>Tailwind CSS</span>
              <span className="hidden sm:inline text-gray-200">|</span>
              <span>Better Auth</span>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-100 py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-sm text-gray-600">&copy; 2026 Todoist. GIAIC Hackathon II</p>
          <p className="text-sm text-gray-600">Spec-Driven Development</p>
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <span>Built with 🤍 by <a href="https://github.com/myousafmarfani" target="_blank" rel="noopener noreferrer">Muhammad Yousaf</a></span>
          </div>
        </div>
      </footer>
    </div>
  );
}