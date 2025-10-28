<template>
  <div class="dashboard-page">
    <div class="container">
      <div class="dashboard-header">
        <h1>Welcome back, {{ userName }}!</h1>
        <p>Manage your insurance quotes and requests</p>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <router-link to="/quote" class="action-card">
          <img src="/images/icons/quote.png" alt="Request Quote" class="icon-img">
          <h3>Request Quote</h3>
          <p>Get a new insurance quote</p>
        </router-link>
        <router-link to="/claims/submit" class="action-card">
          <img src="/images/icons/Claim.png" alt="File Claim" class="icon-img">
          <h3>File Claim</h3>
          <p>Submit an insurance claim</p>
        </router-link>
        <router-link to="/contact" class="action-card">
          <img src="/images/icons/contact.png" alt="Contact" class="icon-img">
          <h3>Contact Us</h3>
          <p>Send us a message</p>
        </router-link>
      </div>

      <!-- Tabbed Section for Claims and Quotes -->
      <div class="tabbed-section">
        <!-- Tab Navigation -->
        <div class="tab-bar">
          <button
            :class="['tab-button', { active: activeTab === 'quotes' }]"
            @click="activeTab = 'quotes'"
          >
            Quotes
          </button>
          <button
            :class="['tab-button', { active: activeTab === 'claims' }]"
            @click="activeTab = 'claims'"
          >
            Claims
          </button>
          <button
            :class="['tab-button', { active: activeTab === 'messages' }]"
            @click="activeTab = 'messages'"
          >
            Messages
          </button>
        </div>

        <!-- Tab Content -->
        <div class="tab-content">
          <!-- Quote Requests Tab -->
          <div v-if="activeTab === 'quotes'" class="tab-panel">
            <QuotesList />
          </div>

          <!-- Claims Tab -->
          <div v-if="activeTab === 'claims'" class="tab-panel">
            <ClaimsList />
          </div>

          <!-- Contact Messages Tab -->
          <div v-if="activeTab === 'messages'" class="tab-panel">
            <ContactMessagesList />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import QuotesList from '@/components/dashboard/QuotesList.vue'
import ClaimsList from '@/components/dashboard/ClaimsList.vue'
import ContactMessagesList from '@/components/dashboard/ContactMessagesList.vue'

const authStore = useAuthStore()
const userName = ref(authStore.user?.full_name || 'User')

// Tab state
const activeTab = ref<'claims' | 'quotes' | 'messages'>('quotes')
</script>

<style scoped>
.dashboard-page {
  min-height: calc(100vh - 200px);
  padding: 3rem 0;
  background: #f5f7fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  color: var(--color-primary);
  margin-bottom: 0.5rem;
}

.dashboard-header p {
  color: #666;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.action-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s;
  cursor: pointer;
}

.action-card:not(.disabled):hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 61, 165, 0.2);
}

.action-card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-card .icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.action-card .icon-img {
  width: 3rem;
  height: 3rem;
  margin-bottom: 1rem;
}

.action-card h3 {
  color: var(--color-primary);
  margin-bottom: 0.5rem;
}

.action-card p {
  color: #666;
  font-size: 0.9rem;
}

/* Tabbed Section */
.tabbed-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.tab-bar {
  display: flex;
  border-bottom: 2px solid #e0e0e0;
  background: #e0e0e0;
}

.tab-button {
  flex: 0 0 25%;
  padding: 1rem 2rem;
  background: #f8f9fa;
  border: none;
  font-size: 1rem;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  border-bottom: 3px solid transparent;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  border-top: 3px solid transparent;
  border-left: 1px solid transparent;
  border-right: 1px solid transparent;
}

.tab-button:hover {
  color: var(--color-primary);
  background: #ffffff;
}

.tab-button.active {
  color: var(--color-primary);
  font-weight: 700;
  border-bottom-color: var(--color-primary);
  border-top-color: var(--color-primary);
  border-left-color: var(--color-primary);
  border-right-color: var(--color-primary);
  background: white;
}

.tab-content {
  padding: 2rem;
}

.tab-panel {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .quick-actions {
    grid-template-columns: 1fr;
  }

  .tab-bar {
    flex-direction: row;
  }

  .tab-button {
    padding: 0.875rem 1rem;
    font-size: 0.95rem;
  }

  .tab-content {
    padding: 1.5rem;
  }
}
</style>
