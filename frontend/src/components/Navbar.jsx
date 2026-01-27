import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './Navbar.css'

function Navbar() {
  const location = useLocation()
  const navigate = useNavigate()
  const { isAuthenticated, user, logout, isAdmin } = useAuth()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          🚗 Club VW Jetta Colombia
        </Link>
        <ul className="navbar-menu">
          <li>
            <Link 
              to="/" 
              className={location.pathname === '/' ? 'active' : ''}
            >
              Inicio
            </Link>
          </li>
          <li>
            <Link 
              to="/members" 
              className={location.pathname.startsWith('/members') ? 'active' : ''}
            >
              Miembros
            </Link>
          </li>
          <li>
            <Link 
              to="/contacts" 
              className={location.pathname === '/contacts' ? 'active' : ''}
            >
              Directorio
            </Link>
          </li>
          {isAuthenticated() && isAdmin() && (
            <li>
              <Link 
                to="/members/new" 
                className={location.pathname === '/members/new' ? 'active' : ''}
              >
                Nuevo Miembro
              </Link>
            </li>
          )}
        </ul>
        <div className="navbar-auth">
          {isAuthenticated() ? (
            <div className="user-menu">
              <span className="user-info">
                {user?.username} {isAdmin() && <span className="admin-badge">Admin</span>}
              </span>
              <button onClick={handleLogout} className="logout-button">
                Cerrar Sesión
              </button>
            </div>
          ) : (
            <Link to="/login" className="login-link">
              Iniciar Sesión
            </Link>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar

