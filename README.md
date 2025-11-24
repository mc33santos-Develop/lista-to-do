# 📋 Projeto To-Do List Full-Stack

Aplicação web completa de lista de tarefas desenvolvida com Vue.js, Flask e MongoDB.

## 🚀 Tecnologias Utilizadas

### Frontend
- **Vue.js 3** - Framework JavaScript reativo
- **Vue Router** - Roteamento de páginas
- **Axios** - Cliente HTTP para comunicação com API
- **Vite** - Build tool e servidor de desenvolvimento

### Backend
- **Flask** - Framework web Python
- **Flask-Session** - Gerenciamento de sessões
- **Flask-CORS** - Suporte a CORS
- **PyMongo** - Driver MongoDB para Python
- **Werkzeug** - Utilitários de segurança (hash de senhas)

### Banco de Dados
- **MongoDB** - Banco de dados NoSQL

## ✨ Funcionalidades

### Autenticação
- ✅ Cadastro de usuários
- ✅ Login com email e senha
- ✅ **Login automático (Remember Me)** - Tokens persistentes por 30 dias
- ✅ Logout com revogação de tokens
- ✅ Verificação de sessão ativa
- ✅ Sessões legíveis no MongoDB

### Tarefas
- ✅ Criar nova tarefa
- ✅ Listar todas as tarefas do usuário
- ✅ Marcar tarefas como concluídas
- ✅ Excluir tarefas
- ✅ Tarefas isoladas por usuário

### Segurança
- ✅ Senhas criptografadas (hash)
- ✅ Tokens de autenticação com expiração
- ✅ Sessões protegidas
- ✅ Middleware de autenticação

## 🏗️ Estrutura do Projeto

```
todo_list_app/
├── backend/
│   ├── app.py                 # Aplicação Flask principal
│   ├── config.py              # Configurações
│   ├── database/              # Módulo de banco (Singleton)
│   │   ├── connection.py      # Conexão MongoDB
│   │   └── __init__.py
│   ├── models/                # Modelos de dados
│   │   ├── user.py            # Modelo User
│   │   ├── task.py            # Modelo Task
│   │   └── __init__.py
│   ├── services/              # Lógica de negócio
│   │   ├── auth_service.py    # Serviço de autenticação
│   │   ├── task_service.py    # Serviço de tarefas
│   │   ├── session_service.py # Serviço de sessões
│   │   ├── token_service.py   # Serviço de tokens
│   │   └── __init__.py
│   ├── routes/                # Rotas da API
│   │   ├── auth_routes.py     # Rotas de autenticação
│   │   ├── task_routes.py     # Rotas de tarefas
│   │   └── __init__.py
│   ├── middleware/            # Middlewares
│   │   ├── auth_middleware.py # Middleware de autenticação
│   │   └── __init__.py
│   └── requirements.txt       # Dependências Python
│
└── frontend/
    └── todo-app/
        ├── src/
        │   ├── components/     # Componentes Vue
        │   │   ├── login.vue
        │   │   ├── Tasks.vue
        │   │   └── register.vue
        │   ├── router/         # Configuração de rotas
        │   ├── App.vue
        │   └── main.js
        └── package.json        # Dependências Node
```

## 📦 Pré-requisitos

- **Python 3.7+**
- **Node.js 20+** e npm
- **MongoDB** (rodando em localhost:27017)

## 🛠️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/mc33santos-Develop/lista-to-do.git
cd lista-to-do
```

### 2. Configure o Backend

```bash
# Navegue até a pasta backend
cd backend

# Crie e ative um ambiente virtual
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
.\venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor
python app.py
```

O backend estará rodando em `http://localhost:5000`

### 3. Configure o Frontend

```bash
# Navegue até a pasta do frontend
cd frontend/todo-app

# Instale as dependências
npm install

# Execute o servidor de desenvolvimento
npm run dev
```

O frontend estará rodando em `http://localhost:5173`

### 4. Configure o MongoDB

Certifique-se de que o MongoDB está rodando:

```bash
# Windows (se instalado como serviço)
net start MongoDB

# Ou inicie manualmente
mongod
```

## 📡 Endpoints da API

### Autenticação

- `POST /todos/register` - Cadastro de usuário
- `POST /todos/login` - Login (aceita `remember_me: true`)
- `POST /todos/logout` - Logout
- `GET /todos/session` - Verificar sessão ativa
- `POST /todos/auto-login` - Login automático com token

### Tarefas

- `GET /todos` - Listar todas as tarefas do usuário
- `POST /todos` - Criar nova tarefa
- `PUT /todos/<id>` - Atualizar tarefa
- `DELETE /todos/<id>` - Deletar tarefa

## 🔐 Segurança

- Senhas são armazenadas com hash (Werkzeug)
- Tokens de autenticação com expiração (30 dias)
- Sessões protegidas por middleware
- CORS configurado para origens específicas

## 📊 Banco de Dados

### Coleções

- `users` - Usuários cadastrados
- `todos` - Tarefas dos usuários
- `sessions` - Sessões do Flask (criptografadas)
- `sessions_info` - Informações legíveis das sessões
- `auth_tokens` - Tokens de autenticação persistente

## 🎯 Funcionalidades Avançadas

### Login Automático (Remember Me)

Quando o usuário marca "Lembrar-me" no login:
1. Um token é gerado e salvo no banco de dados
2. O token é armazenado no `localStorage` do navegador
3. Ao acessar o site novamente, o login é automático
4. Tokens expiram em 30 dias ou podem ser revogados no logout

### Sessões Legíveis

As sessões são salvas em duas coleções:
- `sessions`: Dados criptografados do Flask-Session
- `sessions_info`: Informações legíveis (email, datas, etc.)

Isso permite visualizar no MongoDB Compass:
- Email do usuário
- Data de criação
- Data de atualização
- Data de expiração
- Status ativo

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👤 Autor

Desenvolvido como projeto de aprendizado em desenvolvimento full-stack.
