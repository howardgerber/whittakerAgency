<template>
  <div class="quote-detail-page">
    <div class="container">
      <div v-if="loading" class="loading">
        <p>Loading quote details...</p>
      </div>

      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <router-link to="/dashboard" class="btn btn-primary">Back to Dashboard</router-link>
      </div>

      <div v-else-if="quote" class="quote-detail">
        <div class="quote-header">
          <div>
            <h1>{{ getInsuranceName(quote.category, quote.subcategory) }}</h1>
            <p v-if="quote.subcategory" class="quote-subtype">{{ quote.category.charAt(0).toUpperCase() + quote.category.slice(1) }} Category</p>
          </div>
          <span :class="['status-badge', `status-${quote.status}`]">
            {{ formatText(quote.status) }}
          </span>
        </div>

        <div class="quote-info-grid">
          <div class="info-card">
            <h3>Quote Information</h3>
            <div class="info-item">
              <span class="label">Insurance Type:</span>
              <span class="value">{{ getCategoryDisplay(quote.category, quote.subcategory) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Submitted:</span>
              <span class="value">{{ formatDateOnly(quote.created_at) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Last Updated:</span>
              <span class="value">{{ formatDateOnly(quote.updated_at) }}</span>
            </div>
            <div v-if="quote.quoted_at" class="info-item">
              <span class="label">Quoted On:</span>
              <span class="value">{{ formatDateOnly(quote.quoted_at) }}</span>
            </div>
            <div v-if="quote.quote_amount" class="info-item highlight">
              <span class="label">Quote Amount:</span>
              <span class="value quote-amount">${{ quote.quote_amount }}/month</span>
            </div>
          </div>

          <div class="info-card">
            <h3>Quote Details</h3>
            <div class="quote-details-compact">
              <div v-for="(value, key) in groupedQuoteData" :key="key" class="detail-section">
                <h4 class="section-header">{{ key }}</h4>
                <div v-for="field in value" :key="field.key" class="detail-item">
                  <span class="detail-label">{{ field.label }}:</span>
                  <span :class="['detail-value', field.special ? 'report-number' : '']">{{ field.value }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="quote.customer_notes" class="notes-section">
          <h3>Your Notes</h3>
          <p>{{ quote.customer_notes }}</p>
        </div>

        <div v-if="quote.agent_notes" class="notes-section agent-notes">
          <h3>Agent Notes</h3>
          <p>{{ quote.agent_notes }}</p>
        </div>

        <div class="actions">
          <router-link to="/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import quoteService, { type QuoteResponse } from '@/services/quotes'
import { formatDate as formatDateUtil, formatText } from '@/utils/formatters'

const route = useRoute()

const quote = ref<QuoteResponse | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const quoteId = parseInt(route.params.id as string)

  if (isNaN(quoteId)) {
    error.value = 'Invalid quote ID'
    loading.value = false
    return
  }

  try {
    quote.value = await quoteService.getQuote(quoteId)
  } catch (err: any) {
    console.error('Error loading quote:', err)
    if (err.response?.status === 404) {
      error.value = 'Quote not found'
    } else if (err.response?.status === 403) {
      error.value = 'You do not have permission to view this quote'
    } else {
      error.value = 'Failed to load quote details'
    }
  } finally {
    loading.value = false
  }
})

const getInsuranceName = (category: string, subcategory: string | null): string => {
  // Show most specific name (subcategory if exists, else category)
  if (subcategory) {
    const nameMap: Record<string, string> = {
      // Vehicle
      auto: 'Auto Insurance',
      motorcycle: 'Motorcycle Insurance',
      atv: 'ATV/Off-Road Insurance',
      boat: 'Boat Insurance',
      rv: 'RV Insurance',
      snowmobile: 'Snowmobile Insurance',
      roadside: 'Roadside Assistance',
      vehicle_protection: 'Vehicle Protection',

      // Property
      homeowners: 'Homeowners Insurance',
      renters: 'Renters Insurance',
      condo: 'Condo Insurance',
      landlord: 'Landlord Insurance',
      mobile_home: 'Mobile Home Insurance',

      // Other
      umbrella: 'Umbrella Policy',
      pet: 'Pet Insurance',
      travel: 'Travel Insurance',
      jewelry: 'Jewelry Insurance',
      collectibles: 'Collectibles Insurance',
      individual_health: 'Individual Health Insurance',
      event: 'Event Insurance'
    }
    return nameMap[subcategory] || `${subcategory.charAt(0).toUpperCase() + subcategory.slice(1)} Insurance`
  }

  // Categories without subcategories
  const categoryNameMap: Record<string, string> = {
    life: 'Life Insurance',
    business: 'Business Insurance',
    identity_protection: 'Identity Protection'
  }

  return categoryNameMap[category] || `${category.charAt(0).toUpperCase() + category.slice(1)} Insurance`
}

// Use shared formatter from utils
const formatDateOnly = formatDateUtil

const getCategoryDisplay = (category: string, subcategory: string | null): string => {
  const categoryName = category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ')
  if (subcategory) {
    const subcategoryName = subcategory.charAt(0).toUpperCase() + subcategory.slice(1).replace('_', ' ')
    return `${categoryName} / ${subcategoryName}`
  }
  return categoryName
}

const formatFieldLabel = (key: string): string => {
  // Convert snake_case to Title Case
  return key.split('_').map(word =>
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

const formatFieldValue = (key: string, value: any): { value: string; special: boolean } => {
  if (typeof value === 'boolean') {
    return { value: value ? 'Yes' : 'No', special: false }
  }
  if (key.includes('amount') || key.includes('deductible') || key.includes('premium')) {
    const num = typeof value === 'string' ? parseFloat(value) : value
    return {
      value: new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
      }).format(num),
      special: false
    }
  }
  if (key === 'vin') {
    return { value: value, special: true }
  }
  if (typeof value === 'string' && value.includes('_')) {
    return { value: formatFieldLabel(value), special: false }
  }
  return { value: String(value), special: false }
}

// Group quote data into logical sections
const groupedQuoteData = computed(() => {
  if (!quote.value) return {}

  const data = quote.value.quote_data
  const groups: Record<string, Array<{ key: string; label: string; value: string; special: boolean }>> = {}

  // Define grouping logic
  const vehicleFields = ['year', 'make', 'model', 'vin']
  const coverageFields = ['coverage_level', 'coverage_amount', 'policy_type', 'deductible', 'term_length']

  for (const [key, value] of Object.entries(data)) {
    if (value === null || value === undefined || value === '') continue

    let section = 'Other Details'

    if (vehicleFields.includes(key)) {
      section = 'Vehicle Information'
    } else if (coverageFields.includes(key)) {
      section = 'Coverage Details'
    } else if (key === 'current_provider') {
      section = 'Current Insurance'
    } else if (typeof value === 'object' && value !== null) {
      // Handle services object
      section = 'Services'
      for (const [serviceKey, serviceValue] of Object.entries(value)) {
        if (!groups[section]) groups[section] = []
        const formatted = formatFieldValue(serviceKey, serviceValue)
        groups[section].push({
          key: serviceKey,
          label: formatFieldLabel(serviceKey),
          value: formatted.value,
          special: formatted.special
        })
      }
      continue
    }

    if (!groups[section]) groups[section] = []
    const formatted = formatFieldValue(key, value)
    groups[section].push({
      key,
      label: formatFieldLabel(key),
      value: formatted.value,
      special: formatted.special
    })
  }

  return groups
})
</script>

<style scoped>
.quote-detail-page {
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

.quote-detail {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.quote-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.quote-header h1 {
  color: var(--color-primary);
  margin-bottom: 0.5rem;
}

.quote-subtype {
  color: #666;
  font-size: 1.1rem;
  font-weight: 600;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-pending {
  background: #FFF3CD;
  color: #856404;
}

.status-in_review {
  background: #CCE5FF;
  color: #004085;
}

.status-quoted {
  background: #D4EDDA;
  color: #155724;
}

.quote-info-grid {
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

.info-item.highlight {
  background: #f8f9fa;
  padding: 1rem;
  margin-top: 0.5rem;
  border-radius: 4px;
}

.info-item .label {
  color: #666;
  font-weight: 600;
}

.info-item .value {
  color: #333;
}

.quote-amount {
  color: var(--color-primary);
  font-size: 1.25rem;
  font-weight: 700;
}

.data-display {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 0.875rem;
  color: #333;
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
}

.agent-notes {
  background: #fff9e6;
  border-left: 4px solid #ffc107;
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
  .quote-header {
    flex-direction: column;
    gap: 1rem;
  }

  .quote-info-grid {
    grid-template-columns: 1fr;
  }
}

/* Compact Quote Details Styling (same as claims) */
.quote-details-compact {
  font-size: 14px;
}

.detail-section {
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.detail-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.section-header {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.75rem;
  border-bottom: 2px solid var(--color-primary);
  padding-bottom: 0.25rem;
}

.detail-item {
  display: grid;
  grid-template-columns: 180px 1fr;
  gap: 1rem;
  padding: 0.5rem 0;
  font-size: 13px;
  line-height: 1.5;
  align-items: center;
}

.detail-label {
  font-weight: 600;
  color: #666;
}

.detail-value {
  color: #333;
}

.report-number {
  font-family: 'Courier New', monospace;
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 13px;
}

@media (max-width: 768px) {
  .detail-item {
    grid-template-columns: 1fr;
    gap: 0.25rem;
  }
}
</style>
