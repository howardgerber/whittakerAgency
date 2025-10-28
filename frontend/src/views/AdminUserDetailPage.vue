<template>
  <AdminLayout>
    <div class="container">
      <!-- Back Button -->
      <div class="back-button-container">
        <a @click="goBack" class="back-button">
          ← Back
        </a>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>Loading user details...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <button @click="loadUserDetail" class="btn btn-primary">Retry</button>
      </div>

      <!-- User Details -->
      <div v-else-if="user" class="user-detail">
        <!-- User Information Card -->
        <div class="info-card">
          <h2 @click="toggleUserInfo" class="collapsible-header">
            <span class="collapse-icon">{{ isUserInfoExpanded ? '▼' : '▶' }}</span>
            User Information
          </h2>
          <div v-show="isUserInfoExpanded" class="info-grid">
            <div class="info-item">
              <span class="info-label">User ID</span>
              <span class="info-value">{{ user.id }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Username</span>
              <span class="info-value">{{ user.username }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Full Name</span>
              <span class="info-value">{{ user.full_name }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Email</span>
              <span class="info-value">{{ user.email }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Phone</span>
              <span class="info-value">{{ user.phone || 'Not provided' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Account Status</span>
              <span class="info-value">{{ user.is_active ? 'Active' : 'Inactive' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Admin Status</span>
              <span class="info-value">{{ user.is_admin ? 'Administrator' : 'Regular User' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Registration Date</span>
              <span class="info-value">{{ formatDate(user.created_at) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Last Updated</span>
              <span class="info-value">{{ formatDate(user.updated_at) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Last Login</span>
              <span class="info-value">{{ user.last_login_at ? formatDateTime(user.last_login_at) : 'Never' }}</span>
            </div>
          </div>
        </div>

        <!-- Activity Summary -->
        <div class="activity-summary">
          <div class="summary-header">
            <h2>Activity Summary</h2>
            <div class="time-filter">
              <select v-model="selectedTimeFilter" @change="onTimeFilterChange" class="time-filter-select">
                <option value="all">All</option>
                <option value="30days">Last 30 Days</option>
                <option value="6months">Last 6 Months</option>
                <option value="ytd">Year to Date</option>
                <option value="last_year">Last Year</option>
              </select>
            </div>
          </div>

          <!-- Summary Stats -->
          <div class="summary-stats">
            <div class="stat-card">
              <div class="stat-icon">📋</div>
              <div class="stat-info">
                <span class="stat-value">{{ user.quotes_count }}</span>
                <span class="stat-label">Quote Requests</span>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">🛡️</div>
              <div class="stat-info">
                <span class="stat-value">{{ user.claims_count }}</span>
                <span class="stat-label">Claims</span>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">💬</div>
              <div class="stat-info">
                <span class="stat-value">{{ user.messages_count }}</span>
                <span class="stat-label">Messages</span>
              </div>
            </div>
          </div>

          <!-- Activity Details -->
          <div class="activity-details">
            <!-- Quotes Section with FILTER MODAL -->
            <div class="activity-section">
              <div class="section-header-with-filter">
                <h3>Quotes ({{ filteredQuotes.length }} of {{ user.activity.quotes.length }})</h3>
                <div class="filter-button-wrapper">
                  <button @click="toggleQuotesFilterPopup" class="filter-icon-btn" :class="{ active: quotesStatusFilter || quotesCategoryFilter }">
                    🔍 Filter
                    <span v-if="quotesStatusFilter || quotesCategoryFilter" class="filter-badge">{{ activeQuotesFiltersCount }}</span>
                  </button>

                  <!-- Filter Modal Dropdown -->
                  <div v-if="showQuotesFilterPopup" class="filter-modal-dropdown" @click.stop>
                    <div class="filter-modal-header">
                      <h4>Filter Quotes</h4>
                      <button @click="showQuotesFilterPopup = false" class="close-btn">×</button>
                    </div>
                    <div class="filter-modal-body">
                      <div class="modal-filter-group">
                        <label>Category:</label>
                        <select v-model="quotesCategoryFilter" class="filter-select">
                          <option value="">All Categories</option>
                          <option v-for="cat in quotesCategories" :key="cat" :value="cat">
                            {{ formatText(cat) }}
                          </option>
                        </select>
                      </div>
                      <div class="modal-filter-group">
                        <label>Status:</label>
                        <select v-model="quotesStatusFilter" class="filter-select">
                          <option value="">All Statuses</option>
                          <option value="pending">Pending</option>
                          <option value="in_review">In Review</option>
                          <option value="quoted">Quoted</option>
                          <option value="accepted">Accepted</option>
                          <option value="declined">Declined</option>
                        </select>
                      </div>
                    </div>
                    <div class="filter-modal-footer">
                      <button @click="clearQuotesFilters" class="btn-modal-secondary">Clear All</button>
                      <button @click="showQuotesFilterPopup = false" class="btn-modal-primary">Apply</button>
                    </div>
                  </div>

                  <!-- Backdrop -->
                  <div v-if="showQuotesFilterPopup" class="filter-backdrop" @click="showQuotesFilterPopup = false"></div>
                </div>
              </div>

              <div v-if="filteredQuotes.length > 0" class="activity-table-container">
                <table class="activity-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Category</th>
                      <th>Status</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="quote in filteredQuotes"
                      :key="quote.id"
                      @click="navigateToQuote(quote.id)"
                      class="clickable-row"
                    >
                      <td>#{{ quote.id }}</td>
                      <td>{{ formatText(quote.category) }}</td>
                      <td>
                        <span :class="['status-badge', `status-${quote.status}`]">
                          {{ formatText(quote.status) }}
                        </span>
                      </td>
                      <td>{{ formatDate(quote.created_at) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="empty-activity">
                <p>{{ quotesStatusFilter || quotesCategoryFilter ? 'No quotes match the selected filters' : 'No quote requests yet' }}</p>
              </div>
            </div>

            <!-- Claims Section with FILTER MODAL -->
            <div class="activity-section">
              <div class="section-header-with-filter">
                <h3>Claims ({{ filteredClaims.length }} of {{ user.activity.claims.length }})</h3>
                <div class="filter-button-wrapper">
                  <button @click="toggleClaimsFilterPopup" class="filter-icon-btn" :class="{ active: claimsStatusFilter || claimsCategoryFilter }">
                    🔍 Filter
                    <span v-if="claimsStatusFilter || claimsCategoryFilter" class="filter-badge">{{ activeClaimsFiltersCount }}</span>
                  </button>

                  <!-- Filter Modal Dropdown -->
                  <div v-if="showClaimsFilterPopup" class="filter-modal-dropdown" @click.stop>
                    <div class="filter-modal-header">
                      <h4>Filter Claims</h4>
                      <button @click="showClaimsFilterPopup = false" class="close-btn">×</button>
                    </div>
                    <div class="filter-modal-body">
                      <div class="modal-filter-group">
                        <label>Category:</label>
                        <select v-model="claimsCategoryFilter" class="filter-select">
                          <option value="">All Categories</option>
                          <option v-for="cat in claimsCategories" :key="cat" :value="cat">
                            {{ formatText(cat) }}
                          </option>
                        </select>
                      </div>
                      <div class="modal-filter-group">
                        <label>Status:</label>
                        <select v-model="claimsStatusFilter" class="filter-select">
                          <option value="">All Statuses</option>
                          <option value="submitted">Submitted</option>
                          <option value="contacted">Contacted</option>
                          <option value="closed">Closed</option>
                        </select>
                      </div>
                    </div>
                    <div class="filter-modal-footer">
                      <button @click="clearClaimsFilters" class="btn-modal-secondary">Clear All</button>
                      <button @click="showClaimsFilterPopup = false" class="btn-modal-primary">Apply</button>
                    </div>
                  </div>

                  <!-- Backdrop -->
                  <div v-if="showClaimsFilterPopup" class="filter-backdrop" @click="showClaimsFilterPopup = false"></div>
                </div>
              </div>
              <div v-if="user.activity.claims.length > 0" class="activity-table-container">
                <table class="activity-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Category</th>
                      <th>Status</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="claim in filteredClaims"
                      :key="claim.id"
                      @click="navigateToClaim(claim.id)"
                      class="clickable-row"
                    >
                      <td>#{{ claim.id }}</td>
                      <td>{{ formatText(claim.category) }}</td>
                      <td>
                        <span :class="['status-badge', `status-${claim.status}`]">
                          {{ formatText(claim.status) }}
                        </span>
                      </td>
                      <td>{{ formatDate(claim.created_at) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="empty-activity">
                <p>{{ claimsStatusFilter || claimsCategoryFilter ? 'No claims match the selected filters' : 'No claims yet' }}</p>
              </div>
            </div>

            <!-- Messages Section with FILTER ICON POPUP -->
            <div class="activity-section">
              <div class="section-header-with-filter">
                <h3>Messages ({{ filteredMessages.length }} of {{ user.activity.messages.length }})</h3>
                <div class="filter-button-wrapper">
                  <button @click="toggleMessagesFilterPopup" class="filter-icon-btn" :class="{ active: messagesStatusFilter || messagesSubjectFilter }">
                    🔍 Filter
                    <span v-if="messagesStatusFilter || messagesSubjectFilter" class="filter-badge">{{ activeMessagesFiltersCount }}</span>
                  </button>

                  <!-- Filter Modal Dropdown (positioned below button) -->
                  <div v-if="showMessagesFilterPopup" class="filter-modal-dropdown" @click.stop>
                  <div class="filter-modal-header">
                    <h4>Filter Messages</h4>
                    <button @click="showMessagesFilterPopup = false" class="close-btn">×</button>
                  </div>
                  <div class="filter-modal-body">
                    <div class="modal-filter-group">
                      <label>Subject:</label>
                      <select v-model="messagesSubjectFilter" class="filter-select">
                        <option value="">All Subjects</option>
                        <option v-for="subj in messagesSubjects" :key="subj" :value="subj">
                          {{ formatText(subj) }}
                        </option>
                      </select>
                    </div>
                    <div class="modal-filter-group">
                      <label>Status:</label>
                      <select v-model="messagesStatusFilter" class="filter-select">
                        <option value="">All Statuses</option>
                        <option value="new">New</option>
                        <option value="read">Read</option>
                        <option value="responded">Responded</option>
                        <option value="closed">Closed</option>
                      </select>
                    </div>
                  </div>
                  <div class="filter-modal-footer">
                    <button @click="clearMessagesFilters" class="btn-modal-secondary">Clear All</button>
                    <button @click="showMessagesFilterPopup = false" class="btn-modal-primary">Apply</button>
                  </div>
                  </div>

                  <!-- Backdrop to close modal when clicking outside -->
                  <div v-if="showMessagesFilterPopup" class="filter-backdrop" @click="showMessagesFilterPopup = false"></div>
                </div>
              </div>

              <div v-if="filteredMessages.length > 0" class="activity-table-container">
                <table class="activity-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Subject</th>
                      <th>Status</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="message in filteredMessages"
                      :key="message.id"
                      @click="navigateToMessage(message.id)"
                      class="clickable-row"
                    >
                      <td>#{{ message.id }}</td>
                      <td class="subject-cell">{{ formatText(message.subject) }}</td>
                      <td>
                        <span :class="['status-badge', `status-${message.status}`]">
                          {{ formatText(message.status) }}
                        </span>
                      </td>
                      <td>{{ formatDate(message.created_at) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="empty-activity">
                <p>{{ messagesStatusFilter || messagesSubjectFilter ? 'No messages match the selected filters' : 'No messages yet' }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Admin Actions -->
        <div class="admin-actions-card">
          <h2>Admin Actions</h2>
          <div class="actions-content">
            <p class="actions-warning">
              {{ user.is_active ? 'Deactivating this account will prevent the user from logging in.' : 'Activating this account will allow the user to log in again.' }}
            </p>
            <button
              @click="toggleAccountStatus"
              :class="['btn', user.is_active ? 'btn-warning' : 'btn-success']"
              :disabled="actionLoading"
            >
              {{ actionLoading ? 'Processing...' : (user.is_active ? 'Deactivate Account' : 'Activate Account') }}
            </button>
          </div>
        </div>
      </div>

      <!-- Confirmation Dialog -->
      <div v-if="showConfirmDialog" class="modal-overlay" @click="showConfirmDialog = false">
        <div class="modal-content" @click.stop>
          <h3>Confirm Action</h3>
          <p>Are you sure you want to {{ user?.is_active ? 'deactivate' : 'activate' }} this user account?</p>
          <div class="modal-actions">
            <button @click="confirmToggleStatus" class="btn btn-primary">Confirm</button>
            <button @click="showConfirmDialog = false" class="btn btn-secondary">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import adminService, { type AdminUserDetail } from '@/services/admin'
import { formatDate as formatDateUtil, formatDateTime as formatDateTimeUtil, formatText } from '@/utils/formatters'

const route = useRoute()
const router = useRouter()

// Data
const user = ref<AdminUserDetail | null>(null)
const loading = ref(true)
const error = ref('')
const actionLoading = ref(false)
const showConfirmDialog = ref(false)
const isUserInfoExpanded = ref(false) // Start collapsed

// Time filter state (restored from sessionStorage)
const STORAGE_KEY = `admin_user_filters_${route.params.id}`
const selectedTimeFilter = ref<string>(loadFilter('timeFilter', 'all'))

// Quotes filter state (restored from sessionStorage)
const quotesStatusFilter = ref<string>(loadFilter('quotesStatus', ''))
const quotesCategoryFilter = ref<string>(loadFilter('quotesCategory', ''))

// Claims filter state (restored from sessionStorage)
const claimsStatusFilter = ref<string>(loadFilter('claimsStatus', ''))
const claimsCategoryFilter = ref<string>(loadFilter('claimsCategory', ''))

// Messages filter state (restored from sessionStorage)
const messagesStatusFilter = ref<string>(loadFilter('messagesStatus', ''))
const messagesSubjectFilter = ref<string>(loadFilter('messagesSubject', ''))
const showMessagesFilterPopup = ref(false)

// Modal popup states
const showQuotesFilterPopup = ref(false)
const showClaimsFilterPopup = ref(false)

// Load filter from sessionStorage
function loadFilter(key: string, defaultValue: string): string {
  try {
    const stored = sessionStorage.getItem(`${STORAGE_KEY}_${key}`)
    return stored !== null ? stored : defaultValue
  } catch {
    return defaultValue
  }
}

// Save filter to sessionStorage
function saveFilter(key: string, value: string) {
  try {
    sessionStorage.setItem(`${STORAGE_KEY}_${key}`, value)
  } catch {
    // Ignore storage errors
  }
}

// Watch for filter changes and persist them
watch(selectedTimeFilter, (val) => saveFilter('timeFilter', val))
watch(quotesStatusFilter, (val) => saveFilter('quotesStatus', val))
watch(quotesCategoryFilter, (val) => saveFilter('quotesCategory', val))
watch(claimsStatusFilter, (val) => saveFilter('claimsStatus', val))
watch(claimsCategoryFilter, (val) => saveFilter('claimsCategory', val))
watch(messagesStatusFilter, (val) => saveFilter('messagesStatus', val))
watch(messagesSubjectFilter, (val) => saveFilter('messagesSubject', val))

// Load user detail on mount
onMounted(async () => {
  await loadUserDetail()
})

// Load user detail from API
const loadUserDetail = async () => {
  loading.value = true
  error.value = ''

  try {
    const userId = parseInt(route.params.id as string, 10)
    const dateRange = selectedTimeFilter.value !== 'all' ? selectedTimeFilter.value : undefined
    user.value = await adminService.getUserDetail(userId, dateRange)
  } catch (err: any) {
    console.error('Error loading user detail:', err)
    error.value = 'Failed to load user details. Please try again.'
  } finally {
    loading.value = false
  }
}

// Time filter change handler
const onTimeFilterChange = async () => {
  await loadUserDetail()
}

// Toggle user info section
const toggleUserInfo = () => {
  isUserInfoExpanded.value = !isUserInfoExpanded.value
}

// Go back to referrer or default to user list
const goBack = () => {
  const referrer = sessionStorage.getItem('user_referrer')
  if (referrer) {
    sessionStorage.removeItem('user_referrer')
    router.push(referrer)
  } else {
    router.push('/admin/users')
  }
}

// Toggle account status
const toggleAccountStatus = () => {
  showConfirmDialog.value = true
}

const confirmToggleStatus = async () => {
  if (!user.value) return

  actionLoading.value = true
  showConfirmDialog.value = false

  try {
    const updatedUser = await adminService.updateUser(user.value.id, {
      is_active: !user.value.is_active
    })
    user.value = updatedUser
  } catch (err: any) {
    console.error('Error updating user status:', err)
    error.value = 'Failed to update user status. Please try again.'
  } finally {
    actionLoading.value = false
  }
}


// Computed: Get unique categories from quotes
const quotesCategories = computed(() => {
  if (!user.value) return []
  const categories = user.value.activity.quotes.map(q => q.category)
  return [...new Set(categories)].sort()
})

// Computed: Get unique categories from claims
const claimsCategories = computed(() => {
  if (!user.value) return []
  const categories = user.value.activity.claims.map(c => c.category)
  return [...new Set(categories)].sort()
})

// Computed: Get unique subjects from messages
const messagesSubjects = computed(() => {
  if (!user.value) return []
  const subjects = user.value.activity.messages.map(m => m.subject)
  return [...new Set(subjects)].sort()
})

// Computed: Filtered quotes
const filteredQuotes = computed(() => {
  if (!user.value) return []
  let quotes = user.value.activity.quotes

  if (quotesStatusFilter.value) {
    quotes = quotes.filter(q => q.status === quotesStatusFilter.value)
  }

  if (quotesCategoryFilter.value) {
    quotes = quotes.filter(q => q.category === quotesCategoryFilter.value)
  }

  return quotes
})

// Computed: Filtered claims
const filteredClaims = computed(() => {
  if (!user.value) return []
  let claims = user.value.activity.claims

  if (claimsStatusFilter.value) {
    claims = claims.filter(c => c.status === claimsStatusFilter.value)
  }

  if (claimsCategoryFilter.value) {
    claims = claims.filter(c => c.category === claimsCategoryFilter.value)
  }

  return claims
})

// Computed: Filtered messages
const filteredMessages = computed(() => {
  if (!user.value) return []
  let messages = user.value.activity.messages

  if (messagesStatusFilter.value) {
    messages = messages.filter(m => m.status === messagesStatusFilter.value)
  }

  if (messagesSubjectFilter.value) {
    messages = messages.filter(m => m.subject === messagesSubjectFilter.value)
  }

  return messages
})

// Computed: Count of active filters on quotes
const activeQuotesFiltersCount = computed(() => {
  let count = 0
  if (quotesStatusFilter.value) count++
  if (quotesCategoryFilter.value) count++
  return count
})

// Computed: Count of active filters on claims
const activeClaimsFiltersCount = computed(() => {
  let count = 0
  if (claimsStatusFilter.value) count++
  if (claimsCategoryFilter.value) count++
  return count
})

// Computed: Count of active filters on messages
const activeMessagesFiltersCount = computed(() => {
  let count = 0
  if (messagesStatusFilter.value) count++
  if (messagesSubjectFilter.value) count++
  return count
})

// Clear quotes filters
const clearQuotesFilters = () => {
  quotesStatusFilter.value = ''
  quotesCategoryFilter.value = ''
}

// Clear claims filters
const clearClaimsFilters = () => {
  claimsStatusFilter.value = ''
  claimsCategoryFilter.value = ''
}

// Clear messages filters
const clearMessagesFilters = () => {
  messagesStatusFilter.value = ''
  messagesSubjectFilter.value = ''
}

// Toggle quotes filter popup
const toggleQuotesFilterPopup = () => {
  showQuotesFilterPopup.value = !showQuotesFilterPopup.value
}

// Toggle claims filter popup
const toggleClaimsFilterPopup = () => {
  showClaimsFilterPopup.value = !showClaimsFilterPopup.value
}

// Toggle messages filter popup
const toggleMessagesFilterPopup = () => {
  showMessagesFilterPopup.value = !showMessagesFilterPopup.value
}

// Navigation functions - store referrer in sessionStorage so detail pages can navigate back
const navigateToQuote = (quoteId: number) => {
  sessionStorage.setItem('quote_referrer', route.fullPath)
  router.push(`/admin/quotes/${quoteId}`)
}

const navigateToClaim = (claimId: number) => {
  sessionStorage.setItem('claim_referrer', route.fullPath)
  router.push(`/admin/claims/${claimId}`)
}

const navigateToMessage = (messageId: number) => {
  sessionStorage.setItem('message_referrer', route.fullPath)
  router.push(`/admin/messages/${messageId}`)
}

const formatDate = formatDateUtil
const formatDateTime = formatDateTimeUtil
</script>

<style scoped>
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.back-button-container {
  margin-bottom: 1.5rem;
}

.back-button {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  transition: color 0.2s;
  cursor: pointer;
}

.back-button:hover {
  color: var(--color-primary-dark);
}

/* States */
.loading,
.error-message {
  text-align: center;
  padding: 3rem;
  color: #666;
}

/* Info Card */
.info-card {
  background: white;
  padding: 0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  overflow: hidden;
}

.info-card h2 {
  background: var(--color-primary);
  color: white;
  margin: 0;
  padding: 1.25rem 1.5rem;
  font-size: 1.25rem;
  font-weight: 600;
}

.collapsible-header {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  user-select: none;
  transition: background-color 0.2s;
}

.collapsible-header:hover {
  background: var(--color-primary-dark);
}

.collapse-icon {
  font-size: 0.875rem;
  display: inline-block;
  transition: transform 0.2s;
}

.info-card .info-grid {
  padding: 2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-label {
  font-size: 0.875rem;
  color: #666;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 1rem;
  color: #333;
  font-weight: 600;
}

/* Activity Summary */
.activity-summary {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.activity-summary h2 {
  color: var(--color-primary);
  margin: 0;
  font-size: 1.5rem;
}

.time-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.time-filter-select {
  padding: 0.5rem 1rem;
  border: 2px solid var(--color-primary);
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-primary);
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.time-filter-select:hover {
  background: var(--color-primary);
  color: white;
}

.time-filter-select:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-icon {
  font-size: 2.5rem;
  line-height: 1;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-primary);
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.25rem;
}

/* Activity Details */
.activity-details {
  display: grid;
  gap: 2rem;
  margin-bottom: 2rem;
}

.activity-section h3 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.activity-table-container {
  overflow-x: auto;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
}

.activity-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

/* Column widths for all activity tables */
.activity-table th:nth-child(1),
.activity-table td:nth-child(1) {
  width: 80px;
}

.activity-table th:nth-child(2),
.activity-table td:nth-child(2) {
  width: auto;
}

.activity-table th:nth-child(3),
.activity-table td:nth-child(3) {
  width: 150px;
}

.activity-table th:nth-child(4),
.activity-table td:nth-child(4) {
  width: 200px;
}

.activity-table thead {
  background: var(--color-primary);
  border-bottom: 2px solid var(--color-primary-dark);
}

.activity-table th {
  text-align: left;
  padding: 0.75rem 1rem;
  font-weight: 600;
  color: white;
  font-size: 0.875rem;
  text-transform: uppercase;
}

.activity-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.activity-table tbody tr:last-child td {
  border-bottom: none;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.clickable-row:hover {
  background: #f8f9fa;
}

.activity-table tbody tr:hover {
  background: #f8f9fa;
}

.table-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
}

.table-link:hover {
  text-decoration: underline;
}

.subject-cell {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  display: inline-block;
}

.status-pending {
  background: #FFF3CD;
  color: #856404;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
}

.status-in_review, .status-read {
  background: #CCE5FF;
  color: #004085;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
}

.status-quoted, .status-responded {
  background: #D4EDDA;
  color: #155724;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
}

.status-accepted {
  background: #C3E6CB;
  color: #0F5132;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
}

.status-declined, .status-closed {
  background: #F8D7DA;
  color: #721C24;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
}

.status-submitted, .status-new {
  background: #FFF3CD;
  color: #856404;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
}

.status-contacted {
  background: #CCE5FF;
  color: #004085;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
}

.empty-activity {
  text-align: center;
  padding: 2rem;
  color: #999;
  background: #f8f9fa;
  border-radius: 6px;
}

/* Filter Styles */

/* STYLE 1: Dropdowns Above Table (Quotes) */
.filters-above-table {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: #666;
  font-size: 0.9rem;
}

.filter-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  background: white;
  cursor: pointer;
  min-width: 150px;
}

.filter-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.15);
}

.btn-clear-filters {
  padding: 0.5rem 1rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-clear-filters:hover {
  background: #c82333;
}

.btn-clear-filters-small {
  padding: 0.4rem 0.8rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-clear-filters-small:hover {
  background: #c82333;
}

/* STYLE 2: Inline Header Filters (Claims) */
.activity-table-with-filters thead .filter-row {
  background: #f0f0f0;
}

.activity-table-with-filters thead .filter-row th {
  padding: 0.5rem 1rem;
  background: none;
}

.inline-filter {
  width: 100%;
  padding: 0.4rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
  background: white;
  cursor: pointer;
}

.inline-filter:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.15);
}

/* STYLE 3: Filter Icon Popup (Messages) */
.section-header-with-filter {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header-with-filter h3 {
  margin: 0;
}

.filter-button-wrapper {
  position: relative;
}

.filter-icon-btn {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 2px solid var(--color-primary);
  border-radius: 4px;
  color: var(--color-primary);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-icon-btn:hover {
  background: var(--color-primary);
  color: white;
}

.filter-icon-btn.active {
  background: var(--color-primary);
  color: white;
}

.filter-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 0.4rem;
  background: #dc3545;
  color: white;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 700;
}

/* Filter Modal - Dropdown positioned below button */
.filter-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 999;
}

.filter-modal-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: white;
  border: 2px solid var(--color-primary);
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  width: auto;
  min-width: 320px;
  max-width: 400px;
  z-index: 1000;
}

.filter-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e0e0e0;
  background: var(--color-primary);
}

.filter-modal-header h4 {
  margin: 0;
  color: white;
  font-size: 1rem;
}

.filter-modal-header .close-btn {
  color: white;
}

.filter-modal-header .close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e0e0e0;
  color: #333;
}

.filter-modal-body {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.modal-filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.modal-filter-group label {
  font-weight: 600;
  color: #666;
  font-size: 0.85rem;
}

.filter-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-top: 1px solid #e0e0e0;
  background: #f8f9fa;
}

.btn-modal-primary {
  padding: 0.5rem 1rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-modal-primary:hover {
  background: var(--color-primary-dark);
}

.btn-modal-secondary {
  padding: 0.5rem 1rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-modal-secondary:hover {
  background: var(--color-primary-dark);
}

/* Admin Actions */
.admin-actions-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.admin-actions-card h2 {
  color: var(--color-primary);
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.actions-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.actions-warning {
  color: #666;
  font-size: 0.95rem;
  padding: 1rem;
  background: #FFF3CD;
  border-radius: 6px;
  border-left: 4px solid #ffc107;
}

/* Buttons */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
  font-size: 1rem;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary);
  color: white;
  transform: translateY(-1px);
}

.btn-secondary {
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

.btn-secondary:hover {
  background: var(--color-primary);
  color: white;
}

.btn-warning {
  background: #dc3545;
  color: white;
}

.btn-warning:hover:not(:disabled) {
  background: #c82333;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #218838;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
  color: var(--color-primary);
  margin-bottom: 1rem;
}

.modal-content p {
  color: #666;
  margin-bottom: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .page-header {
    padding: 1.5rem;
  }

  .header-left {
    flex-direction: column;
    align-items: flex-start;
  }

  .user-avatar-large {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }

  .title-row h1 {
    font-size: 1.5rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .summary-stats {
    grid-template-columns: 1fr;
  }

  .activity-table-container {
    overflow-x: scroll;
  }

  .activity-table {
    min-width: 600px;
  }

  .modal-content {
    margin: 1rem;
  }
}
</style>
