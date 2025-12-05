import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getMember, updateMember } from '../services/api'
import './EditMember.css'

function EditMember() {
  const navigate = useNavigate()
  const { id } = useParams()
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const [formData, setFormData] = useState({
    name: '',
    nickname: '',
    email: '',
    phone: '',
    city: '',
    description: '',
    car_year: '',
    car_model: '',
    car_color: '',
    interests: []
  })

  const [currentInterest, setCurrentInterest] = useState('')

  useEffect(() => {
    loadMember()
  }, [id])

  const loadMember = async () => {
    try {
      setLoading(true)
      const member = await getMember(id)
      
      setFormData({
        name: member.name || '',
        nickname: member.nickname || '',
        email: member.email || '',
        phone: member.phone || '',
        city: member.city || '',
        description: member.description || '',
        car_year: member.car_year ? member.car_year.toString() : '',
        car_model: member.car_model || '',
        car_color: member.car_color || '',
        interests: member.interests || []
      })
      
      setError(null)
    } catch (err) {
      setError('Error al cargar el miembro')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleAddInterest = () => {
    if (currentInterest.trim() && !formData.interests.includes(currentInterest.trim())) {
      setFormData(prev => ({
        ...prev,
        interests: [...prev.interests, currentInterest.trim()]
      }))
      setCurrentInterest('')
    }
  }

  const handleRemoveInterest = (interest) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.filter(i => i !== interest)
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    setSuccess(false)

    try {
      // Preparar datos para enviar (solo campos con valor)
      const memberData = {
        ...(formData.name.trim() && { name: formData.name.trim() }),
        ...(formData.nickname && { nickname: formData.nickname.trim() }),
        ...(formData.email && { email: formData.email.trim() }),
        ...(formData.phone && { phone: formData.phone.trim() }),
        ...(formData.city && { city: formData.city.trim() }),
        ...(formData.description && { description: formData.description.trim() }),
        ...(formData.car_year && { car_year: parseInt(formData.car_year) }),
        ...(formData.car_model && { car_model: formData.car_model.trim() }),
        ...(formData.car_color && { car_color: formData.car_color.trim() }),
        ...(formData.interests.length > 0 && { interests: formData.interests })
      }

      await updateMember(id, memberData)
      setSuccess(true)
      
      // Redirigir después de 1.5 segundos
      setTimeout(() => {
        navigate(`/members/${id}`)
      }, 1500)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al actualizar el miembro. Por favor intenta de nuevo.')
      console.error('Error updating member:', err)
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="edit-member-page">
        <div className="loading">Cargando información del miembro...</div>
      </div>
    )
  }

  if (error && !formData.name) {
    return (
      <div className="edit-member-page">
        <div className="error-container">
          <div className="error">{error}</div>
          <button onClick={() => navigate('/members')} className="btn-back">
            Volver a Miembros
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="edit-member-page">
      <div className="page-header">
        <button onClick={() => navigate(`/members/${id}`)} className="back-button">
          ← Volver al Perfil
        </button>
        <h1>Editar Miembro</h1>
        <p>Actualiza la información del miembro</p>
      </div>

      {success && (
        <div className="alert alert-success">
          ✅ ¡Miembro actualizado exitosamente! Redirigiendo...
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          ❌ {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="member-form">
        <div className="form-section">
          <h2>Información Personal</h2>
          
          <div className="form-group">
            <label htmlFor="name">
              Nombre Completo <span className="required">*</span>
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              maxLength={100}
              placeholder="Ej: Juan Pérez"
            />
          </div>

          <div className="form-group">
            <label htmlFor="nickname">Apodo / Nombre de Usuario</label>
            <input
              type="text"
              id="nickname"
              name="nickname"
              value={formData.nickname}
              onChange={handleChange}
              maxLength={50}
              placeholder="Ej: @juanperez"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="ejemplo@email.com"
              />
            </div>

            <div className="form-group">
              <label htmlFor="phone">Teléfono</label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                maxLength={20}
                placeholder="+57 300 123 4567"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="city">Ciudad</label>
            <input
              type="text"
              id="city"
              name="city"
              value={formData.city}
              onChange={handleChange}
              maxLength={100}
              placeholder="Ej: Bogotá"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Descripción</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              maxLength={500}
              rows={4}
              placeholder="Cuéntanos sobre ti..."
            />
            <small>{formData.description.length}/500 caracteres</small>
          </div>
        </div>

        <div className="form-section">
          <h2>Información del Vehículo</h2>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="car_year">Año</label>
              <input
                type="number"
                id="car_year"
                name="car_year"
                value={formData.car_year}
                onChange={handleChange}
                min="1980"
                max="2030"
                placeholder="Ej: 2020"
              />
            </div>

            <div className="form-group">
              <label htmlFor="car_model">Modelo</label>
              <input
                type="text"
                id="car_model"
                name="car_model"
                value={formData.car_model}
                onChange={handleChange}
                maxLength={50}
                placeholder="Ej: Jetta GLI"
              />
            </div>

            <div className="form-group">
              <label htmlFor="car_color">Color</label>
              <input
                type="text"
                id="car_color"
                name="car_color"
                value={formData.car_color}
                onChange={handleChange}
                maxLength={50}
                placeholder="Ej: Negro"
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h2>Intereses</h2>
          
          <div className="interests-input">
            <input
              type="text"
              value={currentInterest}
              onChange={(e) => setCurrentInterest(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddInterest())}
              placeholder="Escribe un interés y presiona Enter"
              maxLength={50}
            />
            <button
              type="button"
              onClick={handleAddInterest}
              className="btn-add-interest"
            >
              Agregar
            </button>
          </div>

          {formData.interests.length > 0 && (
            <div className="interests-list">
              {formData.interests.map((interest, index) => (
                <span key={index} className="interest-tag">
                  {interest}
                  <button
                    type="button"
                    onClick={() => handleRemoveInterest(interest)}
                    className="remove-interest"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={() => navigate(`/members/${id}`)}
            className="btn-cancel"
            disabled={saving}
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="btn-submit"
            disabled={saving || !formData.name.trim()}
          >
            {saving ? 'Guardando...' : 'Guardar Cambios'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default EditMember

