// /frontend/src/main.js
import './assets/main.css'
import router from './router'
import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios' // Importa o axios

// --- Configuração Global do Axios (ESSENCIAL) ---

// 1. Define a URL base da API
axios.defaults.baseURL = 'http://localhost:5000' 

// 2. PERMITE que o axios envie cookies (da sessão) para o backend
axios.defaults.withCredentials = true;

// 3. Interceptor para tentar auto-login quando receber 401
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Se receber 401 e não for uma tentativa de auto-login
    if (error.response && error.response.status === 401 && 
        !originalRequest._retry && 
        !originalRequest.url.includes('/auto-login')) {
      
      originalRequest._retry = true;
      const token = localStorage.getItem('authToken');
      
      if (token) {
        try {
          // Tenta fazer auto-login
          const response = await axios.post('/todos/auto-login', { token });
          if (response.status === 200) {
            // Retenta a requisição original
            return axios(originalRequest);
          }
        } catch (autoLoginError) {
          // Se auto-login falhar, remove o token
          localStorage.removeItem('authToken');
        }
      }
    }
    
    return Promise.reject(error);
  }
);
// --- Fim da Configuração ---

const app = createApp(App)
app.use(router)
app.mount('#app')