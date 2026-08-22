/**
 * RegisterPage — centered register form with subtle background.
 */
import React from 'react';
import RegisterForm from '../components/auth/RegisterForm';

export default function RegisterPage() {
  return (
    <div className="flex-1 flex items-center justify-center py-12 px-4">
      <RegisterForm />
    </div>
  );
}
