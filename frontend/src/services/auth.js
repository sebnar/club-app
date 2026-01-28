import api from './api'

export const authService = {
  login: async (username, password) => {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)

    const response = await api.post('/api/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  getCurrentUser: async () => {
    const response = await api.get('/api/auth/me')
    return response.data
  },

  logout: () => {
    // El logout es principalmente del lado del cliente
    // Solo limpiamos el token
    localStorage.removeItem('token')
  },

  changePassword: async (currentPassword, newPassword) => {
    const response = await api.post('/api/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword
    })
    return response.data
  },
}
