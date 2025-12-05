import { useState, useEffect } from 'react'
import { getContacts, getCategories } from '../services/api'
import './Contacts.css'

function Contacts() {
  const [contacts, setContacts] = useState([])
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadData()
  }, [])

  useEffect(() => {
    loadContacts()
  }, [selectedCategory])

  const loadData = async () => {
    try {
      const [contactsData, categoriesData] = await Promise.all([
        getContacts(),
        getCategories()
      ])
      setContacts(contactsData)
      setCategories(categoriesData)
      setError(null)
    } catch (err) {
      setError('Error al cargar datos')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const loadContacts = async () => {
    try {
      setLoading(true)
      const data = await getContacts(selectedCategory || undefined)
      setContacts(data)
      setError(null)
    } catch (err) {
      setError('Error al cargar contactos')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading && contacts.length === 0) {
    return <div className="loading">Cargando directorio...</div>
  }

  if (error && contacts.length === 0) {
    return <div className="error">{error}</div>
  }

  return (
    <div className="contacts-page">
      <div className="page-header">
        <h1>Directorio de Contactos</h1>
        <p>Encuentra servicios especializados para tu Jetta</p>
      </div>

      {categories.length > 0 && (
        <div className="category-filter">
          <button
            className={selectedCategory === '' ? 'active' : ''}
            onClick={() => setSelectedCategory('')}
          >
            Todos
          </button>
          {categories.map((category) => (
            <button
              key={category}
              className={selectedCategory === category ? 'active' : ''}
              onClick={() => setSelectedCategory(category)}
            >
              {category}
            </button>
          ))}
        </div>
      )}

      {contacts.length === 0 ? (
        <div className="empty-state">
          <p>No hay contactos registrados en esta categoría.</p>
        </div>
      ) : (
        <div className="contacts-grid">
          {contacts.map((contact) => (
            <div key={contact.id} className="contact-card">
              <h3>{contact.name}</h3>
              <span className="category-badge">{contact.category}</span>
              
              {contact.description && (
                <p className="description">{contact.description}</p>
              )}

              <div className="contact-info">
                {contact.phone && (
                  <div className="info-row">
                    <span className="icon">📞</span>
                    <a href={`tel:${contact.phone}`}>{contact.phone}</a>
                  </div>
                )}
                {contact.email && (
                  <div className="info-row">
                    <span className="icon">✉️</span>
                    <a href={`mailto:${contact.email}`}>{contact.email}</a>
                  </div>
                )}
                {contact.address && (
                  <div className="info-row">
                    <span className="icon">📍</span>
                    <span>{contact.address}</span>
                  </div>
                )}
                {contact.website && (
                  <div className="info-row">
                    <span className="icon">🌐</span>
                    <a href={contact.website} target="_blank" rel="noopener noreferrer">
                      Visitar sitio web
                    </a>
                  </div>
                )}
                {contact.rating && (
                  <div className="info-row">
                    <span className="icon">⭐</span>
                    <span>{'★'.repeat(contact.rating)}{'☆'.repeat(5 - contact.rating)}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Contacts

