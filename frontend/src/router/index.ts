import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import HomePage from '@/views/HomePage.vue'
import AboutPage from '@/views/AboutPage.vue'
import TeamPage from '@/views/TeamPage.vue'
import AttributionsPage from '@/views/AttributionsPage.vue'

// Services pages
import ServicesOverview from '@/views/services/ServicesOverview.vue'
import VehicleServices from '@/views/services/VehicleServices.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/services',
      name: 'services',
      component: ServicesOverview
    },
    {
      path: '/services/vehicle',
      name: 'services-vehicle',
      component: VehicleServices
    },
    {
      path: '/about',
      name: 'about',
      component: AboutPage
    },
    {
      path: '/team',
      name: 'team',
      component: TeamPage
    },
    {
      path: '/attributions',
      name: 'attributions',
      component: AttributionsPage
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage
    }
  ],
  scrollBehavior(to, _from, _savedPosition) {
    // Scroll to anchor if present
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    }
    // Otherwise scroll to top
    return { top: 0 }
  }
})

// Navigation guard for protected routes (to be added in later slices)
router.beforeEach((_to, _from, next) => {
  // For now, just proceed
  // In later slices, we'll add protection for dashboard, quotes, claims
  next()
})

export default router
