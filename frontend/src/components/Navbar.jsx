import { Link, useLocation } from 'react-router-dom'
import './Navbar.css'

function Navbar() {
  const location = useLocation()

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
        </ul>
      </div>
    </nav>
  )
}

export default Navbar

