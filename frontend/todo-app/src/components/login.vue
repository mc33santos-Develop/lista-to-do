<template>
  <main class="login-page-container">
    <div class="todo-card login-card">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" v-model="password" required />
        </div>
        <div class="form-group remember-me">
          <label class="remember-label">
            <input type="checkbox" v-model="rememberMe" />
            <span>Lembrar-me</span>
          </label>
        </div>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <button type="submit" class="login-button">Login</button>
      </form>
      <p class="register-link">
        Não possui uma conta? <router-link to="/register">Cadastre-se!</router-link>
      </p>
    </div>
  </main>
</template>

<script>
import axios from 'axios';
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router';

export default {
  name: 'Login',
  components: {
    RouterLink
  },
  data() {
    return {
      email: '',
      password: '',
      rememberMe: false,
      errorMessage: ''
    };
  },
  methods: {
    async handleLogin() {
      this.errorMessage = '';
      try {
        // Usa a URL base do main.js
        const response = await axios.post(`/todos/login`, {
          email: this.email,
          password: this.password,
          remember_me: this.rememberMe
        });
        if (response.status === 200) {
          // Se "Lembrar-me" estiver marcado e houver token, salva no localStorage
          if (this.rememberMe && response.data.token) {
            localStorage.setItem('authToken', response.data.token);
            console.log('Token salvo para login automatico');
          }
          this.$router.push('/dashboard');
        }
      } catch (error) {
        console.error('Erro ao fazer login:', error);
        if (error.response && (error.response.status === 401 || error.response.status === 404)) {
            this.errorMessage = 'Login falhou. Verifique e-mail e senha informados.';
        } else {
            this.errorMessage = 'Ocorreu um erro. Tente novamente mais tarde.';
        }
      }
    },
    async tryAutoLogin() {
      const token = localStorage.getItem('authToken');
      if (token) {
        try {
          const response = await axios.post(`/todos/auto-login`, {
            token: token
          });
          if (response.status === 200) {
            console.log('Login automatico realizado com sucesso');
            this.$router.push('/dashboard');
            return true;
          }
        } catch (error) {
          // Se o token for inválido, remove do localStorage
          if (error.response && error.response.status === 401) {
            localStorage.removeItem('authToken');
            console.log('Token invalido, removido do localStorage');
          }
        }
      }
      return false;
    }
  }, 

  async mounted() {
    // Tenta fazer login automático se houver token
    await this.tryAutoLogin();
  }
};
</script>

<style scoped>
.error {
  color: red;
  text-align: center;
  margin-bottom: 1rem;
}
.login-page-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh; 
  padding: 1rem;
}
.login-card {
  max-width: 40rem;
  padding: 2rem 2.5rem;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1.5rem rgba(6, 40, 175, 0.1);
  background: var(--card-bg, rgba(255, 255, 255, 0.9)); 
}
h1 {
  text-align: center;
  color: var(--primary-color, #3498db);
  margin-top: 0;
  font-size: 2.25rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
}
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.form-group {
  text-align: left;
}
.form-group label {
  font-weight: bold;
  margin-bottom: 0.5rem;
  display: block;
  color: var(--text-color, #34495e);
  font-size: 1.0em;
}
.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--light-gray, #ecf0f1);
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  color: var(--text-color, #34495e);
}
.form-group input::placeholder {
  color: var(--placeholder-color, #95a5a6);
}
.form-group input:focus {
  outline: none;
  border-color: var(--primary-color, #3498db);
}
.remember-me {
  margin-top: -0.5rem;
}
.remember-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--text-color, #34495e);
}
.remember-label input[type="checkbox"] {
  width: auto;
  cursor: pointer;
}
.login-button {
  width: 100%;
  padding: 0.75rem 1.5rem;
  border: none;
  background-color: var(--primary-color, #3498db);
  color: white;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s ease, transform 0.2s ease;
}
.login-button:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}
.register-link {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.9rem;
  color: var(--text-color, #34495e);
}
.register-link a {
  color: var(--primary-color, #3498db);
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
}
.register-link a:hover {
  color: #2980b9;
  text-decoration: underline;
}
</style>