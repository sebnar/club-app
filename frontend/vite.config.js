import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  preview: {
    port: 3000,
    host: true,
    allowedHosts: [
      'jetta-club-frontend.onrender.com',
      '.onrender.com' // Permite cualquier subdominio de Render
    ]
  }
})

