<script setup>

import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

const tasks = ref([]);
const newTaskTitle = ref('');

const fetchTasks = async () => {
  try {
    const response = await axios.get(`${API_URL}/todolist`);
    tasks.value = response.data;
  } catch (error) {
    console.error('Erro ao carregar tarefas:', error);
  }
};

const addTask = async () => {
  if (newTaskTitle.value.trim() === '') return;
  try {
    const response = await axios.post(`${API_URL}/todolist`, {
      titulo: newTaskTitle.value,
      concluido: false
    });
    tasks.value.push(response.data);
    newTaskTitle.value = '';
  } catch (error) {
    console.error('Erro ao adicionar tarefa:', error);
  }
};

const toggleTaskStatus = async (task) => {
  try {
    const updatedTaskData = { ...task, concluido: !task.concluido };
    const response = await axios.put(`${API_URL}/todolist/${task._id}`, {
      concluido: updatedTaskData.concluido,
    });
    
    const index = tasks.value.findIndex((t) => t._id === task._id);
    if (index !== -1) {
      tasks.value[index] = response.data;
    }
  } catch (error) {
    console.error('Erro ao atualizar tarefa:', error);
  }
};

const deleteTask = async (taskId) => {
  try {
    await axios.delete(`${API_URL}/todolist/${taskId}`);
    tasks.value = tasks.value.filter((task) => task._id !== taskId);
  } catch (error) {
    console.error('Erro ao excluir tarefa:', error);
  }
};

onMounted(fetchTasks);
</script>

<template>
  <main class="app-container">
    <div class="todo-card">
      <h1>Lista de Tarefas</h1>

      <form @submit.prevent="addTask" class="task-form">
        <input
          type="text"
          v-model="newTaskTitle"
          placeholder="Adicionar nova tarefa..."
        />
        <button type="submit">Adicionar</button>
      </form>

      <ul class="task-list">
        <li v-for="task in tasks" :key="task._id" :class="{ completed: task.concluido }">
          <span @click="toggleTaskStatus(task)" class="task-title">
            {{ task.titulo }}
          </span>
          <button @click="deleteTask(task._id)" class="delete-btn">×</button>
        </li>
      </ul>
    </div>
  </main>
</template>


<style>

:root {
  --primary-color: #3498db;
  --card-bg: rgba(255, 255, 255, 0.9);
  --text-color: #34495e;
  --placeholder-color: #95a5a6;
  --danger-color: #e74c3c;
  --light-gray: #ecf0f1;
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

  font-size: 50%; 
  
  
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