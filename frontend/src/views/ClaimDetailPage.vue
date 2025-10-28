<template>
  <div class="claim-detail-page">
    <div class="container">
      <div v-if="loading" class="loading">
        <p>Loading claim details...</p>
      </div>

      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <router-link to="/dashboard" class="btn btn-primary">Back to Dashboard</router-link>
      </div>

      <div v-else-if="claim" class="claim-detail">
        <div class="claim-header">
          <div>
            <h1>{{ getInsuranceName(claim.category, claim.subcategory) }} Claim</h1>
            <p class="claim-id">Claim ID: #{{ claim.id }} - {{ getIncidentTypeName(claim.claim_data.incident_type) }}</p>
          </div>
          <span :class="['status-badge', `status-${claim.status}`]">
            {{ formatText(claim.status) }}
          </span>
        </div>

        <!-- Claim Information Grid -->
        <div class="claim-info-grid">
          <div class="info-card">
            <h3>Claim Information</h3>
            <div class="info-item">
              <span class="label">Insurance Type:</span>
              <span class="value">{{ getInsuranceName(claim.category, claim.subcategory) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Incident Type:</span>
              <span class="value">{{ getIncidentTypeName(claim.claim_data.incident_type) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Incident Date:</span>
              <span class="value">{{ formatSimpleDate(claim.incident_date) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Submitted:</span>
              <span class="value">{{ formatSimpleDate(claim.created_at) }}</span>
            </div>
            <div v-if="claim.contacted_at" class="info-item">
              <span class="label">Contacted:</span>
              <span class="value">{{ formatSimpleDate(claim.contacted_at) }}</span>
            </div>
          </div>

          <div class="info-card">
            <h3>Appointment & Contact</h3>
            <div v-if="claim.appointment_requested" class="info-item">
              <span class="label">Appointment Requested:</span>
              <span class="value">{{ formatSimpleDate(claim.appointment_requested) }}</span>
            </div>
            <div v-else class="info-item">
              <span class="label">Appointment:</span>
              <span class="value">Not requested</span>
            </div>
            <div v-if="claim.preferred_contact_time" class="info-item">
              <span class="label">Preferred Contact Time:</span>
              <span class="value">{{ formatPreferredTime(claim.preferred_contact_time) }}</span>
            </div>
            <div class="info-item">
              <span class="label">Contact Preference:</span>
              <span class="value">{{ formatContactPreference(claim.contact_preference) }}</span>
            </div>
          </div>
        </div>

        <!-- Incident Summary -->
        <div class="description-section">
          <h3>Incident Summary</h3>
          <p>{{ claim.incident_summary }}</p>
        </div>

        <!-- Additional Notes -->
        <div v-if="claim.additional_notes" class="notes-section">
          <h3>Additional Notes</h3>
          <p>{{ claim.additional_notes }}</p>
        </div>

        <!-- Claim Details (Formatted) -->
        <div class="info-card" style="margin-bottom: 2rem;">
          <h3>Detailed Information</h3>
          <div class="claim-details-compact">
            <!-- Incident Details Section -->
            <div class="detail-section">
              <h4 class="section-header">Incident Details</h4>
              <div class="detail-item">
                <span class="detail-label">Incident Type:</span>
                <span class="detail-value">{{ formatClaimValue('incident_type', claim.claim_data.incident_type) }}</span>
              </div>
              <div v-if="claim.claim_data.incident_location" class="detail-item">
                <span class="detail-label">Location:</span>
                <span class="detail-value">{{ claim.claim_data.incident_location }}</span>
              </div>
            </div>

            <!-- Other Party Section -->
            <div v-if="claim.claim_data.other_party_involved === 'yes'" class="detail-section">
              <h4 class="section-header">Other Party</h4>
              <div v-if="claim.claim_data.other_party_name" class="detail-item">
                <span class="detail-label">Name:</span>
                <span class="detail-value">{{ claim.claim_data.other_party_name }}</span>
              </div>
              <div v-if="claim.claim_data.other_party_insurance" class="detail-item">
                <span class="detail-label">Insurance:</span>
                <span class="detail-value">{{ claim.claim_data.other_party_insurance }}</span>
              </div>
              <div v-if="claim.claim_data.other_party_phone" class="detail-item">
                <span class="detail-label">Phone:</span>
                <span class="detail-value">{{ claim.claim_data.other_party_phone }}</span>
              </div>
            </div>

            <!-- Police Report Section -->
            <div v-if="claim.claim_data.police_report_filed === 'yes'" class="detail-section">
              <h4 class="section-header">Police Report</h4>
              <div class="detail-item">
                <span class="detail-label">Report Filed:</span>
                <span class="detail-value badge-yes">Yes</span>
              </div>
              <div v-if="claim.claim_data.police_report_number" class="detail-item">
                <span class="detail-label">Report Number:</span>
                <span class="detail-value report-number">{{ claim.claim_data.police_report_number }}</span>
              </div>
              <div v-if="claim.claim_data.police_department" class="detail-item">
                <span class="detail-label">Department:</span>
                <span class="detail-value">{{ claim.claim_data.police_department }}</span>
              </div>
            </div>

            <!-- Vehicle Status Section -->
            <div v-if="claim.claim_data.vehicle_drivable !== undefined" class="detail-section">
              <h4 class="section-header">Vehicle Status</h4>
              <div class="detail-item">
                <span class="detail-label">Vehicle Drivable:</span>
                <span :class="['detail-value', claim.claim_data.vehicle_drivable === 'yes' ? 'badge-yes' : 'badge-no']">
                  {{ claim.claim_data.vehicle_drivable === 'yes' ? 'Yes' : 'No' }}
                </span>
              </div>
              <div v-if="claim.claim_data.damage_description" class="detail-item">
                <span class="detail-label">Damage Description:</span>
                <span class="detail-value">{{ claim.claim_data.damage_description }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Next Steps -->
        <div v-if="claim.status !== 'closed'" class="next-steps">
          <h3>What Happens Next?</h3>
          <div v-if="claim.status === 'submitted'" class="step-content">
            <p>We've received your claim and will review it shortly. An agent will contact you shortly to help you complete and officially file your claim. If you selected a preferred appointment date, we will confirm it during that outreach.</p>
          </div>
          <div v-else-if="claim.status === 'contacted'" class="step-content">
            <p>Our team has reached out to you. Please check your {{ formatContactPreference(claim.contact_preference).toLowerCase() }} for updates. If you haven't heard from us, please call our claims department.</p>
          </div>
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
import claimService, { type ClaimResponse } from '@/services/claims'
import { formatDate as formatDateUtil, formatText } from '@/utils/formatters'

const route = useRoute()

const claim = ref<ClaimResponse | null>(null)
const loading = ref(true)
const error = ref('')

// Status timeline will be implemented when backend supports status history
// const statusOrder = ['submitted', 'contacted', 'closed']

onMounted(async () => {
  const claimId = parseInt(route.params.id as string)

  if (isNaN(claimId)) {
    error.value = 'Invalid claim ID'
    loading.value = false
    return
  }

  try {
    claim.value = await claimService.getClaim(claimId)
  } catch (err: any) {
    console.error('Error loading claim:', err)
    if (err.response?.status === 404) {
      error.value = 'Claim not found'
    } else if (err.response?.status === 403) {
      error.value = 'You do not have permission to view this claim'
    } else {
      error.value = 'Failed to load claim details'
    }
  } finally {
    loading.value = false
  }
})

const getInsuranceName = (category: string, subcategory: string | null): string => {
  if (subcategory) {
    const nameMap: Record<string, string> = {
      auto: 'Auto',
      motorcycle: 'Motorcycle',
      boat: 'Boat',
      rv: 'RV',
      homeowners: 'Homeowners',
      renters: 'Renters',
      condo: 'Condo',
      landlord: 'Landlord',
      umbrella: 'Umbrella',
      pet: 'Pet',
      jewelry: 'Jewelry',
      travel: 'Travel'
    }
    return nameMap[subcategory] || subcategory.charAt(0).toUpperCase() + subcategory.slice(1)
  }

  const categoryNameMap: Record<string, string> = {
    life: 'Life',
    business: 'Business',
    identity_protection: 'Identity Protection'
  }

  return categoryNameMap[category] || category.charAt(0).toUpperCase() + category.slice(1)
}

// Use shared formatters from utils
const formatSimpleDate = formatDateUtil

const formatContactPreference = (preference: string): string => {
  const map: Record<string, string> = {
    email: 'Email',
    phone: 'Phone',
    either: 'Either Email or Phone'
  }
  return map[preference] || preference
}

const formatPreferredTime = (time: string): string => {
  const map: Record<string, string> = {
    morning: 'Morning (8am - 12pm)',
    afternoon: 'Afternoon (12pm - 5pm)',
    evening: 'Evening (5pm - 8pm)',
    anytime: 'Anytime'
  }
  return map[time] || time
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

const formatClaimValue = (key: string, value: any): string => {
  if (key === 'incident_type') {
    return getIncidentTypeName(value)
  }
  if (typeof value === 'string') {
    return value.charAt(0).toUpperCase() + value.slice(1)
  }
  return value
}

// Status timeline tracking will be implemented when backend supports status history
</script>

<style scoped>
.claim-detail-page {
  min-height: calc(100vh - 200px);
  padding: 3rem 0;
  background: #f5f7fa;
}

.container {
  max-width: 1100px;
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

.claim-detail {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.claim-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.claim-header h1 {
  color: var(--color-primary);
  margin-bottom: 0.5rem;
}

.claim-id {
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

/* Status Timeline */
.status-timeline {
  margin-bottom: 3rem;
  padding: 2rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 8px;
}

.status-timeline h3 {
  color: var(--color-primary);
  margin-bottom: 2rem;
  text-align: center;
}

.timeline {
  display: flex;
  justify-content: space-between;
  position: relative;
  padding: 0 2rem;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 30px;
  left: 10%;
  right: 10%;
  height: 4px;
  background: #dee2e6;
  z-index: 0;
}

.timeline-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.timeline-marker {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #dee2e6;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  transition: all 0.3s;
  border: 4px solid white;
}

.timeline-item.active .timeline-marker {
  background: linear-gradient(135deg, var(--color-primary), #0052CC);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 61, 165, 0.3);
}

.marker-icon {
  font-size: 1.8rem;
}

.timeline-item.active .marker-icon {
  filter: brightness(0) invert(1);
}

.timeline-content {
  text-align: center;
}

.timeline-content h4 {
  color: var(--color-primary);
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.timeline-content p {
  color: #666;
  font-size: 0.85rem;
}

.timeline-item.active .timeline-content h4 {
  font-weight: 700;
  color: var(--color-primary);
}

/* Claim Info Grid */
.claim-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
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
  border-bottom: 1px solid #e0e0e0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item.highlight {
  background: white;
  padding: 1rem;
  margin-top: 0.5rem;
  border-radius: 4px;
  border: 2px solid var(--color-primary);
}

.info-item .label {
  color: #666;
  font-weight: 600;
}

.info-item .value {
  color: #333;
  font-weight: 500;
  text-align: right;
}

.claim-amount {
  color: var(--color-primary);
  font-size: 1.25rem;
  font-weight: 700;
}

.data-display {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  max-height: 400px;
  overflow-y: auto;
}

.data-display pre {
  font-size: 0.875rem;
  color: #333;
  margin: 0;
  font-family: 'Courier New', monospace;
}

/* Sections */
.description-section,
.notes-section,
.next-steps {
  margin-bottom: 2rem;
  padding: 0;
  background: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.description-section h3,
.notes-section h3,
.next-steps h3 {
  background: var(--color-primary);
  color: white;
  margin: 0;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
}

.description-section p,
.notes-section p,
.step-content {
  padding: 1.5rem;
  margin: 0;
}

.description-section p,
.notes-section p,
.step-content p {
  color: #333;
  line-height: 1.7;
  font-size: 1rem;
}

.adjuster-notes {
  background: #fff9e6;
  border-left: 4px solid #ffc107;
}

.notes-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.notes-header h3 {
  margin-bottom: 0;
}

.badge {
  background: #ffc107;
  color: #856404;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.next-steps {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border: 3px solid var(--color-primary);
}

.step-content p {
  color: #004085;
  font-weight: 500;
}

/* Actions */
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
  background: #f5f7fa;
}

.btn-outline {
  background: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

.btn-outline:hover {
  background: var(--color-primary);
  color: white;
}

/* Responsive Design */
@media (max-width: 768px) {
  .claim-header {
    flex-direction: column;
    gap: 1rem;
  }

  .timeline {
    flex-direction: column;
    padding: 0;
  }

  .timeline::before {
    display: none;
  }

  .timeline-item {
    flex-direction: row;
    justify-content: flex-start;
    margin-bottom: 1.5rem;
  }

  .timeline-marker {
    margin-right: 1rem;
    margin-bottom: 0;
    width: 50px;
    height: 50px;
  }

  .marker-icon {
    font-size: 1.5rem;
  }

  .timeline-content {
    text-align: left;
  }

  .claim-info-grid {
    grid-template-columns: 1fr;
  }

  .info-item {
    flex-direction: column;
    gap: 0.25rem;
  }

  .info-item .value {
    text-align: left;
  }

  .actions {
    flex-direction: column;
  }

  .actions .btn {
    width: 100%;
    text-align: center;
  }
}

/* Compact Claim Details Styling */
.claim-details-compact {
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

.badge-yes {
  background: #d4edda;
  color: #155724;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 12px;
}

.badge-no {
  background: #f8d7da;
  color: #721c24;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 12px;
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
