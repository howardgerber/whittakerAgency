<template>
  <div class="admin-page">
    <div class="dashboard-layout">
      <AdminSidebar />
      <main class="main-content">
        <slot></slot>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import AdminSidebar from './AdminSidebar.vue'
</script>

<style scoped>
.admin-page {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  margin-left: 260px;
  flex: 1;
  padding: 2rem;
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 80px;
  }
}
</style>
