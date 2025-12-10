import { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Members from './pages/Members'
import MemberProfile from './pages/MemberProfile'
import CreateMember from './pages/CreateMember'
import EditMember from './pages/EditMember'
import Contacts from './pages/Contacts'
import './App.css'

function App() {
  // Despertar el backend cuando se carga el frontend
  useEffect(() => {
    const wakeBackend = async () => {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      try {
        // Ping al backend para mantenerlo activo
        await fetch(`${apiUrl}/api/health`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
        console.log('✅ Backend despertado')
      } catch (error) {
        // Silencioso - el backend se despertará en el próximo request real
        console.log('Backend durmiendo, se despertará en el próximo request')
      }
    }

    // Despertar inmediatamente al cargar el frontend
    wakeBackend()
  }, [])

  return (
    <Router>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/members" element={<Members />} />
            <Route path="/members/new" element={<CreateMember />} />
            <Route path="/members/:id" element={<MemberProfile />} />
            <Route path="/members/:id/edit" element={<EditMember />} />
            <Route path="/contacts" element={<Contacts />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

