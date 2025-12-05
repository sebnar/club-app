import './Home.css'

function Home() {
  return (
    <div className="home">
      <div className="hero">
        <h1>Bienvenido al Club Volkswagen Jetta Colombia</h1>
        <p className="subtitle">
          La comunidad de propietarios de Volkswagen Jetta en Colombia
        </p>
      </div>

      <div className="features">
        <div className="feature-card">
          <h2>👥 Miembros</h2>
          <p>Conoce a los miembros de nuestro club y sus vehículos</p>
        </div>
        <div className="feature-card">
          <h2>📞 Directorio</h2>
          <p>Encuentra contactos de servicios especializados para tu Jetta</p>
        </div>
        <div className="feature-card">
          <h2>🚗 Comunidad</h2>
          <p>Únete a nuestra comunidad de amantes del Volkswagen Jetta</p>
        </div>
      </div>

      <div className="info-section">
        <h2>Sobre el Club</h2>
        <p>
          Somos un grupo de entusiastas del Volkswagen Jetta en Colombia. 
          Compartimos información, experiencias y recursos para mantener nuestros 
          vehículos en perfecto estado.
        </p>
      </div>
    </div>
  )
}

export default Home

