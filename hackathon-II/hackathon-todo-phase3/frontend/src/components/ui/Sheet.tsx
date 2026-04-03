// frontend/components/ui/Sheet.tsx
'use client';

import React, { useEffect, useCallback, useState } from 'react';
import { createPortal } from 'react-dom';

interface SheetProps {
  open: boolean;
  onClose: () => void;
  side?: 'left' | 'right';
  children: React.ReactNode;
  title?: string;
}

const Sheet: React.FC<SheetProps> = ({ open, onClose, side = 'right', children, title }) => {
  const [mounted, setMounted] = useState(false);

  // Only render portal after component mounts on client to avoid hydration mismatch
  useEffect(() => {
    setMounted(true);
  }, []);

  // Lock body scroll when open
  useEffect(() => {
    if (open) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  // Close on Escape
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    },
    [onClose]
  );

  useEffect(() => {
    if (open) {
      document.addEventListener('keydown', handleKeyDown);
    }
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [open, handleKeyDown]);

  // Don't render anything on server or before mount to avoid hydration mismatch
  if (!mounted) return null;

  const isRight = side === 'right';

  return createPortal(
    <>
      {/* Backdrop */}
      <div
        className={`fixed inset-0 z-50 bg-black/40 backdrop-blur-sm transition-opacity duration-300 ${
          open ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Panel */}
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title || 'Menu'}
        className={`fixed inset-y-0 z-50 w-[280px] max-w-[85vw] bg-white shadow-2xl flex flex-col transition-transform duration-300 ease-in-out ${
          isRight ? 'right-0' : 'left-0'
        } ${
          open
            ? 'translate-x-0'
            : isRight
            ? 'translate-x-full'
            : '-translate-x-full'
        }`}
      >
        {/* Sheet Header */}
        <div className="flex items-center justify-between px-5 h-16 border-b border-gray-100 shrink-0">
          {title && (
            <span className="text-base font-semibold text-gray-900">{title}</span>
          )}
          <button
            onClick={onClose}
            className="ml-auto h-8 w-8 rounded-lg flex items-center justify-center text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
            aria-label="Close menu"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Sheet Body */}
        <div className="flex-1 overflow-y-auto">
          {children}
        </div>
      </div>
    </>,
    document.body
  );
};

export default Sheet;
