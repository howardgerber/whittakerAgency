<template>
  <AdminLayout>
    <div class="container">
      <!-- Page Header -->
      <div class="page-header">
        <h1>User Management</h1>
        <p>View and manage user accounts</p>
      </div>

      <!-- Filter Panel -->
      <div class="filter-panel">
        <div class="filters-row">
          <div class="filter-group">
            <label for="search">Search</label>
            <input
              id="search"
              v-model="filters.search"
              type="text"
              placeholder="Username, email, or name..."
              class="search-input"
            />
          </div>

          <div class="filter-group">
            <label for="recently-contacted">Recently Contacted</label>
            <select id="recently-contacted" v-model="filters.recentlyContacted" class="filter-dropdown">
              <option value="">All</option>
              <option value="2weeks">2 Weeks</option>
              <option value="1month">1 Month</option>
              <option value="3months">3 Months</option>
              <option value="6months">6 Months</option>
              <option value="1year">1 Year</option>
            </select>
          </div>

          <div class="filter-group">
            <label for="sort">Sort By</label>
            <select id="sort" v-model="filters.sortBy" class="filter-dropdown">
              <option value="newest">Most Recent Activity</option>
              <option value="oldest">Least Recent Activity</option>
              <option value="name_asc">Name A-Z</option>
              <option value="name_desc">Name Z-A</option>
            </select>
          </div>
        </div>

        <div class="filter-actions">
          <button @click="applyFilters" class="btn btn-primary">Apply Filters</button>
          <button @click="clearFilters" class="btn btn-secondary">Clear</button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>Loading users...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <button @click="loadUsers" class="btn btn-primary">Retry</button>
      </div>

      <!-- Empty State -->
      <div v-else-if="users.length === 0" class="empty-state">
        <p>No users found.</p>
        <p v-if="hasActiveFilters" class="empty-hint">Try adjusting your filters.</p>
      </div>

      <!-- Users Table -->
      <div v-else class="users-table-container">
        <table class="users-table">
          <thead>
            <tr>
              <th>User</th>
              <th>Email</th>
              <th>Phone</th>
              <th class="center">Quotes</th>
              <th class="center">Claims</th>
              <th class="center">Messages</th>
              <th>Registered</th>
              <th>Last Login</th>
              <th class="center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id" class="user-row">
              <td>
                <div class="user-cell">
                  <div class="user-avatar-small">
                    {{ getInitials(user.full_name) }}
                  </div>
                  <div class="user-info-compact">
                    <div class="user-name-compact">
                      {{ user.full_name }}
                      <span v-if="user.is_admin" class="admin-badge-small">Admin</span>
                    </div>
                    <div class="user-username-compact">@{{ user.username }}</div>
                  </div>
                </div>
              </td>
              <td>{{ user.email }}</td>
              <td>{{ user.phone ? formatPhone(user.phone) : '-' }}</td>
              <td class="center stat-cell">{{ user.quotes_count }}</td>
              <td class="center stat-cell">{{ user.claims_count }}</td>
              <td class="center stat-cell">{{ user.messages_count }}</td>
              <td>{{ formatDate(user.created_at) }}</td>
              <td>{{ user.last_login_at ? formatDateTime(user.last_login_at) : 'Never' }}</td>
              <td class="center">
                <router-link :to="`/admin/users/${user.id}`" class="btn-view-details">
                  View Details
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="users.length > 0" class="pagination">
        <p class="pagination-info">
          Showing {{ users.length }} of {{ totalItems }} user{{ totalItems !== 1 ? 's' : '' }}
          <span v-if="totalPages > 1"> (Page {{ currentPage }} of {{ totalPages }})</span>
        </p>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import adminService, { type AdminUser } from '@/services/admin'
import { formatDate as formatDateUtil, formatDateTime as formatDateTimeUtil } from '@/utils/formatters'

// Data
const users = ref<AdminUser[]>([])
const loading = ref(true)
const error = ref('')
const totalItems = ref(0)
const totalPages = ref(0)
const currentPage = ref(1)

// Filters
const filters = ref({
  search: '',
  recentlyContacted: '',
  sortBy: 'newest'
})

// Load users on mount
onMounted(async () => {
  await loadUsers()
})

// Load users from API
const loadUsers = async () => {
  loading.value = true
  error.value = ''

  try {
    const params: any = {}
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.recentlyContacted) params.recently_contacted = filters.value.recentlyContacted

    // Map sort options to backend format
    const sortMap: Record<string, { sort_by: string; sort_order: string }> = {
      newest: { sort_by: 'activity', sort_order: 'desc' },
      oldest: { sort_by: 'activity', sort_order: 'asc' },
      name_asc: { sort_by: 'name', sort_order: 'asc' },
      name_desc: { sort_by: 'name', sort_order: 'desc' }
    }
    const sortConfig = sortMap[filters.value.sortBy]
    params.sort_by = sortConfig.sort_by
    params.sort_order = sortConfig.sort_order

    const response = await adminService.getUsers(params)
    users.value = response.items
    totalItems.value = response.total
    totalPages.value = response.pages
    currentPage.value = response.page
  } catch (err: any) {
    console.error('Error loading users:', err)
    error.value = 'Failed to load users. Please try again.'
  } finally {
    loading.value = false
  }
}

// Filter actions
const applyFilters = () => {
  loadUsers()
}

const clearFilters = () => {
  filters.value = {
    search: '',
    recentlyContacted: '',
    sortBy: 'newest'
  }
  loadUsers()
}

// Computed: Check if any filters are active
const hasActiveFilters = computed(() => {
  return !!(filters.value.search || filters.value.recentlyContacted)
})

// Helper: Get initials from full name
const getInitials = (fullName: string): string => {
  const names = fullName.trim().split(' ')
  if (names.length === 1) {
    return names[0].substring(0, 2).toUpperCase()
  }
  return (names[0][0] + names[names.length - 1][0]).toUpperCase()
}

// Helper: Format phone number
const formatPhone = (phone: string): string => {
  // Assuming backend returns XXX.XXX.XXXX format
  return phone
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

/* Users Table */
.users-table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
  margin-bottom: 2rem;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table thead {
  background: var(--color-primary);
  border-bottom: 2px solid #e0e0e0;
}

.users-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.875rem;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.users-table th.center {
  text-align: center;
}

.users-table tbody tr {
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s;
}

.users-table tbody tr:hover {
  background-color: #f8f9fa;
}

.users-table tbody tr:last-child {
  border-bottom: none;
}

.users-table td {
  padding: 1rem;
  font-size: 0.875rem;
  color: #333;
  vertical-align: middle;
}

.users-table td.center {
  text-align: center;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar-small {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), #0056d9);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.user-info-compact {
  min-width: 0;
}

.user-name-compact {
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.125rem;
}

.user-username-compact {
  font-size: 0.8rem;
  color: #666;
}

.admin-badge-small {
  padding: 0.125rem 0.5rem;
  background: #ffc107;
  color: #333;
  border-radius: 4px;
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: uppercase;
}

.stat-cell {
  font-weight: 600;
  color: var(--color-primary);
  font-size: 1rem;
}

.btn-view-details {
  padding: 0.5rem 1rem;
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.2s;
  display: inline-block;
}

.btn-view-details:hover {
  background: var(--color-primary);
  color: white;
  transform: translateY(-1px);
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
  .container {
    padding: 0 1rem;
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

  /* Make table scrollable on mobile */
  .users-table-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .users-table {
    min-width: 800px;
  }

  .users-table th,
  .users-table td {
    padding: 0.75rem 0.5rem;
    font-size: 0.8rem;
  }

  .user-avatar-small {
    width: 32px;
    height: 32px;
    font-size: 0.75rem;
  }
}
</style>
