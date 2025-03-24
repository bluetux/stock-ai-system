// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173
  },
  esbuild: {
    loader: 'jsx',
    include: [/\.js$/, /\.jsx$/], // ✅ js + jsx 모두 적용
  },
})
