import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Members from './pages/Members'
import MemberProfile from './pages/MemberProfile'
import CreateMember from './pages/CreateMember'
import Contacts from './pages/Contacts'
import './App.css'

function App() {
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
            <Route path="/contacts" element={<Contacts />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

