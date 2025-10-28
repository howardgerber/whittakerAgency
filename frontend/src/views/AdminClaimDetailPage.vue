<template>
  <AdminLayout>
    <div class="container">
      <!-- Back Button -->
      <div class="back-button-wrapper">
        <a @click="goBack" class="back-link" style="cursor: pointer;">
          ← Back
        </a>
      </div>

      <!-- Page Header -->
      <div class="page-header">
        <h1>Claim Details</h1>
        <StatusBadge v-if="claim" :status="claim.status" />
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>Loading claim details...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <button @click="loadClaim" class="btn btn-primary">Retry</button>
      </div>

      <!-- Claim Details -->
      <div v-else-if="claim" class="detail-layout">
        <!-- Left Column: Readonly Information -->
        <div class="info-section">
          <!-- Customer Information -->
          <div class="info-card">
            <h2>Customer Information</h2>
            <div class="info-row">
              <span class="label">Name:</span>
              <span class="value">{{ claim.customer_name }}</span>
            </div>
            <div class="info-row">
              <span class="label">Email:</span>
              <span class="value">{{ claim.customer_email }}</span>
            </div>
            <div class="info-row" v-if="claim.customer_phone">
              <span class="label">Phone:</span>
              <span class="value">{{ claim.customer_phone }}</span>
            </div>
            <div class="info-row">
              <span class="label">Insurance Type:</span>
              <span class="value">{{ getInsuranceName(claim.category, claim.subcategory) }}</span>
            </div>
            <div class="info-row">
              <span class="label">Incident Date:</span>
              <span class="value">{{ formatDate(claim.incident_date) }}</span>
            </div>
            <div class="info-row">
              <span class="label">Submitted:</span>
              <span class="value">{{ formatDateTime(claim.created_at) }}</span>
            </div>
            <div class="info-row" v-if="claim.updated_at !== claim.created_at">
              <span class="label">Last Updated:</span>
              <span class="value">{{ formatDateTime(claim.updated_at) }}</span>
            </div>
          </div>

          <!-- Claim Data (Dynamic Fields) -->
          <div class="info-card" v-if="Object.keys(claim.claim_data).length > 0">
            <h2>Claim Details</h2>
            <div class="info-row" v-for="(value, key) in claim.claim_data" :key="key">
              <span class="label">{{ formatFieldName(key) }}:</span>
              <span class="value">{{ formatFieldValue(value) }}</span>
            </div>
          </div>
        </div>

        <!-- Right Column: Editable Admin Section -->
        <div class="edit-section">
          <div class="edit-card">
            <h2>Admin Actions</h2>

            <form @submit.prevent="saveChanges">
              <!-- Status -->
              <div class="form-group">
                <label for="status">Status</label>
                <select id="status" v-model="formData.status" class="form-control">
                  <option value="submitted">Submitted</option>
                  <option value="contacted">Contacted</option>
                  <option value="closed">Closed</option>
                </select>
              </div>

              <!-- Appointment Date -->
              <div class="form-group">
                <label for="appointment_requested">Appointment Date (Optional)</label>
                <input
                  id="appointment_requested"
                  v-model="formData.appointment_requested"
                  type="date"
                  class="form-control"
                />
              </div>

              <!-- Admin Notes -->
              <div class="form-group">
                <label for="admin_notes">Admin Notes</label>
                <textarea
                  id="admin_notes"
                  v-model="formData.admin_notes"
                  class="form-control"
                  rows="6"
                  placeholder="Add internal notes about this claim..."
                ></textarea>
              </div>

              <!-- Save Button -->
              <div class="form-actions">
                <button type="submit" class="btn btn-primary btn-block" :disabled="saving || !hasChanges">
                  {{ saving ? 'Saving...' : 'Save Changes' }}
                </button>

                <!-- Success Message -->
                <div v-if="successMessage" class="success-message">
                  {{ successMessage }}
                </div>

                <!-- Save Error -->
                <div v-if="saveError" class="error-message">
                  {{ saveError }}
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminLayout from '@/components/admin/AdminLayout.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import adminService, { type AdminClaim } from '@/services/admin'
import { formatDate, formatDateTime } from '@/utils/formatters'

// Route and data
const route = useRoute()
const router = useRouter()
const id = Number(route.params.id)

const claim = ref<AdminClaim | null>(null)
const loading = ref(true)
const error = ref('')
const saving = ref(false)
const successMessage = ref('')
const saveError = ref('')

// Form data
const formData = ref({
  status: '',
  appointment_requested: '',
  admin_notes: ''
})

// Original data to track changes
const originalData = ref({
  status: '',
  appointment_requested: '',
  admin_notes: ''
})

// Check if form has changes
const hasChanges = computed(() => {
  return formData.value.status !== originalData.value.status ||
         formData.value.appointment_requested !== originalData.value.appointment_requested ||
         formData.value.admin_notes !== originalData.value.admin_notes
})

// Load claim on mount
onMounted(async () => {
  await loadClaim()
})

// Load claim from API
const loadClaim = async () => {
  loading.value = true
  error.value = ''

  try {
    claim.value = await adminService.getClaim(id)

    // Initialize form data with current values
    formData.value = {
      status: claim.value.status,
      appointment_requested: claim.value.appointment_requested || '',
      admin_notes: claim.value.admin_notes || ''
    }

    // Store original values for change detection
    originalData.value = {
      status: claim.value.status,
      appointment_requested: claim.value.appointment_requested || '',
      admin_notes: claim.value.admin_notes || ''
    }
  } catch (err: any) {
    console.error('Error loading claim:', err)
    error.value = 'Failed to load claim details. Please try again.'
  } finally {
    loading.value = false
  }
}

// Save changes
const saveChanges = async () => {
  if (!claim.value) return

  saving.value = true
  saveError.value = ''
  successMessage.value = ''

  try {
    const updateData: any = {
      status: formData.value.status
    }

    // Only include appointment_requested if it has a value
    if (formData.value.appointment_requested) {
      updateData.appointment_requested = formData.value.appointment_requested
    }

    // Only include admin_notes if it's not empty
    if (formData.value.admin_notes.trim()) {
      updateData.admin_notes = formData.value.admin_notes.trim()
    }

    claim.value = await adminService.updateClaim(id, updateData)
    successMessage.value = 'Changes saved successfully!'

    // Update original data after successful save
    originalData.value = {
      status: claim.value.status,
      appointment_requested: claim.value.appointment_requested || '',
      admin_notes: claim.value.admin_notes || ''
    }

    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (err: any) {
    console.error('Error saving claim:', err)
    saveError.value = 'Failed to save changes. Please try again.'
  } finally {
    saving.value = false
  }
}

// Format field name (convert snake_case to Title Case)
const formatFieldName = (key: string): string => {
  return key
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

// Format field value
const formatFieldValue = (value: any): string => {
  if (value === null || value === undefined) return '—'
  if (typeof value === 'boolean') return value ? 'Yes' : 'No'
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}

// Format status

// Navigate back to referrer or default to claims list
const goBack = () => {
  const referrer = sessionStorage.getItem('claim_referrer')
  if (referrer) {
    sessionStorage.removeItem('claim_referrer')
    router.push(referrer)
  } else {
    router.push('/admin/claims')
  }
}

// Get insurance name
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
</script>

<style scoped>
.admin-claim-detail-page {
  min-height: calc(100vh - 200px);
  padding: 3rem 0;
  background: #f5f7fa;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.back-button-wrapper {
  margin-bottom: 1.5rem;
}

.back-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  transition: color 0.2s;
}

.back-link:hover {
  color: var(--color-primary-dark);
}

.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.page-header h1 {
  color: var(--color-primary);
  margin: 0;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-submitted {
  background: #FFF3CD;
  color: #856404;
}

.status-contacted {
  background: #CCE5FF;
  color: #004085;
}

.status-closed {
  background: #D4EDDA;
  color: #155724;
}

/* Loading/Error States */
.loading,
.error-message {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.error-message {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Layout */
.detail-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
}

/* Info Cards */
.info-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0;
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.info-card h2 {
  background: var(--color-primary);
  color: white;
  font-size: 1.25rem;
  margin: 0;
  padding: 1.25rem 1.5rem;
  font-weight: 600;
}

.info-card .info-row,
.info-card .notes-content {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

.info-card .info-row:first-of-type {
  padding-top: 1.5rem;
}

.info-card .notes-content {
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-row:last-child {
  border-bottom: none;
}

.info-row .label {
  font-weight: 600;
  color: #666;
  flex-shrink: 0;
  margin-right: 1rem;
}

.info-row .value {
  color: #333;
  text-align: right;
  word-break: break-word;
}

/* Edit Card */
.edit-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0;
  position: sticky;
  top: 2rem;
  overflow: hidden;
}

.edit-card h2 {
  background: var(--color-primary);
  color: white;
  font-size: 1.25rem;
  margin: 0;
  padding: 1.25rem 1.5rem;
  font-weight: 600;
}

.edit-card .form-group,
.edit-card .form-actions {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

.edit-card .form-group:first-of-type {
  padding-top: 1.5rem;
}

.edit-card .form-actions {
  padding-bottom: 1.5rem;
}

/* Form Styles */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d0d0d0;
  border-radius: 4px;
  font-size: 1rem;
  transition: all 0.2s;
  font-family: inherit;
}

.form-control:hover {
  border-color: var(--color-primary);
}

.form-control:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 61, 165, 0.1);
}

textarea.form-control {
  resize: vertical;
  min-height: 120px;
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

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-block {
  width: 100%;
  text-align: center;
}

/* Messages */
.success-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #D4EDDA;
  color: #155724;
  border-radius: 4px;
  text-align: center;
  font-weight: 600;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #F8D7DA;
  color: #721C24;
  border-radius: 4px;
  text-align: center;
  font-weight: 600;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .admin-claim-detail-page {
    padding: 1.5rem 0;
  }

  .container {
    padding: 0 1rem;
  }

  .detail-layout {
    grid-template-columns: 1fr;
  }

  .edit-card {
    position: static;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
