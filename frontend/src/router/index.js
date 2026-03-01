import { createRouter, createWebHistory } from 'vue-router'

// --- Import all pages ---
import LandingPage from '../views/LandingPage.vue'
import Auth from '../views/Auth.vue'
import MainLayout from '../layouts/MainLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import Vault from '../views/Vault.vue'
import Addvault from '../views/Addvault.vue' 
import Letters from '../views/Letters.vue'
import Executor from '../views/Executor.vue'
import AddLetter from '../views/AddLetter.vue'
import ExecutorPortal from '../views/ExecutorPortal.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // --- Public Routes ---
    { path: '/', name: 'home', component: LandingPage },
    { path: '/login', name: 'login', component: Auth },
    
    // --- Executor Verification Portal ---
    { path: '/executor-portal', name: 'executor-portal', component: ExecutorPortal },
    
    // --- App Routes (Wrapped in your Navbar layout) ---
    {
      path: '/',
      component: MainLayout,
      children: [
        { path: 'dashboard', name: 'dashboard', component: Dashboard },
        { path: 'vault', name: 'vault', component: Vault },
        { path: 'addvault', name: 'addvault', component: Addvault }, 
        { path: 'letters', name: 'letters', component: Letters },
        { path: 'add-letter', name: 'add-letter', component: AddLetter },
        { path: 'executor', name: 'executor', component: Executor },
        { path: 'executor/:id', name: 'executor-detail', component: Executor, props: true },
      ]
    }
  ]
})

export default router