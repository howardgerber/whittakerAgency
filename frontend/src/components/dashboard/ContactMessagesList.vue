<template>
  <div class="contact-messages-section">
    <div class="section-header">
      <h2>Your Messages</h2>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <p>Loading your messages...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="messages.length === 0" class="empty-state">
      <div class="empty-icon">💬</div>
      <p>No messages yet. Have a question? Send us a message!</p>
      <router-link to="/contact" class="btn btn-primary">Send Message</router-link>
    </div>

    <!-- Messages Display -->
    <div v-else>
      <!-- Messages Table (Desktop) -->
      <div class="messages-table desktop-only">
        <table>
          <thead>
            <tr>
              <th>Subject</th>
              <th>Submitted Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="message in messages" :key="message.id">
              <td>
                <div class="subject-cell">
                  <span class="subject-icon">{{ getSubjectIcon(message.subject) }}</span>
                  <span>{{ getSubjectLabel(message.subject) }}</span>
                </div>
              </td>
              <td>{{ formatDate(message.created_at) }}</td>
              <td>
                <span :class="['status-badge', `status-${message.status}`]">
                  {{ formatText(message.status) }}
                </span>
              </td>
              <td>
                <router-link :to="`/contact/${message.id}`" class="btn-view">View Details</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Messages Cards (Mobile) -->
      <div class="messages-cards mobile-only">
        <div v-for="message in messages" :key="message.id" class="message-card">
          <div class="card-header">
            <div class="card-title">
              <span class="subject-icon">{{ getSubjectIcon(message.subject) }}</span>
              <span>{{ getSubjectLabel(message.subject) }}</span>
            </div>
            <span :class="['status-badge', `status-${message.status}`]">
              {{ formatText(message.status) }}
            </span>
          </div>
          <div class="card-body">
            <div class="card-info">
              <span class="label">Submitted:</span>
              <span class="value">{{ formatDate(message.created_at) }}</span>
            </div>
          </div>
          <div class="card-actions">
            <router-link :to="`/contact/${message.id}`" class="btn btn-view-mobile">View Details</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import contactService, { type ContactMessageResponse } from '@/services/contact'
import { formatDate, formatText } from '@/utils/formatters'

const messages = ref<ContactMessageResponse[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    messages.value = await contactService.getUserMessages()
  } catch (err: any) {
    console.error('Error loading contact messages:', err)
    error.value = 'Failed to load your messages. Please try again later.'
  } finally {
    loading.value = false
  }
})

const getSubjectIcon = (subject: string): string => {
  const iconMap: Record<string, string> = {
    general: '💬',
    quote: '📋',
    claim: '🔔',
    policy: '📄',
    other: '❓'
  }
  return iconMap[subject] || '📧'
}

const getSubjectLabel = (subject: string): string => {
  const labelMap: Record<string, string> = {
    general: 'General Question',
    quote: 'Quote Question',
    claim: 'Claim Question',
    policy: 'Policy Question',
    other: 'Other'
  }
  return labelMap[subject] || subject
}
</script>

<style scoped>
.contact-messages-section {
  margin-top: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  color: var(--color-primary);
  margin: 0;
}

.btn-send-message {
  padding: 0.5rem 1rem;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.btn-send-message:hover {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
}

.loading, .error-message {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px dashed #d0d0d0;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.6;
}

.empty-state p {
  color: #666;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

/* Desktop/Mobile Display Control */
.desktop-only {
  display: block !important;
}

.mobile-only {
  display: none !important;
}

.messages-table table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.messages-table thead {
  background: var(--color-primary);
  border-bottom: 2px solid #e0e0e0;
}

.messages-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: white;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.messages-table td {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  color: #333;
}

.messages-table tbody tr:last-child td {
  border-bottom: none;
}

.messages-table tbody tr:hover {
  background: #f8f9fa;
}

.subject-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.subject-icon {
  font-size: 1.25rem;
  line-height: 1;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  display: inline-block;
}

.status-new {
  background: #3B82F6;
  color: white;
}

.status-read {
  background: #F59E0B;
  color: white;
}

.status-responded {
  background: #10B981;
  color: white;
}

.status-closed {
  background: #6B7280;
  color: white;
}

.btn-view {
  padding: 0.375rem 1rem;
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.875rem;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
}

.btn-view:hover {
  background: var(--color-primary);
  color: white;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
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
  transform: translateY(-1px);
}

/* Mobile Cards */
.messages-cards {
  display: grid;
  gap: 1rem;
}

.message-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: box-shadow 0.3s;
}

.message-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 1rem 1.25rem;
  background: var(--color-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: white;
  font-size: 1.05rem;
}

.card-title .subject-icon {
  filter: brightness(0) invert(1);
}

.card-body {
  padding: 1rem;
}

.card-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-info .label {
  color: #666;
  font-size: 0.875rem;
}

.card-info .value {
  color: #333;
  font-weight: 600;
}

.card-actions {
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
}

.btn-view-mobile {
  display: block;
  width: 100%;
  padding: 0.75rem;
  text-align: center;
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  border-radius: 4px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.btn-view-mobile:hover {
  background: var(--color-primary);
  color: white;
}

@media (max-width: 768px) {
  .desktop-only {
    display: none !important;
  }

  .mobile-only {
    display: block !important;
  }

  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .btn-send-message {
    width: 100%;
    text-align: center;
  }

  .empty-state {
    padding: 2rem 1rem;
  }

  .empty-icon {
    font-size: 3rem;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
