<template>
  <div class="travel-claim-form">
    <h3>Travel Insurance Claim Details</h3>

    <div class="form-group">
      <label for="trip-destination">Trip Destination *</label>
      <input
        type="text"
        id="trip-destination"
        v-model="formData.trip_destination"
        required
        maxlength="100"
        :class="['form-control', { 'invalid': touched.trip_destination && !isTripDestinationValid }]"
        placeholder="Destination city or country"
        @blur="touched.trip_destination = true"
      />
    </div>

    <div class="form-group">
      <label for="incident-type">Type of Incident *</label>
      <select id="incident-type" v-model="formData.incident_type" required class="form-control">
        <option value="">Select Incident Type</option>
        <option value="trip_cancellation">Trip Cancellation</option>
        <option value="trip_interruption">Trip Interruption</option>
        <option value="baggage_loss">Baggage Loss</option>
        <option value="baggage_delay">Baggage Delay</option>
        <option value="medical_emergency">Medical Emergency</option>
        <option value="travel_delay">Travel Delay</option>
        <option value="missed_connection">Missed Connection</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label for="scheduled-departure">Scheduled Departure Date *</label>
      <input
        type="date"
        id="scheduled-departure"
        v-model="formData.scheduled_departure"
        required
        class="form-control"
      />
    </div>

    <div class="form-group">
      <label for="incident-date">Incident Date *</label>
      <input
        type="date"
        id="incident-date"
        v-model="formData.incident_date"
        required
        :max="maxDate"
        class="form-control"
      />
    </div>

    <div class="form-group">
      <label for="incident-description">Incident Description *</label>
      <textarea
        id="incident-description"
        v-model="formData.incident_description"
        rows="4"
        maxlength="250"
        required
        :class="['form-control', { 'invalid': touched.incident_description && !isIncidentDescriptionValid }]"
        placeholder="Describe what happened during your trip"
        @blur="touched.incident_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.incident_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface TravelClaimFormData {
  trip_destination: string
  incident_type: string
  scheduled_departure: string
  incident_date: string
  incident_description: string
}

const emit = defineEmits<{
  (e: 'update', data: TravelClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<TravelClaimFormData>({
  trip_destination: '',
  incident_type: '',
  scheduled_departure: '',
  incident_date: '',
  incident_description: ''
})

const touched = reactive({
  trip_destination: false,
  incident_description: false
})

const maxDate = computed(() => new Date().toISOString().split('T')[0])
const isTripDestinationValid = computed(() => formData.trip_destination.trim().length > 0)
const isIncidentDescriptionValid = computed(() => formData.incident_description.trim().length >= 50)

const isFormValid = computed(() => {
  return (
    isTripDestinationValid.value &&
    formData.incident_type !== '' &&
    formData.scheduled_departure !== '' &&
    formData.incident_date !== '' &&
    isIncidentDescriptionValid.value
  )
})

const charCountClass = computed(() => {
  const length = formData.incident_description.length
  if (length < 50) return 'below-min'
  if (length >= 250) return 'at-limit'
  if (length / 250 >= 0.9) return 'near-limit'
  return 'normal'
})

watch(formData, (newData) => { emit('update', { ...newData }) }, { deep: true })
watch(isFormValid, (isValid) => { emit('valid', isValid) }, { immediate: true })
</script>

<style scoped>
.travel-claim-form { width: 100%; }
h3 { color: var(--color-primary, var(--color-primary)); font-size: 1.3rem; margin-bottom: 1.5rem; }
.form-group { margin-bottom: 1.5rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: 600; color: #333; }
.form-control { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; transition: border-color 0.3s; }
.form-control:focus { outline: none; border-color: var(--color-primary, var(--color-primary)); }
.form-control.invalid { border-color: #dc3545; border-width: 2px; }
.form-control.invalid:focus { border-color: #dc3545; box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25); }
select.form-control { cursor: pointer; }
textarea.form-control { resize: vertical; min-height: 100px; font-family: inherit; }
small { color: #666; font-size: 0.875rem; display: block; margin-top: 0.25rem; }
small.normal { color: #666; }
small.below-min { color: #ff9800; font-weight: 600; }
small.below-min::after { content: ' (minimum 50 characters)'; }
small.near-limit { color: #ff9800; font-weight: 600; }
small.at-limit { color: #f44336; font-weight: 600; }
</style>
