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
import StudentEnrollmentTab from './pages/dashboard/student/StudentEnrollementTab'
import StudentCurrentEnrollmentTab from './pages/dashboard/student/StudentCurrentEnrollementTab'
import DeanEnrollmentApprovalTab from './pages/dashboard/dean/EnrollmentApprovalTab'

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
                            <StudentEnrollmentTab />
                        </ProtectedRoute>
                    } />
                    <Route path="/student/my-enrollment" element={
                        <ProtectedRoute >
                            <StudentCurrentEnrollmentTab />
                        </ProtectedRoute>
                    } />


                    <Route path="/dean/dashboard" element={
                        <ProtectedRoute >
                            <DeanEnrollmentApprovalTab />
                        </ProtectedRoute>
                    } />

                    <Route path="/dean/approve-enrollment" element={
                        <ProtectedRoute >
                            <DeanEnrollmentApprovalTab />
                        </ProtectedRoute>
                    } />
                </Route>
            </Routes>
            <Toaster />
        </>
    )
}

export default App
