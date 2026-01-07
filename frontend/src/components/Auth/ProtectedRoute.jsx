import React from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../../auth/auth_provider';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  // If not authenticated, redirect to login
  if (!isAuthenticated) {
    // Store the attempted route for redirect after login
    router.replace(`/login?redirect=${router.asPath}`);
    return null;
  }

  // If authenticated, render the protected content
  return children;
};

export default ProtectedRoute;