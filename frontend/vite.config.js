import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Проксируем /api на бэкенд, чтобы не было CORS-проблем
      '/api': 'http://localhost:8000'
    }
  }
})