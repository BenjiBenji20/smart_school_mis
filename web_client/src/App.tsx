import './components/FaceVerification'
import './App.css'
import { Toaster } from 'sonner'
import { Routes, Route } from 'react-router'

import EmployeeRegistrationPage from './pages/authentication/EmployeeRegistrationPage'
import StudentRegistrationPage from './pages/authentication/StudentRegistrationPage'
import { RegistrationSuccessPage } from './pages/authentication/RegistrationSuccessPage'
import UserAuthenticationPage from './pages/authentication/UserAuthenticationPage'
import StudentDashboardPage from './pages/dashboard/student/StudentDashboardPage'
import { ProtectedRoute } from './middlewares/ProtectedRoute'
import StudentEnrollmentPage from './pages/dashboard/student/StudentEnrollementPage'

function App() {
    return (
        <>
            <Routes>
                <Route>
                    {/* PUBLIC ROUTES */}
                    <Route path="/register/employee" element={<EmployeeRegistrationPage />} />
                    <Route path="/register/student" element={<StudentRegistrationPage />} />
                    <Route path="/register/success" element={<RegistrationSuccessPage />} />
                    <Route path="/" element={<UserAuthenticationPage />} />
                    <Route path="/student/dashboard" element={
                        <ProtectedRoute >
                            <StudentDashboardPage />
                        </ProtectedRoute>
                    } />
                    <Route path="/student/enrollment" element={
                        <ProtectedRoute >
                            <StudentEnrollmentPage />
                        </ProtectedRoute>
                    } />
                </Route>
            </Routes>
            <Toaster />
        </>
    )
}

export default App
