<template>
  <AdminLayout>
    <div class="container">
      <!-- Page Header -->
      <div class="page-header">
        <h1>Contact Messages Management</h1>
        <p>View and respond to customer messages</p>
      </div>

      <!-- Filter Panel -->
      <div class="filter-panel">
        <div class="filters-row">
          <div class="filter-group">
            <label for="subject">Subject</label>
            <select id="subject" v-model="filters.subject" class="filter-dropdown">
              <option value="">All Subjects</option>
              <option value="general">💬 General Inquiry</option>
              <option value="quote">💰 Quote Request</option>
              <option value="claim">📋 Claim Question</option>
              <option value="policy">📄 Policy Question</option>
              <option value="other">❓ Other</option>
            </select>
          </div>

          <div class="filter-group">
            <label for="status">Status</label>
            <select id="status" v-model="filters.status" class="filter-dropdown">
              <option value="">All Statuses</option>
              <option value="new">New</option>
              <option value="read">Read</option>
              <option value="responded">Responded</option>
              <option value="closed">Closed</option>
            </select>
          </div>

          <div class="filter-group">
            <label for="guest">Message Type</label>
            <select id="guest" v-model="filters.include_guest" class="filter-dropdown">
              <option value="true">All Messages</option>
              <option value="false">Authenticated Only</option>
              <option value="guest_only">Guest Only</option>
            </select>
          </div>

          <div class="filter-group">
            <label for="search">Search</label>
            <input
              id="search"
              v-model="filters.search"
              type="text"
              placeholder="Name or email..."
              class="search-input"
            />
          </div>
        </div>

        <div class="filter-actions">
          <button @click="applyFilters" class="btn btn-primary">Apply Filters</button>
          <button @click="clearFilters" class="btn btn-secondary">Clear</button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>Loading messages...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <button @click="loadMessages" class="btn btn-primary">Retry</button>
      </div>

      <!-- Empty State -->
      <div v-else-if="messages.length === 0" class="empty-state">
        <p>No messages found.</p>
        <p v-if="hasActiveFilters" class="empty-hint">Try adjusting your filters.</p>
      </div>

      <!-- Messages List -->
      <div v-else>
        <!-- Messages Table (Desktop) -->
        <div class="messages-table-container desktop-only">
        <table class="messages-table">
          <thead>
            <tr>
              <th>Sender Name</th>
              <th>Subject</th>
              <th>Submitted</th>
              <th>Status</th>
              <th>Response</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="message in messages" :key="message.id" class="message-row">
              <td>
                <div class="customer-info">
                  <strong>{{ message.sender_name }}</strong>
                  <span class="customer-email">{{ message.sender_email }}</span>
                  <span v-if="message.is_guest" class="guest-badge">Guest</span>
                </div>
              </td>
              <td>
                <div class="subject-info">
                  <span class="subject-icon">{{ getSubjectIcon(message.subject) }}</span>
                  <span>{{ formatSubject(message.subject) }}</span>
                </div>
              </td>
              <td>{{ formatDate(message.created_at) }}</td>
              <td>
                <StatusBadge :status="message.status" />
              </td>
              <td>
                <span v-if="message.admin_response" class="has-response">✓ Yes</span>
                <span v-else class="no-response">—</span>
              </td>
              <td>
                <router-link :to="`/admin/messages/${message.id}`" class="btn btn-small">
                  View Details
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
        </div>

        <!-- Messages Cards (Mobile) -->
        <div class="messages-cards mobile-only">
        <div v-for="message in messages" :key="message.id" class="message-card">
          <div class="card-header">
            <div class="header-left">
              <span class="subject-icon">{{ getSubjectIcon(message.subject) }}</span>
              <div class="customer-info">
                <strong>{{ message.sender_name }}</strong>
                <span class="customer-email">{{ message.sender_email }}</span>
                <span v-if="message.is_guest" class="guest-badge">Guest</span>
              </div>
            </div>
            <StatusBadge :status="message.status" />
          </div>

          <div class="card-body">
            <div class="card-row">
              <span class="label">Subject:</span>
              <span class="value">{{ formatSubject(message.subject) }}</span>
            </div>
            <div class="card-row">
              <span class="label">Submitted:</span>
              <span class="value">{{ formatDate(message.created_at) }}</span>
            </div>
            <div class="card-row">
              <span class="label">Response:</span>
              <span v-if="message.admin_response" class="value has-response">✓ Yes</span>
              <span v-else class="value no-response">Not yet</span>
            </div>
          </div>

          <div class="card-actions">
            <router-link :to="`/admin/messages/${message.id}`" class="btn btn-primary btn-block">
              View Details
            </router-link>
          </div>
        </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="messages.length > 0" class="pagination">
        <p class="pagination-info">
          Showing {{ messages.length }} of {{ totalItems }} message{{ totalItems !== 1 ? 's' : '' }}
          <span v-if="totalPages > 1"> (Page {{ currentPage }} of {{ totalPages }})</span>
        </p>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import adminService, { type AdminMessage } from '@/services/admin'
import { formatDate as formatDateUtil } from '@/utils/formatters'

// Data
const messages = ref<AdminMessage[]>([])
const loading = ref(true)
const error = ref('')
const totalItems = ref(0)
const totalPages = ref(0)
const currentPage = ref(1)

// Filters
const filters = ref({
  subject: '',
  status: '',
  include_guest: 'true',
  search: ''
})

// Load messages on mount
onMounted(async () => {
  await loadMessages()
})

// Load messages from API
const loadMessages = async () => {
  loading.value = true
  error.value = ''

  try {
    const params: any = {}
    if (filters.value.subject) params.subject = filters.value.subject
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.search) params.search = filters.value.search

    // Handle guest filter
    if (filters.value.include_guest === 'true') {
      params.include_guest = true
    } else if (filters.value.include_guest === 'false') {
      params.include_guest = false
    }
    // If guest_only, we'll filter client-side after getting all guest messages

    const response = await adminService.getMessages(params)
    messages.value = response.items
    totalItems.value = response.total
    totalPages.value = response.pages
    currentPage.value = response.page

    // Client-side filter for guest_only
    if (filters.value.include_guest === 'guest_only') {
      messages.value = messages.value.filter(m => m.is_guest)
      totalItems.value = messages.value.length
    }
  } catch (err: any) {
    console.error('Error loading messages:', err)
    error.value = 'Failed to load messages. Please try again.'
  } finally {
    loading.value = false
  }
}

// Filter actions
const applyFilters = () => {
  loadMessages()
}

const clearFilters = () => {
  filters.value = {
    subject: '',
    status: '',
    include_guest: 'true',
    search: ''
  }
  loadMessages()
}

// Computed: Check if any filters are active
const hasActiveFilters = computed(() => {
  return !!(filters.value.subject || filters.value.status || filters.value.search || filters.value.include_guest !== 'true')
})

// Helpers: Subject icons
const getSubjectIcon = (subject: string): string => {
  const iconMap: Record<string, string> = {
    general: '💬',
    quote: '📋',
    claim: '🔔',
    policy: '📄',
    other: '❓'
  }
  return iconMap[subject] || '💬'
}

const formatSubject = (subject: string): string => {
  const subjectMap: Record<string, string> = {
    general: 'General Inquiry',
    quote: 'Quote Request',
    claim: 'Claim Question',
    policy: 'Policy Question',
    other: 'Other'
  }
  return subjectMap[subject] || subject.charAt(0).toUpperCase() + subject.slice(1)
}


const formatDate = formatDateUtil
</script>

<style scoped>
.admin-messages-page {
  min-height: calc(100vh - 200px);
  padding: 3rem 0;
  background: #f5f7fa;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  color: var(--color-primary);
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #666;
}

/* Filter Panel */
.filter-panel {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.filters-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.filter-dropdown,
.search-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d0d0d0;
  border-radius: 4px;
  background: white;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.filter-dropdown:hover,
.search-input:hover {
  border-color: var(--color-primary);
}

.filter-dropdown:focus,
.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 61, 165, 0.1);
}

.filter-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

/* States */
.loading,
.error-message,
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.empty-hint {
  font-size: 0.9rem;
  color: #999;
  margin-top: 0.5rem;
}

/* Desktop Table */
.desktop-only {
  display: block;
}

.mobile-only {
  display: none;
}

.messages-table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.messages-table {
  width: 100%;
  border-collapse: collapse;
}

.messages-table thead {
  background: var(--color-primary);
  border-bottom: 2px solid #e0e0e0;
}

.messages-table th {
  text-align: left;
  padding: 1rem;
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
  text-transform: uppercase;
}

.messages-table td {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  vertical-align: middle;
}

.message-row:hover {
  background: #f8f9fa;
}

.customer-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.customer-email {
  font-size: 0.875rem;
  color: #666;
}

.guest-badge {
  display: inline-block;
  padding: 0.125rem 0.5rem;
  background: #E2E3E5;
  color: #383D41;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 8px;
  text-transform: uppercase;
  width: fit-content;
  margin-top: 0.25rem;
}

.subject-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.subject-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.has-response {
  color: #155724;
  font-weight: 600;
}

.no-response {
  color: #999;
}

/* Buttons */
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--color-primary-dark);
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

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  font-weight: 600;
}

.btn-small:hover {
  background: var(--color-primary);
  color: white;
  transform: translateY(-1px);
}

.btn-block {
  width: 100%;
  text-align: center;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
}

.pagination-info {
  color: #666;
  font-size: 0.9rem;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .admin-messages-page {
    padding: 1.5rem 0;
  }

  .container {
    padding: 0 1rem;
  }

  .desktop-only {
    display: none !important;
  }

  .mobile-only {
    display: block !important;
  }

  .filters-row {
    grid-template-columns: 1fr;
  }

  .filter-actions {
    flex-direction: column;
  }

  .filter-actions .btn {
    width: 100%;
  }

  .messages-cards {
    display: grid;
    gap: 1rem;
  }

  .message-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 1rem;
    border-bottom: 1px solid #e0e0e0;
    gap: 1rem;
  }

  .header-left {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    flex: 1;
  }

  .header-left .subject-icon {
    font-size: 2rem;
    flex-shrink: 0;
  }

  .header-left .customer-info {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .card-body {
    padding: 1rem;
  }

  .card-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f0f0f0;
  }

  .card-row:last-child {
    border-bottom: none;
  }

  .card-row .label {
    font-size: 0.875rem;
    color: #666;
    font-weight: 500;
  }

  .card-row .value {
    font-weight: 600;
    color: #333;
    text-align: right;
  }

  .card-actions {
    padding: 1rem;
    border-top: 1px solid #e0e0e0;
    background: #f8f9fa;
  }
}
</style>
