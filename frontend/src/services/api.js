import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Members API
export const getMembers = async () => {
  const response = await api.get('/api/members')
  return response.data
}

export const getMember = async (id) => {
  const response = await api.get(`/api/members/${id}`)
  return response.data
}

export const createMember = async (memberData) => {
  const response = await api.post('/api/members', memberData)
  return response.data
}

export const updateMember = async (id, memberData) => {
  const response = await api.put(`/api/members/${id}`, memberData)
  return response.data
}

export const deleteMember = async (id) => {
  await api.delete(`/api/members/${id}`)
}

// Contacts API
export const getContacts = async (category = null) => {
  const params = category ? { category } : {}
  const response = await api.get('/api/contacts', { params })
  return response.data
}

export const getCategories = async () => {
  const response = await api.get('/api/contacts/categories')
  return response.data
}

export const createContact = async (contactData) => {
  const response = await api.post('/api/contacts', contactData)
  return response.data
}

export default api

