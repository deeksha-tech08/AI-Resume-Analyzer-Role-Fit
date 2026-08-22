/**
 * Production Navbar with responsive mobile menu and auth-aware navigation.
 */
import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/');
    setMobileOpen(false);
  };

  const isActive = (path) => location.pathname === path;

  const linkClass = (path) =>
    `transition-colors duration-200 text-sm font-medium ${
      isActive(path)
        ? 'text-brand-primary'
        : 'text-text-secondary hover:text-text-primary'
    }`;

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border-subtle bg-background-primary/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <span className="text-lg font-bold gradient-text hidden sm:inline">AI Resume Fit</span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-6">
            {isAuthenticated ? (
              <>
                <Link to="/upload" className={linkClass('/upload')}>Upload</Link>
                <Link to="/history" className={linkClass('/history')}>History</Link>
                <span className="text-text-secondary text-sm">
                  Hi, <span className="text-text-primary font-medium">{user?.full_name?.split(' ')[0]}</span>
                </span>
                <button onClick={handleLogout} className="btn-ghost text-sm">Logout</button>
              </>
            ) : (
              <>
                <Link to="/" className={linkClass('/')}>Home</Link>
                <Link to="/login" className={linkClass('/login')}>Login</Link>
                <Link to="/register" className="btn-primary text-sm">Get Started</Link>
              </>
            )}
          </div>

          {/* Mobile Hamburger */}
          <button
            className="md:hidden p-2 text-text-secondary hover:text-text-primary transition-colors"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle menu"
          >
            {mobileOpen ? (
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileOpen && (
          <div className="md:hidden pb-4 pt-2 border-t border-border-subtle fade-in">
            <div className="flex flex-col gap-3">
              {isAuthenticated ? (
                <>
                  <Link to="/upload" className={linkClass('/upload')} onClick={() => setMobileOpen(false)}>Upload Resume</Link>
                  <Link to="/history" className={linkClass('/history')} onClick={() => setMobileOpen(false)}>History</Link>
                  <span className="text-text-secondary text-sm">Hi, {user?.full_name?.split(' ')[0]}</span>
                  <button onClick={handleLogout} className="btn-ghost text-sm text-left">Logout</button>
                </>
              ) : (
                <>
                  <Link to="/" className={linkClass('/')} onClick={() => setMobileOpen(false)}>Home</Link>
                  <Link to="/login" className={linkClass('/login')} onClick={() => setMobileOpen(false)}>Login</Link>
                  <Link to="/register" className={linkClass('/register')} onClick={() => setMobileOpen(false)}>Get Started</Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
