/**
 * LoginPage — centered login form with subtle background.
 */
import React from 'react';
import LoginForm from '../components/auth/LoginForm';

export default function LoginPage() {
  return (
    <div className="flex-1 flex items-center justify-center py-12 px-4">
      <LoginForm />
    </div>
  );
}
