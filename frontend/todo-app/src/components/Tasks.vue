<template>
  <main class="app-container">
    <div class="todo-card">
      
      <div class="header">
        <h1>Lista de Tarefas</h1>
        <button @click="handleLogout" class="logout-btn">Sair</button>
      </div>

      <form @submit.prevent="addTodo" class="task-form">
        <input
          type="text"
          v-model="newTodo"
          placeholder="Adicionar nova tarefa..."
        />
        <button type="submit">Adicionar</button>
      </form>

      <ul class="task-list">
        <li v-for="todo in todos" :key="todo._id" :class="{ completed: todo.done }">
          <span @click="updateTodoStatus(todo)" class="task-title">
            {{ todo.text }}
          </span>
          <button @click="deleteTodo(todo._id)" class="delete-btn">×</button>
        </li>
      </ul>
    </div>
  </main>
</template>

<script>
// Convertido para Options API, como nos slides
import axios from 'axios';

export default {
  data() {
    return {
      todos: [],
      newTodo: ''
    };
  },
  async mounted() {
    // Tenta fazer login automático se houver token
    await this.tryAutoLogin();
    // 'mounted' é chamado quando o componente é carregado
    this.loadTodos();
  },
  methods: {
    async loadTodos() {
      try {
        const response = await axios.get('/todos');
        this.todos = response.data;
      } catch (error) {
        console.error('Erro ao carregar tarefas:', error);
        // Proteção de rota: se não estiver logado, volta ao login
        if (error.response && error.response.status === 401) {
          this.$router.push('/'); 
        }
      }
    },
    async addTodo() {
      if (this.newTodo.trim() === '') return;
      try {
        // Envia 'text' como nos slides
        const response = await axios.post('/todos', { text: this.newTodo });
        this.todos.push(response.data);
        this.newTodo = '';
      } catch (error) {
        console.error('Erro ao adicionar tarefa:', error);
      }
    },
    async updateTodoStatus(todo) {
      try {
        const newStatus = !todo.done;
        // Envia 'done' como nos slides
        await axios.put(`/todos/${todo._id}`, {
          done: newStatus,
        });
        // Atualiza o status local
        todo.done = newStatus;
      } catch (error) {
        console.error('Erro ao atualizar tarefa:', error);
      }
    },
    async deleteTodo(taskId) {
      try {
        await axios.delete(`/todos/${taskId}`);
        this.todos = this.todos.filter((task) => task._id !== taskId);
      } catch (error) {
        console.error('Erro ao excluir tarefa:', error);
      }
    },
    
    // Método de Logout (Exercício)
    async handleLogout() {
      try {
        // Obtém o token do localStorage para revogá-lo
        const token = localStorage.getItem('authToken');
        const logoutData = token ? { token } : {};
        
        await axios.post('/todos/logout', logoutData);
        
        // Remove o token do localStorage
        localStorage.removeItem('authToken');
        
        this.$router.push('/'); // Redireciona para o login
      } catch (error) {
        console.error('Erro ao fazer logout:', error);
        // Remove o token mesmo se houver erro
        localStorage.removeItem('authToken');
        this.$router.push('/'); // Força o redirecionamento
      }
    },
    async tryAutoLogin() {
      const token = localStorage.getItem('authToken');
      if (token) {
        try {
          const response = await axios.post('/todos/auto-login', {
            token: token
          });
          if (response.status === 200) {
            console.log('Login automatico realizado com sucesso');
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
  }
};
</script>

<style scoped>
/* Seus estilos estão ótimos. Apenas adicionei o .header e .logout-btn */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.header h1 {
  margin-bottom: 0;
  margin-top: 0;
}
.logout-btn {
  padding: 0.5rem 1rem;
  border: none;
  background-color: var(--danger-color, #e74c3c);
  color: white;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background-color 0.3s ease;
}
.logout-btn:hover {
  background-color: #c0392b;
}

.app-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 1rem;
}
.todo-card {
  font-size: 100%;
  max-width: 40rem; 
  width: 100%;
  background: var(--card-bg);
  padding: 2rem 2.5rem; 
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1.5rem rgba(6, 40, 175, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
h1 {
  text-align: center;
  color: var(--primary-color);
  margin-top: 0;
  font-size: 2.25rem; 
  margin-bottom: 1.5rem;
  font-weight: 600;
}
.task-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
}
.task-form input {
  flex-grow: 1;
  padding: 0.75rem 1rem;
  border: 2px solid var(--light-gray);
  border-radius: 0.5rem;
  font-size: 1rem; 
  transition: border-color 0.3s ease;
}
.task-form input::placeholder {
  color: var(--placeholder-color);
}
.task-form input:focus {
  outline: none;
  border-color: var(--primary-color);
}
.task-form button {
  padding: 0.75rem 1.5rem;
  border: none;
  background-color: var(--primary-color);
  color: white;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s ease, transform 0.2s ease;
}
.task-form button:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}
.task-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.task-list li {
  display: flex;
  align-items: center;
  padding: 1rem;
  background-color: #fff;
  border: 1px solid var(--light-gray);
  border-radius: 0.5rem;
  margin-bottom: 0.75rem;
  transition: all 0.3s ease;
  font-size: 1rem;
}
.task-list li:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.07);
}
.task-list li.completed .task-title {
  text-decoration: line-through;
  color: var(--placeholder-color);
}
.task-list li.completed {
  opacity: 0.7;
}
.task-title {
  cursor: pointer;
  flex-grow: 1;
  padding-left: 1rem;
}
.delete-btn {
  background: transparent;
  border: none;
  color: var(--placeholder-color);
  font-size: 1.5rem;
  cursor: pointer;
  transition: color 0.3s ease, transform 0.2s ease;
  padding: 0 0.5rem;
}
.delete-btn:hover {
  color: var(--danger-color);
}
</style>