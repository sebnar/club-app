import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createMember } from '../services/api'
import './CreateMember.css'

function CreateMember() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const [formData, setFormData] = useState({
    name: '',
    nickname: '',
    email: '',
    phone: '',
    city: '',
    description: '',
    birthday: '',
    join_date: '',
    car_year: '',
    car_model: '',
    car_color: ''
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }


  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      // Preparar datos para enviar
      const memberData = {
        name: formData.name.trim(),
        ...(formData.nickname && { nickname: formData.nickname.trim() }),
        ...(formData.email && { email: formData.email.trim() }),
        ...(formData.phone && { phone: formData.phone.trim() }),
        ...(formData.city && { city: formData.city.trim() }),
        ...(formData.description && { description: formData.description.trim() }),
        ...(formData.birthday && { birthday: formData.birthday }),
        ...(formData.join_date && { join_date: formData.join_date }),
        ...(formData.car_year && { car_year: parseInt(formData.car_year) }),
        ...(formData.car_model && { car_model: formData.car_model.trim() }),
        ...(formData.car_color && { car_color: formData.car_color.trim() })
      }

      await createMember(memberData)
      setSuccess(true)
      
      // Redirigir después de 2 segundos
      setTimeout(() => {
        navigate('/members')
      }, 2000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear el miembro. Por favor intenta de nuevo.')
      console.error('Error creating member:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="create-member-page">
      <div className="page-header">
        <button onClick={() => navigate('/members')} className="back-button">
          ← Volver a Miembros
        </button>
        <h1>Registrar Nuevo Miembro</h1>
        <p>Completa el formulario para agregar un nuevo miembro al club</p>
      </div>

      {success && (
        <div className="alert alert-success">
          ✅ ¡Miembro creado exitosamente! Redirigiendo...
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

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="birthday">Fecha de Cumpleaños</label>
              <input
                type="date"
                id="birthday"
                name="birthday"
                value={formData.birthday}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="join_date">Fecha de Ingreso al Club</label>
              <input
                type="date"
                id="join_date"
                name="join_date"
                value={formData.join_date}
                onChange={handleChange}
              />
            </div>
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

        <div className="form-actions">
          <button
            type="button"
            onClick={() => navigate('/members')}
            className="btn-cancel"
            disabled={loading}
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="btn-submit"
            disabled={loading || !formData.name.trim()}
          >
            {loading ? 'Creando...' : 'Crear Miembro'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default CreateMember

