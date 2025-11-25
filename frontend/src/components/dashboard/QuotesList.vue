<template>
  <div class="quotes-section">
    <div class="quotes-header">
      <h2>Your Quotes</h2>
      <div class="filters">
        <select v-model="selectedCategory" class="filter-dropdown">
          <option value="">All Categories</option>
          <option v-for="category in availableCategories" :key="category.value" :value="category.value">
            {{ category.icon }} {{ category.label }}
          </option>
        </select>
        <select v-model="selectedYear" class="filter-dropdown">
          <option value="">All Years</option>
          <option v-for="year in availableYears" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <p>Loading your quotes...</p>
    </div>

    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="quotes.length === 0" class="empty-state">
      <p>You haven't requested any quotes yet.</p>
      <router-link to="/quote" class="btn btn-primary">Request Your First Quote</router-link>
    </div>

    <div v-else class="quotes-list">
      <div v-for="quote in filteredQuotes" :key="quote.id" class="quote-card">
        <div class="quote-header">
          <div class="header-left">
            <span class="category-icon">{{ getCategoryIcon(quote.category, quote.subcategory) }}</span>
            <h3>{{ getInsuranceName(quote.category, quote.subcategory) }}</h3>
          </div>
          <span :class="['status-badge', `status-${quote.status}`]">
            {{ formatText(quote.status) }}
          </span>
        </div>

        <div class="quote-details">
          <div class="detail-item">
            <span class="label">Submitted:</span>
            <span class="value">{{ formatDate(quote.created_at) }}</span>
          </div>
          <div v-if="quote.quote_amount" class="detail-item">
            <span class="label">Quote Amount:</span>
            <span class="value quote-amount">${{ quote.quote_amount }}/mo</span>
          </div>
          <div class="detail-item quote-action-item">
            <router-link :to="`/quotes/${quote.id}`" class="btn btn-secondary">View Details</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import quoteService, { type QuoteResponse } from '@/services/quotes'
import { formatDate, formatText } from '@/utils/formatters'

const quotes = ref<QuoteResponse[]>([])
const loading = ref(true)
const error = ref('')

// Filter state
const selectedCategory = ref('')
const selectedYear = ref('')

onMounted(async () => {
  try {
    quotes.value = await quoteService.getMyQuotes()
  } catch (err: any) {
    console.error('Error loading quotes:', err)
    error.value = 'Failed to load your quotes. Please try again later.'
  } finally {
    loading.value = false
  }
})

const getCategoryIcon = (category: string, subcategory: string | null): string => {
  const type = subcategory || category

  const iconMap: Record<string, string> = {
    vehicle: '🚗',
    property: '🏠',
    life: '❤️',
    business: '💼',
    identity_protection: '🔒',
    other: '📋',
    auto: '🚗',
    motorcycle: '🏍️',
    atv: '🛞',
    boat: '⛵',
    rv: '🚐',
    snowmobile: '🛷',
    roadside: '🚨',
    vehicle_protection: '🛡️',
    homeowners: '🏠',
    renters: '🏢',
    condo: '🏘️',
    landlord: '🏚️',
    mobile_home: '🚐',
    umbrella: '☂️',
    pet: '🐾',
    travel: '✈️',
    jewelry: '💎',
    collectibles: '🏺',
    individual_health: '🏥',
    event: '🎉'
  }

  return iconMap[type] || '📄'
}

const getInsuranceName = (category: string, subcategory: string | null): string => {
  if (subcategory) {
    const nameMap: Record<string, string> = {
      auto: 'Auto Insurance',
      motorcycle: 'Motorcycle Insurance',
      atv: 'ATV/Off-Road Insurance',
      boat: 'Boat Insurance',
      rv: 'RV Insurance',
      snowmobile: 'Snowmobile Insurance',
      roadside: 'Roadside Assistance',
      vehicle_protection: 'Vehicle Protection',
      homeowners: 'Homeowners Insurance',
      renters: 'Renters Insurance',
      condo: 'Condo Insurance',
      landlord: 'Landlord Insurance',
      mobile_home: 'Mobile Home Insurance',
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

  const categoryNameMap: Record<string, string> = {
    life: 'Life Insurance',
    business: 'Business Insurance',
    identity_protection: 'Identity Protection'
  }

  return categoryNameMap[category] || `${category.charAt(0).toUpperCase() + category.slice(1)} Insurance`
}

const availableCategories = computed(() => {
  const categoryMap: Record<string, { value: string; label: string; icon: string }> = {
    vehicle: { value: 'vehicle', label: 'Vehicle', icon: '🚗' },
    property: { value: 'property', label: 'Property', icon: '🏠' },
    life: { value: 'life', label: 'Life', icon: '❤️' },
    business: { value: 'business', label: 'Business', icon: '💼' },
    identity_protection: { value: 'identity_protection', label: 'Identity Protection', icon: '🔒' },
    phone_protection: { value: 'phone_protection', label: 'Phone Protection', icon: '📱' },
    other: { value: 'other', label: 'Other', icon: '☂️' }
  }

  const uniqueCategories = new Set<string>()
  quotes.value.forEach(quote => {
    uniqueCategories.add(quote.category)
  })

  return Array.from(uniqueCategories)
    .map(cat => categoryMap[cat])
    .filter(Boolean)
    .sort((a, b) => a.label.localeCompare(b.label))
})

const availableYears = computed(() => {
  const years = new Set<number>()
  quotes.value.forEach(quote => {
    const year = new Date(quote.created_at).getFullYear()
    years.add(year)
  })
  return Array.from(years).sort((a, b) => b - a)
})

const filteredQuotes = computed(() => {
  return quotes.value.filter(quote => {
    if (selectedCategory.value && quote.category !== selectedCategory.value) {
      return false
    }

    if (selectedYear.value) {
      const year = new Date(quote.created_at).getFullYear()
      if (year !== Number(selectedYear.value)) {
        return false
      }
    }

    return true
  })
})
</script>

<style scoped>
.quotes-section {
  margin-top: 0;
}

.quotes-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.quotes-header h2 {
  color: var(--color-primary);
  margin: 0;
  flex-shrink: 0;
}

.filters {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.filter-dropdown {
  padding: 0.5rem 1rem;
  border: 1px solid #d0d0d0;
  border-radius: 4px;
  background: white;
  color: #333;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 180px;
}

.filter-dropdown:hover {
  border-color: var(--color-primary);
}

.filter-dropdown:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 61, 165, 0.1);
}

.loading, .error-message, .empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.empty-state .btn {
  margin-top: 1rem;
}

.quotes-list {
  display: grid;
  gap: 1.5rem;
}

.quote-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.quote-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.quote-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
  padding: 1.25rem 1.5rem;
  background: var(--color-primary);
  border-radius: 8px 8px 0 0;
  margin: -1.5rem -1.5rem 1rem -1.5rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.category-icon {
  font-size: 2rem;
  line-height: 1;
  filter: brightness(0) invert(1);
  opacity: 1;
}

.quote-header h3 {
  color: white;
  margin: 0;
  font-size: 1.25rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-submitted,
.status-pending {
  background: #FFF3CD;
  color: #856404;
}

.status-contacted {
  background: #CCE5FF;
  color: #004085;
}

.status-quoted {
  background: #D4EDDA;
  color: #155724;
}

.status-accepted {
  background: #C3E6CB;
  color: #0F5132;
}

.status-declined {
  background: #F8D7DA;
  color: #721C24;
}

.status-closed {
  background: #E2E3E5;
  color: #383D41;
}

.quote-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item .label {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.detail-item .value {
  font-weight: 600;
  color: #333;
}

.quote-action-item {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
}

.quote-amount {
  color: var(--color-primary);
  font-size: 1.125rem;
}

.btn {
  padding: 0.5rem 1.5rem;
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
  padding: 0.625rem 1.5rem;
  font-size: 1rem;
}

.btn-secondary:hover {
  background: var(--color-primary);
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 61, 165, 0.2);
}

@media (max-width: 768px) {
  .quotes-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .quotes-header h2 {
    text-align: center;
  }

  .filters {
    flex-direction: column;
    width: 100%;
  }

  .filter-dropdown {
    width: 100%;
  }

  .quote-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .header-left {
    width: 100%;
  }

  .category-icon {
    font-size: 1.75rem;
  }

  .quote-details {
    grid-template-columns: 1fr;
  }
}
</style>
