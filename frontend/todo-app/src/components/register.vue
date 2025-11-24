<template>
  <main class="login-page-container">
    <div class="todo-card login-card">
      <h1>Cadastro</h1>
      <form @submit.prevent="handleRegister" class="login-form">
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" v-model="password" required />
        </div>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>
        <button type="submit" class="login-button register-button">Cadastrar</button>
      </form>
      <p class="register-link">
        Já possui uma conta? <router-link to="/">Faça o login!</router-link>
      </p>
    </div>
  </main>
</template>

<script>
import axios from 'axios';
import { RouterLink } from 'vue-router';

export default {
  name: 'Register',
  components: {
    RouterLink
  },
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
      successMessage: ''
    };
  },
  methods: {
    async handleRegister() {
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        // Usa a URL base do main.js
        const response = await axios.post('/todos/register', {
          email: this.email,
          password: this.password
        });
        
        if (response.status === 201) {
          this.successMessage = "Cadastro realizado com sucesso! Redirecionando para o login...";
          setTimeout(() => {
            this.$router.push('/');
          }, 2000);
        }
      } catch (error) {
        console.error('Erro ao cadastrar:', error);
        if (error.response && error.response.status === 409) {
          this.errorMessage = 'Este e-mail já está cadastrado.';
        } else {
          this.errorMessage = 'Ocorreu um erro. Tente novamente mais tarde.';
        }
      }
    }
  }
};
</script>

<style scoped>
/* Estilos copiados do login.vue, com botão verde */
.error {
  color: red;
  text-align: center;
  margin-bottom: 1rem;
}
.success {
  color: green;
  text-align: center;
  margin-bottom: 1rem;
}
.register-button {
  background-color: #28a745 !important;
}
.register-button:hover {
  background-color: #218838 !important;
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