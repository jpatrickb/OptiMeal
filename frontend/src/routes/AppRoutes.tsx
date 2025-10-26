import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import LoginPage from '../pages/Auth/LoginPage';
import RegisterPage from '../pages/Auth/RegisterPage';
import MainLayout from '../components/Layout/MainLayout';
import PantryPage from '../pages/Pantry/PantryPage';
import AddFoodItemPage from '../pages/Pantry/AddFoodItemPage';
import AddToPantryPage from '../pages/Pantry/AddToPantryPage';
import EditPantryItemPage from '../pages/Pantry/EditPantryItemPage';
import MealLoggerPage from '../pages/MealLogger/MealLoggerPage';
import CreateMealPage from '../pages/MealLogger/CreateMealPage';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
}

function PublicRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return !isAuthenticated ? <>{children}</> : <Navigate to="/pantry" replace />;
}

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <RegisterPage />
            </PublicRoute>
          }
        />

        {/* Protected routes with layout */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/pantry" replace />} />
          <Route path="pantry" element={<PantryPage />} />
          <Route path="pantry/add-food-item" element={<AddFoodItemPage />} />
          <Route path="pantry/add-to-pantry" element={<AddToPantryPage />} />
          <Route path="pantry/edit/:id" element={<EditPantryItemPage />} />
          <Route path="meal-logger" element={<MealLoggerPage />} />
          <Route path="meal-logger/create" element={<CreateMealPage />} />
        </Route>

        {/* Catch all */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
