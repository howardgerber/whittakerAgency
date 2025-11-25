<template>
  <div class="claims-section">
    <div class="claims-header">
      <h2>Your Claims</h2>
    </div>

    <div v-if="loading" class="loading">
      <p>Loading your claims...</p>
    </div>

    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="claims.length === 0" class="empty-state">
      <p>You haven't filed any claims yet.</p>
      <router-link to="/claims" class="btn btn-secondary">Learn About Claims</router-link>
    </div>

    <div v-else class="claims-list">
      <div v-for="claim in claims" :key="claim.id" class="claim-card">
        <div class="claim-header">
          <div class="header-left">
            <span class="category-icon">{{ getCategoryIcon(claim.category, claim.subcategory) }}</span>
            <h3>{{ getIncidentTypeName(claim.claim_data.incident_type) }}</h3>
          </div>
          <span :class="['status-badge', `status-${claim.status}`]">
            {{ formatText(claim.status) }}
          </span>
        </div>

        <div class="claim-details">
          <div class="detail-item">
            <span class="label">Incident Date:</span>
            <span class="value">{{ formatDate(claim.incident_date) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Submitted:</span>
            <span class="value">{{ formatDate(claim.created_at) }}</span>
          </div>
          <div class="detail-item claim-action-item">
            <router-link :to="`/claims/${claim.id}`" class="btn btn-secondary">View Details</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import claimService, { type ClaimResponse } from '@/services/claims'
import { formatDate, formatText } from '@/utils/formatters'

const claims = ref<ClaimResponse[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    claims.value = await claimService.getMyClaims()
  } catch (err: any) {
    console.error('Error loading claims:', err)
    error.value = 'Failed to load your claims. Please try again later.'
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

const getIncidentTypeName = (incidentType: string): string => {
  const typeMap: Record<string, string> = {
    collision: 'Collision with Another Vehicle',
    single_vehicle: 'Single Vehicle Accident',
    theft: 'Theft',
    vandalism: 'Vandalism',
    weather: 'Weather Damage',
    hit_and_run: 'Hit and Run',
    rollover: 'Rollover',
    avalanche: 'Avalanche',
    mechanical_failure: 'Mechanical Failure',
    other: 'Other'
  }
  return typeMap[incidentType] || incidentType
}

</script>

<style scoped>
.claims-section {
  margin-top: 0;
}

.claims-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.claims-header h2 {
  color: var(--color-primary);
  margin: 0;
  flex-shrink: 0;
}

.loading, .error-message, .empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.empty-state .btn {
  margin-top: 1rem;
}

.claims-list {
  display: grid;
  gap: 1.5rem;
}

.claim-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.claim-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.claim-header {
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

.claim-header h3 {
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

.status-in_review {
  background: #CCE5FF;
  color: #004085;
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

.claim-details {
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

.claim-action-item {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
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
  .claim-header {
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

  .claim-details {
    grid-template-columns: 1fr;
  }
}
</style>
