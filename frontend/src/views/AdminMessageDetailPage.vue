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
        <h1>Contact Message Details</h1>
        <StatusBadge v-if="message" :status="message.status" />
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>Loading message details...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <button @click="loadMessage" class="btn btn-primary">Retry</button>
      </div>

      <!-- Message Details -->
      <div v-else-if="message" class="detail-layout">
        <!-- Left Column: Readonly Information -->
        <div class="info-section">
          <!-- Sender Information -->
          <div class="info-card">
            <h2>Sender Information</h2>
            <div class="info-row">
              <span class="label">Name:</span>
              <span class="value">{{ message.sender_name }}</span>
            </div>
            <div class="info-row">
              <span class="label">Email:</span>
              <span class="value">{{ message.sender_email }}</span>
            </div>
            <div class="info-row" v-if="message.sender_phone">
              <span class="label">Phone:</span>
              <span class="value">{{ message.sender_phone }}</span>
            </div>
            <div class="info-row">
              <span class="label">User Type:</span>
              <span class="value">
                <span :class="['badge', message.is_guest ? 'badge-guest' : 'badge-customer']">
                  {{ message.is_guest ? 'Guest' : 'Customer' }}
                </span>
              </span>
            </div>
            <div class="info-row">
              <span class="label">Subject:</span>
              <span class="value">{{ message.subject.charAt(0).toUpperCase() + message.subject.slice(1) }}</span>
            </div>
            <div class="info-row">
              <span class="label">Submitted:</span>
              <span class="value">{{ formatDateTime(message.created_at) }}</span>
            </div>
            <div class="info-row" v-if="message.updated_at !== message.created_at">
              <span class="label">Last Updated:</span>
              <span class="value">{{ formatDateTime(message.updated_at) }}</span>
            </div>
          </div>

          <!-- Message Content -->
          <div class="info-card">
            <h2>Message</h2>
            <div class="message-content">
              {{ message.message }}
            </div>
          </div>

          <!-- Existing Response (if any) -->
          <div class="info-card" v-if="message.admin_response">
            <h2>Previous Response</h2>
            <div class="response-content">
              {{ message.admin_response }}
            </div>
            <div class="response-meta" v-if="message.responded_at">
              <small>Responded: {{ formatDateTime(message.responded_at) }}</small>
            </div>
          </div>
        </div>

        <!-- Right Column: Editable Admin Section -->
        <div class="edit-section">
          <div class="edit-card">
            <h2>Admin Actions</h2>

            <form @submit.prevent="saveResponse">
              <!-- Status -->
              <div class="form-group">
                <label for="status">Status</label>
                <select id="status" v-model="formData.status" class="form-control">
                  <option value="new">New</option>
                  <option value="read">Read</option>
                  <option value="responded">Responded</option>
                  <option value="closed">Closed</option>
                </select>
              </div>

              <!-- Appointment Date -->
              <div class="form-group">
                <label for="appointment_date">Appointment Date (Optional)</label>
                <input
                  id="appointment_date"
                  v-model="formData.appointment_date"
                  type="date"
                  class="form-control"
                />
              </div>

              <!-- Admin Response -->
              <div class="form-group">
                <label for="admin_response">Response to Customer</label>
                <textarea
                  id="admin_response"
                  v-model="formData.admin_response"
                  class="form-control"
                  rows="8"
                  placeholder="Type your response here. This will be sent to the customer via email..."
                ></textarea>
              </div>

              <!-- Save Button -->
              <div class="form-actions">
                <button type="submit" class="btn btn-primary btn-block" :disabled="saving || !hasChanges">
                  {{ saving ? 'Sending...' : 'Send Response' }}
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
import adminService, { type AdminMessage } from '@/services/admin'
import { formatDateTime } from '@/utils/formatters'

// Route and data
const route = useRoute()
const router = useRouter()
const id = Number(route.params.id)

const message = ref<AdminMessage | null>(null)
const loading = ref(true)
const error = ref('')
const saving = ref(false)
const successMessage = ref('')
const saveError = ref('')

// Form data
const formData = ref({
  status: '',
  appointment_date: '',
  admin_response: ''
})

// Original data to track changes
const originalData = ref({
  status: '',
  appointment_date: '',
  admin_response: ''
})

// Check if form has changes
const hasChanges = computed(() => {
  return formData.value.status !== originalData.value.status ||
         formData.value.appointment_date !== originalData.value.appointment_date ||
         formData.value.admin_response !== originalData.value.admin_response
})

// Load message on mount
onMounted(async () => {
  await loadMessage()
})

// Load message from API
const loadMessage = async () => {
  loading.value = true
  error.value = ''

  try {
    message.value = await adminService.getMessage(id)

    // Auto-mark as "read" if status is "new"
    if (message.value.status === 'new') {
      // Update status to "read" without showing a success message
      await adminService.updateMessage(id, { status: 'read' })
      message.value.status = 'read'
    }

    // Initialize form data with current values
    formData.value = {
      status: message.value.status,
      appointment_date: message.value.appointment_date || '',
      admin_response: message.value.admin_response || ''
    }

    // Store original values for change detection
    originalData.value = {
      status: message.value.status,
      appointment_date: message.value.appointment_date || '',
      admin_response: message.value.admin_response || ''
    }
  } catch (err: any) {
    console.error('Error loading message:', err)
    error.value = 'Failed to load message details. Please try again.'
  } finally {
    loading.value = false
  }
}

// Save response
const saveResponse = async () => {
  if (!message.value) return

  saving.value = true
  saveError.value = ''
  successMessage.value = ''

  try {
    const updateData: any = {
      status: formData.value.status
    }

    // Only include appointment_date if it has a value
    if (formData.value.appointment_date) {
      updateData.appointment_date = formData.value.appointment_date
    }

    // Include admin_response if provided
    if (formData.value.admin_response.trim()) {
      updateData.admin_response = formData.value.admin_response.trim()
      // Automatically set status to "responded" if a response is provided
      updateData.status = 'responded'
      formData.value.status = 'responded'
    }

    message.value = await adminService.updateMessage(id, updateData)
    successMessage.value = 'Response sent successfully!'

    // Update original data after successful save
    originalData.value = {
      status: message.value.status,
      appointment_date: message.value.appointment_date || '',
      admin_response: message.value.admin_response || ''
    }

    // Clear success message after 3 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (err: any) {
    console.error('Error saving response:', err)
    saveError.value = 'Failed to send response. Please try again.'
  } finally {
    saving.value = false
  }
}


// Navigate back to referrer or default to messages list
const goBack = () => {
  const referrer = sessionStorage.getItem('message_referrer')
  if (referrer) {
    sessionStorage.removeItem('message_referrer')
    router.push(referrer)
  } else {
    router.push('/admin/messages')
  }
}
</script>

<style scoped>
.admin-message-detail-page {
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

/* Badges */
.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-guest {
  background: #CCE5FF;
  color: #004085;
}

.badge-customer {
  background: #C3E6CB;
  color: #0F5132;
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
.info-card .message-content,
.info-card .response-content {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

.info-card .info-row:first-of-type {
  padding-top: 1.5rem;
}

.info-card .message-content,
.info-card .response-content {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
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

.message-content {
  background: white;
  padding: 1rem;
  color: #333;
  white-space: pre-wrap;
  line-height: 1.6;
}

.response-content {
  background: white;
  padding: 1rem;
  color: #333;
  white-space: pre-wrap;
  line-height: 1.6;
}

.response-meta {
  margin-top: 0.75rem;
  text-align: right;
  color: #666;
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
  min-height: 150px;
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
  .admin-message-detail-page {
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
