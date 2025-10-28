<template>
  <div class="contact-detail-page">
    <div class="container">
      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <p>Loading message details...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <router-link to="/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
      </div>

      <!-- Message Detail -->
      <div v-else-if="message" class="message-detail">
        <!-- Header -->
        <div class="message-header">
          <div>
            <h1>{{ getSubjectLabel(message.subject) }}</h1>
            <p class="message-meta">Message #{{ message.id }} • Submitted on {{ formatDateTime(message.created_at) }}</p>
          </div>
          <span :class="['status-badge', `status-${message.status}`]">
            {{ formatText(message.status) }}
          </span>
        </div>

        <!-- Message Info Grid -->
        <div class="message-info-grid">
          <div class="info-card">
            <h3>Message Information</h3>
            <div class="info-item">
              <span class="label">Name:</span>
              <span class="value">{{ message.full_name }}</span>
            </div>
            <div class="info-item">
              <span class="label">Email:</span>
              <span class="value">{{ message.email }}</span>
            </div>
            <div v-if="message.phone" class="info-item">
              <span class="label">Phone:</span>
              <span class="value">{{ message.phone }}</span>
            </div>
            <div class="info-item">
              <span class="label">Subject:</span>
              <span class="value">{{ getSubjectLabel(message.subject) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Submitted:</span>
              <span class="value">{{ formatDate(message.created_at) }}</span>
            </div>
          </div>

          <div class="info-card">
            <h3>Your Message</h3>
            <div class="message-content">{{ message.message }}</div>
          </div>
        </div>

        <!-- Admin Response Section -->
        <div v-if="message.admin_response" class="notes-section">
          <h3>Our Response</h3>
          <p>{{ message.admin_response }}</p>
          <div v-if="message.responded_at" class="response-date">
            Responded on {{ formatDateTime(message.responded_at) }}
          </div>
        </div>

        <!-- No Response Yet -->
        <div v-else class="notes-section no-response">
          <h3>Status</h3>
          <p>We received your message and will respond soon. Check back here or we'll email you when we reply.</p>
        </div>

        <!-- Actions -->
        <div class="actions">
          <router-link to="/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import contactService, { type ContactMessageDetail } from '@/services/contact'
import { formatDate, formatDateTime, formatText } from '@/utils/formatters'

const route = useRoute()

const message = ref<ContactMessageDetail | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const messageId = route.params.id as string

  if (!messageId) {
    error.value = 'Invalid message ID'
    loading.value = false
    return
  }

  try {
    message.value = await contactService.getMessageDetail(messageId)
  } catch (err: any) {
    console.error('Error loading message:', err)
    if (err.response?.status === 403) {
      error.value = 'You do not have permission to view this message.'
    } else if (err.response?.status === 404) {
      error.value = 'Message not found.'
    } else {
      error.value = 'Failed to load message details. Please try again later.'
    }
  } finally {
    loading.value = false
  }
})

const getSubjectLabel = (subject: string): string => {
  const subjectMap: Record<string, string> = {
    general: 'General Question',
    quote: 'Quote Question',
    claim: 'Claim Question',
    policy: 'Policy Question',
    other: 'Other'
  }
  return subjectMap[subject] || subject
}
</script>

<style scoped>
.contact-detail-page {
  min-height: calc(100vh - 200px);
  padding: 3rem 0;
  background: #f5f7fa;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 2rem;
}

.loading, .error-message {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message-detail {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.message-header h1 {
  color: var(--color-primary);
  margin-bottom: 0.5rem;
}

.message-meta {
  color: #666;
  font-size: 1rem;
  font-weight: 600;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-new {
  background: #FFF3CD;
  color: #856404;
}

.status-read {
  background: #CCE5FF;
  color: #004085;
}

.status-responded {
  background: #D4EDDA;
  color: #155724;
}

.status-closed {
  background: #D4EDDA;
  color: #155724;
}

.message-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.info-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  background: #fafafa;
}

.info-card h3 {
  background: var(--color-primary);
  color: white;
  margin: -1.5rem -1.5rem 1rem -1.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px 8px 0 0;
  font-weight: 600;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item .label {
  color: #666;
  font-weight: 600;
}

.info-item .value {
  color: #333;
}

.message-content {
  color: #333;
  line-height: 1.7;
  font-size: 1rem;
  white-space: pre-wrap;
}

.notes-section {
  margin-bottom: 2rem;
  padding: 0;
  background: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.notes-section h3 {
  background: var(--color-primary);
  color: white;
  margin: 0;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
}

.notes-section p {
  padding: 1.5rem;
  margin: 0;
  color: #333;
  line-height: 1.7;
  font-size: 1rem;
}

.response-date {
  padding: 0 1.5rem 1.5rem 1.5rem;
  color: #666;
  font-size: 0.875rem;
  font-weight: 600;
}

.no-response {
  background: #EFF6FF;
  border: 2px solid #93C5FD;
}

.no-response p {
  color: #1E40AF;
}

.actions {
  display: flex;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
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

@media (max-width: 768px) {
  .message-header {
    flex-direction: column;
    gap: 1rem;
  }

  .message-info-grid {
    grid-template-columns: 1fr;
  }

  .actions {
    flex-direction: column;
  }

  .actions .btn {
    width: 100%;
    text-align: center;
  }
}
</style>
