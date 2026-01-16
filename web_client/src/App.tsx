import './components/FaceVerification'
import './App.css'
import { Toaster } from 'sonner'
import { Routes, Route } from 'react-router'

import EmployeeRegistrationPage from './pages/authentication/EmployeeRegistrationPage'
import StudentRegistrationPage from './pages/authentication/StudentRegistrationPage'
import { RegistrationSuccessPage } from './pages/authentication/RegistrationSuccessPage'
import UserAuthenticationPage from './pages/authentication/UserAuthenticationPage'
import StudentDashboardPage from './pages/dashboard/student/StudentDashboardPage'

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
                    <Route path="/test" element={<StudentDashboardPage />} />

                </Route>
            </Routes>
            <Toaster />
        </>
    )
}

export default App
