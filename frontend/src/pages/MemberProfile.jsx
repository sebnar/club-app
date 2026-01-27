import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { getMember, deactivateMember, activateMember, deleteMember } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import DeleteConfirmModal from '../components/DeleteConfirmModal'
import './MemberProfile.css'

function MemberProfile() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user, isAdmin } = useAuth()
  const [member, setMember] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showDeactivateModal, setShowDeactivateModal] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [actionLoading, setActionLoading] = useState(false)

  // Verificar si el usuario puede editar este perfil
  const canEdit = () => {
    if (!user) return false
    if (isAdmin()) return true
    return user.member_id === id
  }

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

  const handleDeactivate = async () => {
    try {
      setActionLoading(true)
      setError(null) // Limpiar errores previos
      await deactivateMember(id)
      await loadMember() // Recargar para actualizar el estado
      setShowDeactivateModal(false)
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Error al inactivar el miembro'
      setError(errorMessage)
      console.error('Error al inactivar:', err)
    } finally {
      setActionLoading(false)
    }
  }

  const handleActivate = async () => {
    try {
      setActionLoading(true)
      setError(null) // Limpiar errores previos
      await activateMember(id)
      await loadMember() // Recargar para actualizar el estado
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Error al reactivar el miembro'
      setError(errorMessage)
      console.error('Error al reactivar:', err)
    } finally {
      setActionLoading(false)
    }
  }

  const handleDelete = async () => {
    try {
      setActionLoading(true)
      setError(null) // Limpiar errores previos
      await deleteMember(id)
      setShowDeleteModal(false)
      navigate('/members')
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Error al eliminar el miembro'
      setError(errorMessage)
      console.error('Error al eliminar:', err)
      setShowDeleteModal(false)
    } finally {
      setActionLoading(false)
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
      <div className="profile-actions">
        <Link to="/members" className="back-link">← Volver a miembros</Link>
        {user && (
          <div className="action-buttons">
            {/* Solo admin puede activar/desactivar */}
            {isAdmin() && member && !member.is_active && (
              <button
                onClick={handleActivate}
                className="btn-activate"
                disabled={actionLoading}
              >
                {actionLoading ? 'Reactivando...' : '✅ Reactivar'}
              </button>
            )}
            {/* Solo admin o dueño puede editar */}
            {canEdit() && (
              <Link to={`/members/${id}/edit`} className="edit-button">
                ✏️ Editar
              </Link>
            )}
            {/* Solo admin puede inactivar */}
            {isAdmin() && member && member.is_active !== false && (
              <button
                onClick={() => setShowDeactivateModal(true)}
                className="btn-deactivate"
                disabled={actionLoading}
              >
                ⚠️ Inactivar
              </button>
            )}
            {/* Solo admin puede eliminar */}
            {isAdmin() && (
              <button
                onClick={() => setShowDeleteModal(true)}
                className="btn-delete"
                disabled={actionLoading}
              >
                🗑️ Eliminar
              </button>
            )}
          </div>
        )}
      </div>

      {error && (
        <div className="alert alert-error">
          ❌ {error}
        </div>
      )}

      {member && member.is_active === false && (
        <div className="alert alert-warning">
          ⚠️ Este miembro está inactivo
        </div>
      )}
      
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

        {(member.birthday || member.join_date) && (
          <div className="profile-section">
            <h2>Fechas Importantes</h2>
            <div className="info-grid">
              {member.birthday && (
                <div className="info-item">
                  <span className="label">Cumpleaños:</span>
                  <span className="value">
                    {new Date(member.birthday).toLocaleDateString('es-CO', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </span>
                </div>
              )}
              {member.join_date && (
                <div className="info-item">
                  <span className="label">Ingreso al Club:</span>
                  <span className="value">
                    {new Date(member.join_date).toLocaleDateString('es-CO', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </span>
                </div>
              )}
            </div>
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

      </div>

      <DeleteConfirmModal
        isOpen={showDeactivateModal}
        onClose={() => setShowDeactivateModal(false)}
        onConfirm={handleDeactivate}
        memberName={member?.name || ''}
        type="deactivate"
      />

      <DeleteConfirmModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onConfirm={handleDelete}
        memberName={member?.name || ''}
        type="delete"
      />
    </div>
  )
}

export default MemberProfile

