<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1>Whittaker</h1>
      <p>Admin Dashboard</p>
    </div>
    <nav class="nav-menu">
      <router-link to="/admin" class="nav-item" :class="{active: $route.path === '/admin'}">
        <span class="nav-icon">📊</span>
        <span>Dashboard</span>
      </router-link>
      <router-link to="/admin/quotes" class="nav-item" :class="{active: $route.path.startsWith('/admin/quotes')}">
        <span class="nav-icon">💬</span>
        <span>Quote Requests</span>
      </router-link>
      <router-link to="/admin/claims" class="nav-item" :class="{active: $route.path.startsWith('/admin/claims')}">
        <span class="nav-icon">🛡️</span>
        <span>Claims</span>
      </router-link>
      <router-link to="/admin/messages" class="nav-item" :class="{active: $route.path.startsWith('/admin/messages')}">
        <span class="nav-icon">✉️</span>
        <span>Messages</span>
      </router-link>
      <router-link to="/admin/users" class="nav-item" :class="{active: $route.path.startsWith('/admin/users')}">
        <img src="/images/icons/users.png" alt="Users" class="nav-icon-img" />
        <span>Users</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
const $route = useRoute()
</script>

<style scoped>
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, var(--color-primary) 0%, #002873 100%);
  color: white;
  padding: 0;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.sidebar-header {
  padding: 2rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.sidebar-header p {
  font-size: 0.875rem;
  opacity: 0.8;
}

.nav-menu {
  padding: 1.5rem 0;
}

.nav-item {
  padding: 0.875rem 1.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background-color: rgba(255, 255, 255, 0.15);
  border-left: 4px solid #ffc107;
  padding-left: calc(1.5rem - 4px);
}

.nav-icon {
  font-size: 1.25rem;
}

.nav-icon-img {
  width: 20px;
  height: 20px;
  object-fit: contain;
  filter: brightness(0) invert(1); /* Makes icon white */
}

@media (max-width: 768px) {
  .sidebar {
    width: 80px;
  }

  .sidebar-header h1 {
    font-size: 1.25rem;
  }

  .sidebar-header p,
  .nav-item span:not(.nav-icon) {
    display: none;
  }
}
</style>
