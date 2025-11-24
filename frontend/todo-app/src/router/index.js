// /frontend/src/router/index.js
import { createWebHistory, createRouter } from "vue-router";
import Login from "@/components/login.vue";
import Dashboard from "@/components/Tasks.vue"; // Usando seu componente Tasks.vue
import Register from "@/components/Register.vue"; // Novo componente (exercício)
import axios from "axios";

const routes = [
    {
        path: "/",
        name: "Login",
        component: Login,
    },
    {
        path: "/dashboard",
        name: "Dashboard",
        component: Dashboard,
        meta: { requiresAuth: true }
    },
    {
        path: "/register", // Rota para o exercício de cadastro
        name: "Register",
        component: Register,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// Guard de navegação para tentar auto-login
router.beforeEach(async (to, from, next) => {
    // Se a rota requer autenticação
    if (to.matched.some(record => record.meta.requiresAuth)) {
        const token = localStorage.getItem('authToken');
        
        // Se houver token, tenta fazer auto-login
        if (token) {
            try {
                const response = await axios.post('/todos/auto-login', { token });
                if (response.status === 200) {
                    // Auto-login bem-sucedido, permite acesso
                    next();
                    return;
                }
            } catch (error) {
                // Se auto-login falhar, remove token e redireciona para login
                localStorage.removeItem('authToken');
            }
        }
        
        // Verifica se há sessão ativa
        try {
            const sessionResponse = await axios.get('/todos/session');
            if (sessionResponse.data.logged_in) {
                next();
                return;
            }
        } catch (error) {
            // Sem sessão ativa
        }
        
        // Redireciona para login se não houver autenticação
        next('/');
    } else {
        // Rota pública, permite acesso
        next();
    }
})

export default router;