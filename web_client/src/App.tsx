import './components/FaceVerification'
import './App.css'
import { Toaster } from 'sonner'
import { Routes, Route } from 'react-router'

import EmployeeRegistrationPage from './pages/EmployeeRegistrationPage'
import StudentRegistrationPage from './pages/StudentRegistrationPage'


function App() {
    return (
        <>
            <Routes>
                <Route>
                    {/* PUBLIC ROUTES */}
                    <Route path="/register/employee" element={<EmployeeRegistrationPage />} />
                    <Route path="/register/student" element={<StudentRegistrationPage />} />

                </Route>
            </Routes>
            <Toaster />
        </>
    )
}

export default App
