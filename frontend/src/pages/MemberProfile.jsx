import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getMember } from '../services/api'
import './MemberProfile.css'

function MemberProfile() {
  const { id } = useParams()
  const [member, setMember] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadMember()
  }, [id])

  const loadMember = async () => {
    try {
      setLoading(true)
      const data = await getMember(id)
      setMember(data)
      setError(null)
    } catch (err) {
      setError('Error al cargar el perfil')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Cargando perfil...</div>
  }

  if (error || !member) {
    return (
      <div className="error">
        {error || 'Miembro no encontrado'}
        <Link to="/members" className="back-link">Volver a miembros</Link>
      </div>
    )
  }

  return (
    <div className="member-profile">
      <Link to="/members" className="back-link">← Volver a miembros</Link>
      
      <div className="profile-header">
        <div className="profile-avatar-large">
          {member.name.charAt(0).toUpperCase()}
        </div>
        <div className="profile-info">
          <h1>{member.name}</h1>
          {member.nickname && <p className="nickname">@{member.nickname}</p>}
        </div>
      </div>

      <div className="profile-content">
        <div className="profile-section">
          <h2>Información Personal</h2>
          <div className="info-grid">
            {member.city && (
              <div className="info-item">
                <span className="label">Ciudad:</span>
                <span className="value">{member.city}</span>
              </div>
            )}
            {member.email && (
              <div className="info-item">
                <span className="label">Email:</span>
                <span className="value">{member.email}</span>
              </div>
            )}
            {member.phone && (
              <div className="info-item">
                <span className="label">Teléfono:</span>
                <span className="value">{member.phone}</span>
              </div>
            )}
          </div>
        </div>

        {member.description && (
          <div className="profile-section">
            <h2>Descripción</h2>
            <p>{member.description}</p>
          </div>
        )}

        {(member.car_year || member.car_model || member.car_color) && (
          <div className="profile-section">
            <h2>Vehículo</h2>
            <div className="info-grid">
              {member.car_year && (
                <div className="info-item">
                  <span className="label">Año:</span>
                  <span className="value">{member.car_year}</span>
                </div>
              )}
              {member.car_model && (
                <div className="info-item">
                  <span className="label">Modelo:</span>
                  <span className="value">{member.car_model}</span>
                </div>
              )}
              {member.car_color && (
                <div className="info-item">
                  <span className="label">Color:</span>
                  <span className="value">{member.car_color}</span>
                </div>
              )}
            </div>
          </div>
        )}

        {member.interests && member.interests.length > 0 && (
          <div className="profile-section">
            <h2>Intereses</h2>
            <div className="interests">
              {member.interests.map((interest, index) => (
                <span key={index} className="interest-tag">
                  {interest}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default MemberProfile

