<template>
  <AdminLayout>
    <div class="admin-dashboard-content">
        <div class="top-bar">
          <h2>Dashboard Overview</h2>
          <p>Welcome back! Here's what's happening today.</p>
        </div>

        <div v-if="loading" class="loading">
          <p>Loading dashboard...</p>
        </div>

        <div v-else-if="error" class="error-message">
          <p>{{ error }}</p>
        </div>

        <template v-else>
          <!-- Summary Statistics -->
          <div class="stats-grid">
            <router-link to="/admin/quotes" class="stat-card stat-card-link">
              <div class="stat-header">
                <div>
                  <div class="stat-value">{{ stats.quotes.pending }}</div>
                  <div class="stat-label">Pending Quotes</div>
                </div>
                <div class="stat-icon yellow">💬</div>
              </div>
              <div class="stat-change positive">{{ stats.quotes.total }} total</div>
            </router-link>

            <router-link to="/admin/claims" class="stat-card stat-card-link">
              <div class="stat-header">
                <div>
                  <div class="stat-value">{{ stats.claims.submitted }}</div>
                  <div class="stat-label">Pending Claims</div>
                </div>
                <div class="stat-icon blue">🛡️</div>
              </div>
              <div class="stat-change positive">{{ stats.claims.total }} total</div>
            </router-link>

            <router-link to="/admin/messages" class="stat-card stat-card-link">
              <div class="stat-header">
                <div>
                  <div class="stat-value">{{ stats.messages.new }}</div>
                  <div class="stat-label">New Messages</div>
                </div>
                <div class="stat-icon green">✉️</div>
              </div>
              <div class="stat-change positive">{{ stats.messages.total }} total</div>
            </router-link>
          </div>

          <!-- Two Column Activity Grid -->
          <div class="activity-grid">
            <!-- Recent Activity - Left Column -->
            <div class="activity-section">
              <div class="section-header">
                <h3>Recent Activity</h3>
              </div>
              <div class="activity-list">
                <div v-for="activity in recentActivity" :key="`${activity.type}-${activity.date}`" class="activity-item">
                  <div class="activity-type-badge">
                    <span class="type-icon">{{ getTypeIcon(activity.type) }}</span>
                    <span>{{ formatText(activity.type) }}</span>
                  </div>
                  <div class="activity-content">
                    <div class="activity-meta">
                      <span>{{ activity.customer }}</span>
                      <span>•</span>
                      <span>{{ formatRelativeTime(activity.date) }}</span>
                    </div>
                  </div>
                  <StatusBadge :status="activity.action.toLowerCase()" />
                </div>

                <div v-if="recentActivity.length === 0" class="empty-activity">
                  <p>No recent activity</p>
                </div>
              </div>
            </div>

            <!-- Items Requiring Attention - Right Column -->
            <div class="activity-section">
              <div class="section-header">
                <h3>⏱️ Items Requiring Attention</h3>
              </div>
              <div class="activity-list">
                <router-link
                  v-for="item in attentionItems"
                  :key="`${item.type}-${item.id || item.customer_name}`"
                  :to="item.link"
                  @click="storeReferrer(item)"
                  class="attention-item"
                >
                  <div :class="['attention-icon-wrapper', getIconColor(item.priority)]">{{ item.icon }}</div>
                  <div class="attention-content">
                    <div class="activity-title">{{ item.title }}</div>
                    <div class="activity-meta">
                      <span>{{ item.category }}</span>
                      <span>•</span>
                      <span>{{ item.detail }}</span>
                      <span>•</span>
                      <span>{{ item.age }}</span>
                    </div>
                  </div>
                </router-link>

                <div v-if="attentionItems.length === 0" class="empty-activity">
                  <p>No items require attention</p>
                </div>
              </div>
            </div>
          </div>
        </template>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import adminService, { type DashboardStats, type AttentionItem } from '@/services/admin'
import { formatRelativeTime, formatText } from '@/utils/formatters'

const loading = ref(true)
const error = ref('')
const stats = ref<DashboardStats>({
  quotes: { pending: 0, in_review: 0, quoted: 0, total: 0 },
  claims: { submitted: 0, contacted: 0, closed: 0, total: 0 },
  messages: { new: 0, read: 0, responded: 0, closed: 0, total: 0 },
  users: { active: 0, inactive: 0, total: 0 },
  recent_activity: []
})
const attentionItems = ref<AttentionItem[]>([])

onMounted(async () => {
  try {
    const [statsData, attentionData] = await Promise.all([
      adminService.getDashboardStats(),
      adminService.getAttentionItems()
    ])
    stats.value = statsData
    attentionItems.value = attentionData
  } catch (err: any) {
    console.error('Error loading dashboard data:', err)
    error.value = 'Failed to load dashboard data'
  } finally {
    loading.value = false
  }
})

const recentActivity = computed(() => {
  return stats.value.recent_activity.slice(0, 10)
})

// Map priority to icon color for attention items
const getIconColor = (priority: string): string => {
  switch (priority) {
    case 'high':
      return 'red'
    case 'medium':
      return 'yellow'
    case 'low':
      return 'green'
    default:
      return 'blue'
  }
}

// Get icon for activity type
const getTypeIcon = (type: string): string => {
  const iconMap: Record<string, string> = {
    message: '✉️',
    claim: '🛡️',
    quote: '💬'
  }
  return iconMap[type.toLowerCase()] || '📄'
}

// Store referrer for back navigation
const storeReferrer = (item: AttentionItem) => {
  const referrerPath = '/admin'

  // Determine what kind of item this is and store appropriate referrer
  if (item.link.includes('/admin/quotes/')) {
    sessionStorage.setItem('quote_referrer', referrerPath)
  } else if (item.link.includes('/admin/claims/')) {
    sessionStorage.setItem('claim_referrer', referrerPath)
  } else if (item.link.includes('/admin/messages/')) {
    sessionStorage.setItem('message_referrer', referrerPath)
  } else if (item.link.includes('/admin/users/')) {
    sessionStorage.setItem('user_referrer', referrerPath)
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.admin-dashboard-content {
  width: 100%;
}

.top-bar {
  background: white;
  padding: 1.5rem 2rem;
  margin: -2rem -2rem 2rem -2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.top-bar h2 {
  font-size: 1.875rem;
  color: #1a202c;
  font-weight: 700;
}

.top-bar p {
  color: #718096;
  margin-top: 0.25rem;
}

/* Stats Cards */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.75rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.stat-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.stat-card-link:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.stat-card-link:active {
  transform: translateY(-2px);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-icon.blue {
  background: rgba(0, 61, 165, 0.1);
  color: var(--color-primary);
}

.stat-icon.yellow {
  background: rgba(255, 193, 7, 0.1);
  color: #f59e0b;
}

.stat-icon.green {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: #1a202c;
  line-height: 1;
}

.stat-label {
  color: #718096;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  font-weight: 500;
}

.stat-change {
  font-size: 0.875rem;
  margin-top: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  display: inline-block;
}

.stat-change.positive {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

/* Two-Column Layout for Activity Sections */
.activity-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

/* Activity Section */
.activity-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  max-height: 600px;
}

.section-header {
  padding: 1.75rem 2rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a202c;
}

.view-all {
  color: var(--color-primary);
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
}

.view-all:hover {
  text-decoration: underline;
}

.activity-list {
  padding: 0;
  overflow-y: auto;
  flex: 1;
}

.activity-item {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f7fafc;
  display: flex;
  gap: 1rem;
  align-items: center;
  transition: background-color 0.2s;
}

.activity-item:hover {
  background-color: #f7fafc;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 0.25rem;
}

.activity-meta {
  display: flex;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #718096;
}

/* Type Badge - Blue box with icon and white text */
.activity-type-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.875rem;
  background: var(--color-primary);
  color: white;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

.type-icon {
  font-size: 1rem;
  line-height: 1;
}

/* Items Requiring Attention Styles */
.attention-item {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f7fafc;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  transition: background-color 0.2s;
  text-decoration: none;
  color: inherit;
}

.attention-item:hover {
  background-color: #f7fafc;
  cursor: pointer;
}

.attention-item:last-child {
  border-bottom: none;
}

.attention-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.attention-icon-wrapper.yellow {
  background: rgba(255, 193, 7, 0.15);
}

.attention-icon-wrapper.blue {
  background: rgba(0, 61, 165, 0.15);
}

.attention-icon-wrapper.green {
  background: rgba(16, 185, 129, 0.15);
}

.attention-icon-wrapper.red {
  background: rgba(239, 68, 68, 0.15);
}

.attention-content {
  flex: 1;
}

.loading, .error-message {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
}

.empty-activity {
  padding: 3rem 2rem;
  text-align: center;
  color: #718096;
}

@media (max-width: 1200px) {
  .activity-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .activity-grid {
    grid-template-columns: 1fr;
  }

  .top-bar {
    padding: 1rem;
  }

  .top-bar h2 {
    font-size: 1.5rem;
  }
}
</style>
