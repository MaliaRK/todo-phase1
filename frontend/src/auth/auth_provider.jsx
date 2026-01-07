import React, { createContext, useContext, useReducer } from 'react';

// Create the authentication context
const AuthContext = createContext();

// Initial state for authentication
const initialState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
};

// Reducer for authentication state
const authReducer = (state, action) => {
  switch (action.type) {
    case 'LOGIN_START':
      return {
        ...state,
        isLoading: true,
      };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        isLoading: false,
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        isLoading: false,
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: !!action.payload,
        isLoading: false,
      };
    default:
      return state;
  }
};

// AuthProvider component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Login function
  const login = async (email, password) => {
    dispatch({ type: 'LOGIN_START' });

    try {
      const baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${baseURL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        const { access_token } = data;

        // Store token in localStorage (or use HttpOnly cookies in production)
        localStorage.setItem('auth_token', access_token);

        // Decode token to get user info (simplified)
        const tokenPayload = JSON.parse(atob(access_token.split('.')[1]));

        dispatch({
          type: 'LOGIN_SUCCESS',
          payload: {
            user: { id: tokenPayload.sub, email: tokenPayload.email },
            token: access_token,
          },
        });

        return { success: true };
      } else {
        const errorData = await response.json();
        dispatch({ type: 'LOGIN_FAILURE' });
        return { success: false, error: errorData.detail || 'Login failed' };
      }
    } catch (error) {
      dispatch({ type: 'LOGIN_FAILURE' });
      return { success: false, error: error.message };
    }
  };

  // Logout function
  const logout = () => {
    // Remove token from localStorage
    localStorage.removeItem('auth_token');

    dispatch({ type: 'LOGOUT' });
  };

  // Check if user is authenticated
  const checkAuthStatus = () => {
    const token = localStorage.getItem('auth_token');

    if (token) {
      try {
        // Decode token to get user info
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));

        dispatch({
          type: 'SET_USER',
          payload: { id: tokenPayload.sub, email: tokenPayload.email },
        });
      } catch (error) {
        // Token is invalid, clear it
        localStorage.removeItem('auth_token');
        dispatch({ type: 'SET_USER', payload: null });
      }
    } else {
      dispatch({ type: 'SET_USER', payload: null });
    }
  };

  // Initialize auth status when component mounts
  React.useEffect(() => {
    checkAuthStatus();
  }, []);

  const value = {
    ...state,
    login,
    logout,
    checkAuthStatus,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
};