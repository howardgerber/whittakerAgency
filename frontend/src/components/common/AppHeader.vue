<template>
  <header class="header">
    <div class="container header-content">
      <!-- Logo -->
      <div class="logo">
        <RouterLink to="/">
          <span class="logo-text">Whittaker Agency</span>
        </RouterLink>
      </div>

      <!-- Desktop Navigation -->
      <nav class="nav-desktop">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/services" class="nav-link">Services</RouterLink>
        <RouterLink to="/about" class="nav-link">About</RouterLink>
        <RouterLink to="/team" class="nav-link">Team</RouterLink>

        <!-- User Menu (Authenticated) -->
        <template v-if="authStore.isAuthenticated">
          <div class="user-menu">
            <button class="user-menu-btn" @click="toggleUserMenu">
              <span class="user-name">{{ authStore.user?.full_name }}</span>
              <span class="dropdown-icon">▼</span>
            </button>

            <div v-if="showUserMenu" class="user-dropdown">
              <RouterLink to="/dashboard" class="dropdown-item" @click="closeUserMenu">
                Dashboard
              </RouterLink>
              <RouterLink to="/quotes" class="dropdown-item" @click="closeUserMenu">
                My Quotes
              </RouterLink>
              <RouterLink to="/claims" class="dropdown-item" @click="closeUserMenu">
                My Claims
              </RouterLink>
              <button class="dropdown-item logout-btn" @click="handleLogout">
                Logout
              </button>
            </div>
          </div>
        </template>

        <!-- Sign In/Register (Not Authenticated) -->
        <template v-else>
          <RouterLink to="/login" class="btn btn-outline">Sign In</RouterLink>
          <RouterLink to="/register" class="btn btn-primary">Get Started</RouterLink>
        </template>
      </nav>

      <!-- Mobile Menu Button -->
      <button class="mobile-menu-btn" @click="toggleMobileMenu" aria-label="Toggle menu">
        <span class="hamburger" :class="{ 'active': showMobileMenu }">
          <span></span>
          <span></span>
          <span></span>
        </span>
      </button>
    </div>

    <!-- Mobile Navigation -->
    <div class="nav-mobile" :class="{ 'active': showMobileMenu }">
      <RouterLink to="/" class="nav-link-mobile" @click="closeMobileMenu">Home</RouterLink>
      <RouterLink to="/services" class="nav-link-mobile" @click="closeMobileMenu">Services</RouterLink>
      <RouterLink to="/about" class="nav-link-mobile" @click="closeMobileMenu">About</RouterLink>
      <RouterLink to="/team" class="nav-link-mobile" @click="closeMobileMenu">Team</RouterLink>

      <template v-if="authStore.isAuthenticated">
        <div class="mobile-divider"></div>
        <RouterLink to="/dashboard" class="nav-link-mobile" @click="closeMobileMenu">Dashboard</RouterLink>
        <RouterLink to="/quotes" class="nav-link-mobile" @click="closeMobileMenu">My Quotes</RouterLink>
        <RouterLink to="/claims" class="nav-link-mobile" @click="closeMobileMenu">My Claims</RouterLink>
        <button class="nav-link-mobile logout-btn-mobile" @click="handleLogout">Logout</button>
      </template>
      <template v-else>
        <div class="mobile-divider"></div>
        <RouterLink to="/login" class="nav-link-mobile" @click="closeMobileMenu">Sign In</RouterLink>
        <RouterLink to="/register" class="nav-link-mobile btn-mobile" @click="closeMobileMenu">Get Started</RouterLink>
      </template>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const showMobileMenu = ref(false)
const showUserMenu = ref(false)

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const closeUserMenu = () => {
  showUserMenu.value = false
}

const handleLogout = () => {
  authStore.logout()
  showMobileMenu.value = false
  showUserMenu.value = false
  router.push('/login')
}

// Close menus when clicking outside
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.user-menu') && showUserMenu.value) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.header {
  background-color: var(--color-primary);
  color: var(--color-white);
  padding: var(--spacing-md) 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Logo */
.logo a {
  text-decoration: none;
}

.logo-text {
  font-family: var(--font-heading);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-white);
  transition: opacity 0.3s ease;
}

.logo a:hover .logo-text {
  opacity: 0.9;
}

/* Desktop Navigation */
.nav-desktop {
  display: flex;
  gap: var(--spacing-lg);
  align-items: center;
}

.nav-link {
  color: var(--color-white);
  font-weight: 600;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

/* User Menu */
.user-menu {
  position: relative;
}

.user-menu-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: var(--color-white);
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.user-menu-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.user-name {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-icon {
  font-size: 0.7rem;
  transition: transform 0.3s ease;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  overflow: hidden;
  animation: dropdownFade 0.2s ease;
}

@keyframes dropdownFade {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 0.75rem 1rem;
  color: var(--color-text);
  text-decoration: none;
  text-align: left;
  background: none;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
  font-weight: 500;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.logout-btn {
  border-top: 1px solid #e9ecef;
  color: #dc3545;
}

/* Buttons */
.btn-outline {
  color: var(--color-white);
  border: 2px solid var(--color-white);
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  background: transparent;
}

.btn-outline:hover {
  background: var(--color-white);
  color: var(--color-primary);
}

.btn-primary {
  background: var(--color-white);
  color: var(--color-primary);
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

/* Mobile Menu Button */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.hamburger {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 24px;
}

.hamburger span {
  display: block;
  width: 100%;
  height: 3px;
  background: var(--color-white);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.hamburger.active span:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.hamburger.active span:nth-child(2) {
  opacity: 0;
}

.hamburger.active span:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* Mobile Navigation */
.nav-mobile {
  display: none;
  flex-direction: column;
  background: var(--color-primary);
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.nav-mobile.active {
  max-height: 500px;
  padding: var(--spacing-md) 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-link-mobile {
  color: var(--color-white);
  text-decoration: none;
  padding: 0.75rem var(--spacing-md);
  font-weight: 600;
  transition: background-color 0.2s ease;
  display: block;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.nav-link-mobile:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link-mobile.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.mobile-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: var(--spacing-sm) 0;
}

.logout-btn-mobile {
  color: #ffcccc;
}

.btn-mobile {
  margin: var(--spacing-sm) var(--spacing-md);
  background: var(--color-white);
  color: var(--color-primary);
  padding: 0.75rem;
  text-align: center;
  border-radius: 4px;
  font-weight: 700;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-desktop {
    display: none;
  }

  .mobile-menu-btn {
    display: block;
  }

  .nav-mobile {
    display: flex;
  }
}
</style>
