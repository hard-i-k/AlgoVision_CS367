import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useAuthStore } from './context/authStore';
import NavBar from './components/Navbar/NavBar';
import Home from './pages/Home';
import QuestionDetail from './pages/QuestionDetail';
import AskQuestion from './pages/AskQuestion';
import Login from './pages/Login';
import Register from './pages/Register';

function App() {
  const { initialize, isAuthenticated = false } = useAuthStore();

  useEffect(() => {
    initialize();
  }, []);

  const ProtectedRoute = ({ children }) => {
    return isAuthenticated ? children : <Navigate to="/login" />;
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <NavBar />
        
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/questions/:id" element={<QuestionDetail />} />
            <Route 
              path="/ask" 
              element={
                <ProtectedRoute>
                  <AskQuestion />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/login" 
              element={
                isAuthenticated ? <Navigate to="/" /> : <Login />
              } 
            />
            <Route 
              path="/register" 
              element={
                isAuthenticated ? <Navigate to="/" /> : <Register />
              } 
            />
          </Routes>
        </main>

        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App;