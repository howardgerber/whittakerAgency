import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import HomePage from '@/views/HomePage.vue'
import AboutPage from '@/views/AboutPage.vue'
import TeamPage from '@/views/TeamPage.vue'
import AttributionsPage from '@/views/AttributionsPage.vue'

// Services pages
import ServicesOverview from '@/views/services/ServicesOverview.vue'
import VehicleServices from '@/views/services/VehicleServices.vue'

// Claims pages
import ClaimsPage from '@/views/ClaimsPage.vue'

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
      path: '/claims',
      name: 'claims',
      component: ClaimsPage
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
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('@/views/ContactPage.vue')
    },

    // Protected routes (require authentication)
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/quote',
      name: 'quote-request',
      component: () => import('@/views/QuoteRequestPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/quotes/:id',
      name: 'quote-detail',
      component: () => import('@/views/QuoteDetailPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/claims/submit',
      name: 'claim-submit',
      component: () => import('@/views/ClaimSubmitPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/claims/:id',
      name: 'claim-detail',
      component: () => import('@/views/ClaimDetailPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/contact/:id',
      name: 'contact-detail',
      component: () => import('@/views/ContactDetailPage.vue'),
      meta: { requiresAuth: true }
    },

    // Admin routes (require authentication + admin flag)
    {
      path: '/admin',
      name: 'admin-dashboard',
      component: () => import('@/views/AdminDashboardPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/quotes',
      name: 'admin-quotes',
      component: () => import('@/views/AdminQuotesPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/quotes/:id',
      name: 'admin-quote-detail',
      component: () => import('@/views/AdminQuoteDetailPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/claims',
      name: 'admin-claims',
      component: () => import('@/views/AdminClaimsPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/claims/:id',
      name: 'admin-claim-detail',
      component: () => import('@/views/AdminClaimDetailPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/messages',
      name: 'admin-messages',
      component: () => import('@/views/AdminMessagesPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/messages/:id',
      name: 'admin-message-detail',
      component: () => import('@/views/AdminMessageDetailPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: () => import('@/views/AdminUsersPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/users/:id',
      name: 'admin-user-detail',
      component: () => import('@/views/AdminUserDetailPage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
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

// Navigation guard for protected routes
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Redirect to login and save intended destination
    next({
      name: 'login',
      query: { redirect: to.fullPath }
    })
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    // Redirect non-admin users to regular dashboard
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
