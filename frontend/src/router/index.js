import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import Auth from '../views/Auth.vue'
import MainLayout from '../layouts/MainLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import Vault from '../views/Vault.vue'
import Letters from '../views/Letters.vue'
import Executor from '../views/Executor.vue' // <-- 1. Added the missing import

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // --- Public Routes ---
    { path: '/', name: 'home', component: LandingPage },
    { path: '/login', name: 'login', component: Auth },
    
    // --- App Routes (Wrapped in Navbar/Sidebar layout) ---
    {
      path: '/',
      component: MainLayout,
      children: [
        { path: 'dashboard', name: 'dashboard', component: Dashboard },
        { path: 'vault', name: 'vault', component: Vault },
        { path: 'letters', name: 'letters', component: Letters },
        { path: 'executor', name: 'executor', component: Executor } // <-- 2. Moved inside the layout
      ]
    }
  ]
})

export default router