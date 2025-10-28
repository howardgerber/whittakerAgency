<template>
  <AdminLayout>
    <div class="container">
      <!-- Page Header -->
      <div class="page-header">
        <h1>Claims Management</h1>
        <p>View and manage customer claim requests</p>
      </div>

      <!-- Filter Panel -->
      <div class="filter-panel">
        <div class="filters-row">
          <div class="filter-group">
            <label for="category">Category</label>
            <select id="category" v-model="filters.category" class="filter-dropdown">
              <option value="">All Categories</option>
              <option value="vehicle">🚗 Vehicle</option>
              <option value="property">🏠 Property</option>
              <option value="life">❤️ Life</option>
              <option value="business">💼 Business</option>
              <option value="identity_protection">🔒 Identity Protection</option>
              <option value="other">📋 Other</option>
            </select>
          </div>

          <div class="filter-group">
            <label for="subcategory">Subcategory</label>
            <select id="subcategory" v-model="filters.subcategory" class="filter-dropdown" :disabled="!filters.category">
              <option value="">All Subcategories</option>
              <option v-for="sub in availableSubcategories" :key="sub.value" :value="sub.value">
                {{ sub.label }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label for="status">Status</label>
            <select id="status" v-model="filters.status" class="filter-dropdown">
              <option value="">All Statuses</option>
              <option value="submitted">Submitted</option>
              <option value="contacted">Contacted</option>
              <option value="closed">Closed</option>
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
        <p>Loading claims...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <button @click="loadClaims" class="btn btn-primary">Retry</button>
      </div>

      <!-- Empty State -->
      <div v-else-if="claims.length === 0" class="empty-state">
        <p>No claim requests found.</p>
        <p v-if="hasActiveFilters" class="empty-hint">Try adjusting your filters.</p>
      </div>

      <!-- Claims List -->
      <div v-else>
        <!-- Claims Table (Desktop) -->
        <div class="claims-table-container desktop-only">
        <table class="claims-table">
          <thead>
            <tr>
              <th>Customer Name</th>
              <th>Insurance Type</th>
              <th>Incident Date</th>
              <th>Submitted</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="claim in claims" :key="claim.id" class="claim-row">
              <td>
                <div class="customer-info">
                  <strong>{{ claim.customer_name }}</strong>
                  <span class="customer-email">{{ claim.customer_email }}</span>
                </div>
              </td>
              <td>
                <div class="insurance-type">
                  <span class="category-icon">{{ getCategoryIcon(claim.category, claim.subcategory) }}</span>
                  <span>{{ getInsuranceName(claim.category, claim.subcategory) }}</span>
                </div>
              </td>
              <td>{{ formatDate(claim.incident_date) }}</td>
              <td>{{ formatDate(claim.created_at) }}</td>
              <td>
                <StatusBadge :status="claim.status" />
              </td>
              <td>
                <router-link :to="`/admin/claims/${claim.id}`" class="btn btn-small">
                  View Details
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
        </div>

        <!-- Claims Cards (Mobile) -->
        <div class="claims-cards mobile-only">
        <div v-for="claim in claims" :key="claim.id" class="claim-card">
          <div class="card-header">
            <div class="header-left">
              <span class="category-icon">{{ getCategoryIcon(claim.category, claim.subcategory) }}</span>
              <div class="customer-info">
                <strong>{{ claim.customer_name }}</strong>
                <span class="customer-email">{{ claim.customer_email }}</span>
              </div>
            </div>
            <StatusBadge :status="claim.status" />
          </div>

          <div class="card-body">
            <div class="card-row">
              <span class="label">Insurance Type:</span>
              <span class="value">{{ getInsuranceName(claim.category, claim.subcategory) }}</span>
            </div>
            <div class="card-row">
              <span class="label">Incident Date:</span>
              <span class="value">{{ formatDate(claim.incident_date) }}</span>
            </div>
            <div class="card-row">
              <span class="label">Submitted:</span>
              <span class="value">{{ formatDate(claim.created_at) }}</span>
            </div>
          </div>

          <div class="card-actions">
            <router-link :to="`/admin/claims/${claim.id}`" class="btn btn-primary btn-block">
              View Details
            </router-link>
          </div>
        </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="claims.length > 0" class="pagination">
        <p class="pagination-info">
          Showing {{ claims.length }} of {{ totalItems }} claim{{ totalItems !== 1 ? 's' : '' }}
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
import adminService, { type AdminClaim } from '@/services/admin'
import { formatDate as formatDateUtil } from '@/utils/formatters'

// Data
const claims = ref<AdminClaim[]>([])
const loading = ref(true)
const error = ref('')
const totalItems = ref(0)
const totalPages = ref(0)
const currentPage = ref(1)

// Filters
const filters = ref({
  category: '',
  subcategory: '',
  status: '',
  search: ''
})

// Load claims on mount
onMounted(async () => {
  await loadClaims()
})

// Load claims from API
const loadClaims = async () => {
  loading.value = true
  error.value = ''

  try {
    const params: any = {}
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.subcategory) params.subcategory = filters.value.subcategory
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.search) params.search = filters.value.search

    const response = await adminService.getClaims(params)
    claims.value = response.items
    totalItems.value = response.total
    totalPages.value = response.pages
    currentPage.value = response.page
  } catch (err: any) {
    console.error('Error loading claims:', err)
    error.value = 'Failed to load claims. Please try again.'
  } finally {
    loading.value = false
  }
}

// Filter actions
const applyFilters = () => {
  loadClaims()
}

const clearFilters = () => {
  filters.value = {
    category: '',
    subcategory: '',
    status: '',
    search: ''
  }
  loadClaims()
}

// Computed: Check if any filters are active
const hasActiveFilters = computed(() => {
  return !!(filters.value.category || filters.value.subcategory || filters.value.status || filters.value.search)
})

// Computed: Available subcategories based on selected category
const availableSubcategories = computed(() => {
  const subcategoryMap: Record<string, Array<{ value: string; label: string }>> = {
    vehicle: [
      { value: 'auto', label: 'Auto' },
      { value: 'motorcycle', label: 'Motorcycle' },
      { value: 'atv', label: 'ATV/Off-Road' },
      { value: 'boat', label: 'Boat' },
      { value: 'rv', label: 'RV' },
      { value: 'snowmobile', label: 'Snowmobile' },
      { value: 'roadside', label: 'Roadside Assistance' },
      { value: 'vehicle_protection', label: 'Vehicle Protection' }
    ],
    property: [
      { value: 'homeowners', label: 'Homeowners' },
      { value: 'renters', label: 'Renters' },
      { value: 'condo', label: 'Condo' },
      { value: 'landlord', label: 'Landlord' },
      { value: 'mobile_home', label: 'Mobile Home' }
    ],
    other: [
      { value: 'umbrella', label: 'Umbrella Policy' },
      { value: 'pet', label: 'Pet Insurance' },
      { value: 'travel', label: 'Travel Insurance' },
      { value: 'jewelry', label: 'Jewelry Insurance' },
      { value: 'collectibles', label: 'Collectibles Insurance' },
      { value: 'individual_health', label: 'Individual Health' },
      { value: 'event', label: 'Event Insurance' }
    ]
  }

  return subcategoryMap[filters.value.category] || []
})

// Helpers: Category icons
const getCategoryIcon = (category: string, subcategory: string | null): string => {
  const type = subcategory || category
  const iconMap: Record<string, string> = {
    vehicle: '🚗', property: '🏠', life: '❤️', business: '💼',
    identity_protection: '🔒', other: '📋',
    auto: '🚗', motorcycle: '🏍️', atv: '🛞', boat: '⛵', rv: '🚐',
    snowmobile: '🛷', roadside: '🚨', vehicle_protection: '🛡️',
    homeowners: '🏠', renters: '🏢', condo: '🏘️', landlord: '🏚️',
    mobile_home: '🚐', umbrella: '☂️', pet: '🐾', travel: '✈️',
    jewelry: '💎', collectibles: '🏺', individual_health: '🏥', event: '🎉'
  }
  return iconMap[type] || '📄'
}

const getInsuranceName = (category: string, subcategory: string | null): string => {
  if (subcategory) {
    const nameMap: Record<string, string> = {
      auto: 'Auto Insurance', motorcycle: 'Motorcycle Insurance',
      atv: 'ATV/Off-Road Insurance', boat: 'Boat Insurance', rv: 'RV Insurance',
      snowmobile: 'Snowmobile Insurance', roadside: 'Roadside Assistance',
      vehicle_protection: 'Vehicle Protection', homeowners: 'Homeowners Insurance',
      renters: 'Renters Insurance', condo: 'Condo Insurance',
      landlord: 'Landlord Insurance', mobile_home: 'Mobile Home Insurance',
      umbrella: 'Umbrella Policy', pet: 'Pet Insurance', travel: 'Travel Insurance',
      jewelry: 'Jewelry Insurance', collectibles: 'Collectibles Insurance',
      individual_health: 'Individual Health Insurance', event: 'Event Insurance'
    }
    return nameMap[subcategory] || `${subcategory.charAt(0).toUpperCase() + subcategory.slice(1)} Insurance`
  }

  const categoryNameMap: Record<string, string> = {
    life: 'Life Insurance', business: 'Business Insurance',
    identity_protection: 'Identity Protection'
  }
  return categoryNameMap[category] || `${category.charAt(0).toUpperCase() + category.slice(1)} Insurance`
}

const formatDate = formatDateUtil
</script>

<style scoped>
.admin-claims-page {
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

.filter-dropdown:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
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

.claims-table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.claims-table {
  width: 100%;
  border-collapse: collapse;
}

.claims-table thead {
  background: var(--color-primary);
  border-bottom: 2px solid #e0e0e0;
}

.claims-table th {
  text-align: left;
  padding: 1rem;
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
  text-transform: uppercase;
}

.claims-table td {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  vertical-align: middle;
}

.claim-row:hover {
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

.insurance-type {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.category-icon {
  font-size: 1.5rem;
  line-height: 1;
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
  .admin-claims-page {
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

  .claims-cards {
    display: grid;
    gap: 1rem;
  }

  .claim-card {
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

  .header-left .category-icon {
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
