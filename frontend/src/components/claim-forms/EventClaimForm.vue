<template>
  <div class="event-claim-form">
    <h3>Event Insurance Claim Details</h3>

    <div class="form-group">
      <label for="event-name">Event Name *</label>
      <input
        type="text"
        id="event-name"
        v-model="formData.event_name"
        required
        maxlength="100"
        :class="['form-control', { 'invalid': touched.event_name && !isEventNameValid }]"
        placeholder="Name of the event"
        @blur="touched.event_name = true"
      />
    </div>

    <div class="form-group">
      <label for="event-date">Event Date *</label>
      <input
        type="date"
        id="event-date"
        v-model="formData.event_date"
        required
        class="form-control"
      />
    </div>

    <div class="form-group">
      <label for="incident-type">Type of Incident *</label>
      <select id="incident-type" v-model="formData.incident_type" required class="form-control">
        <option value="">Select Incident Type</option>
        <option value="cancellation">Cancellation</option>
        <option value="postponement">Postponement</option>
        <option value="property_damage">Property Damage</option>
        <option value="liability_claim">Liability Claim</option>
        <option value="vendor_no_show">Vendor No-Show</option>
        <option value="weather">Weather</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label for="cancellation-date">Cancellation/Incident Date *</label>
      <input
        type="date"
        id="cancellation-date"
        v-model="formData.cancellation_date"
        required
        :max="maxDate"
        class="form-control"
      />
    </div>

    <div class="form-group">
      <label for="reason-description">Reason Description *</label>
      <textarea
        id="reason-description"
        v-model="formData.reason_description"
        rows="4"
        maxlength="250"
        required
        :class="['form-control', { 'invalid': touched.reason_description && !isReasonDescriptionValid }]"
        placeholder="Describe why the event was cancelled or what incident occurred"
        @blur="touched.reason_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.reason_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface EventClaimFormData {
  event_name: string
  event_date: string
  incident_type: string
  cancellation_date: string
  reason_description: string
}

const emit = defineEmits<{
  (e: 'update', data: EventClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<EventClaimFormData>({
  event_name: '',
  event_date: '',
  incident_type: '',
  cancellation_date: '',
  reason_description: ''
})

const touched = reactive({
  event_name: false,
  reason_description: false
})

const maxDate = computed(() => new Date().toISOString().split('T')[0])
const isEventNameValid = computed(() => formData.event_name.trim().length > 0)
const isReasonDescriptionValid = computed(() => formData.reason_description.trim().length >= 50)

const isFormValid = computed(() => {
  return (
    isEventNameValid.value &&
    formData.event_date !== '' &&
    formData.incident_type !== '' &&
    formData.cancellation_date !== '' &&
    isReasonDescriptionValid.value
  )
})

const charCountClass = computed(() => {
  const length = formData.reason_description.length
  if (length < 50) return 'below-min'
  if (length >= 250) return 'at-limit'
  if (length / 250 >= 0.9) return 'near-limit'
  return 'normal'
})

watch(formData, (newData) => { emit('update', { ...newData }) }, { deep: true })
watch(isFormValid, (isValid) => { emit('valid', isValid) }, { immediate: true })
</script>

<style scoped>
.event-claim-form { width: 100%; }
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
