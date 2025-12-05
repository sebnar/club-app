import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getMembers } from '../services/api'
import './Members.css'

function Members() {
  const [members, setMembers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadMembers()
  }, [])

  const loadMembers = async () => {
    try {
      setLoading(true)
      const data = await getMembers()
      setMembers(data)
      setError(null)
    } catch (err) {
      setError('Error al cargar miembros')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Cargando miembros...</div>
  }

  if (error) {
    return <div className="error">{error}</div>
  }

  return (
    <div className="members-page">
      <div className="page-header">
        <div className="header-content">
          <div>
            <h1>Miembros del Club</h1>
            <p>Conoce a los miembros de nuestra comunidad</p>
          </div>
          <Link to="/members/new" className="btn-add-member">
            + Nuevo Miembro
          </Link>
        </div>
      </div>

      {members.length === 0 ? (
        <div className="empty-state">
          <p>No hay miembros registrados aún.</p>
        </div>
      ) : (
        <div className="members-grid">
          {members.map((member) => (
            <Link 
              key={member.id} 
              to={`/members/${member.id}`}
              className="member-card"
            >
              <div className="member-avatar">
                {member.name.charAt(0).toUpperCase()}
              </div>
              <h3>{member.name}</h3>
              {member.nickname && (
                <p className="nickname">@{member.nickname}</p>
              )}
              {member.city && (
                <p className="city">📍 {member.city}</p>
              )}
              {member.car_year && member.car_model && (
                <p className="car-info">
                  🚗 {member.car_year} {member.car_model}
                </p>
              )}
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export default Members

