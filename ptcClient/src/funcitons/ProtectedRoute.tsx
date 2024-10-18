import React from 'react';
import { useAuth } from './AuthProvider';
import { Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute = () => {
    //This function checks if a user is authenticated, if not it redirects someone to the login page if there someone tries to go a protected page
    const user = useAuth();
    if(!user?.token) return <Navigate to='/login' />;
    return <Outlet/>
}

export default ProtectedRoute;