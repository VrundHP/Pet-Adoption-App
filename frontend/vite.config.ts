import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Allow access from Docker or other network devices
    port: 5173,      // Ensure the port matches your Dockerfile EXPOSE
  },
});
