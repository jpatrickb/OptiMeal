import { AuthProvider } from './contexts/AuthContext';
import AppRoutes from './routes/AppRoutes';
import { CssBaseline } from '@mui/material';

function App() {
  return (
    <AuthProvider>
      <CssBaseline />
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;
