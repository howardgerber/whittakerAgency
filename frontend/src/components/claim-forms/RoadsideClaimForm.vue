<template>
  <div class="roadside-claim-form">
    <h3>Roadside Assistance Claim Details</h3>

    <div class="form-group">
      <label for="service-type">Type of Service *</label>
      <select
        id="service-type"
        v-model="formData.service_type"
        required
        class="form-control"
      >
        <option value="">Select Service Type</option>
        <option value="flat_tire">Flat Tire</option>
        <option value="dead_battery">Dead Battery</option>
        <option value="lockout">Lockout</option>
        <option value="out_of_fuel">Out of Fuel</option>
        <option value="tow_needed">Tow Needed</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label for="service-location">Service Location *</label>
      <input
        type="text"
        id="service-location"
        v-model="formData.service_location"
        required
        maxlength="250"
        :class="['form-control', { 'invalid': touched.service_location && !isServiceLocationValid }]"
        placeholder="Street address or general location"
        @blur="touched.service_location = true"
      />
    </div>

    <div class="form-group">
      <label for="service-date">Service Date/Time *</label>
      <input
        type="datetime-local"
        id="service-date"
        v-model="formData.service_date"
        required
        :max="maxDateTime"
        class="form-control"
      />
    </div>

    <div class="form-group">
      <label for="service-provider">Service Provider</label>
      <input
        type="text"
        id="service-provider"
        v-model="formData.service_provider"
        maxlength="100"
        class="form-control"
        placeholder="e.g., AAA, Tow Company Name"
      />
    </div>

    <div class="form-group">
      <label for="service-description">Service Description *</label>
      <textarea
        id="service-description"
        v-model="formData.service_description"
        rows="4"
        maxlength="250"
        required
        :class="['form-control', { 'invalid': touched.service_description && !isServiceDescriptionValid }]"
        placeholder="Describe the service that was provided or is needed"
        @blur="touched.service_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.service_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface RoadsideClaimFormData {
  service_type: string
  service_location: string
  service_date: string
  service_provider: string
  service_description: string
}

const emit = defineEmits<{
  (e: 'update', data: RoadsideClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<RoadsideClaimFormData>({
  service_type: '',
  service_location: '',
  service_date: '',
  service_provider: '',
  service_description: ''
})

const touched = reactive({
  service_location: false,
  service_description: false
})

// Max datetime is now
const maxDateTime = computed(() => {
  const now = new Date()
  return now.toISOString().slice(0, 16)
})

// Validation computed properties
const isServiceLocationValid = computed(() => {
  const trimmed = formData.service_location.trim()
  return trimmed.length >= 3
})

const isServiceDescriptionValid = computed(() => {
  return formData.service_description.trim().length >= 50
})

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  return (
    formData.service_type !== '' &&
    isServiceLocationValid.value &&
    formData.service_date !== '' &&
    isServiceDescriptionValid.value
  )
})

// Character count styling
const charCountClass = computed(() => {
  const length = formData.service_description.length
  const min = 50
  const max = 250

  if (length < min) return 'below-min'
  if (length >= max) return 'at-limit'
  if (length / max >= 0.9) return 'near-limit'
  return 'normal'
})

// Watch for changes and emit to parent
watch(formData, (newData) => {
  emit('update', { ...newData })
}, { deep: true })

watch(isFormValid, (isValid) => {
  emit('valid', isValid)
}, { immediate: true })
</script>

<style scoped>
.roadside-claim-form {
  width: 100%;
}

h3 {
  color: var(--color-primary, var(--color-primary));
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: var(--color-primary, var(--color-primary));
}

.form-control.invalid {
  border-color: #dc3545;
  border-width: 2px;
}

.form-control.invalid:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

select.form-control {
  cursor: pointer;
}

textarea.form-control {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

small {
  color: #666;
  font-size: 0.875rem;
  display: block;
  margin-top: 0.25rem;
}

small.normal {
  color: #666;
}

small.below-min {
  color: #ff9800;
  font-weight: 600;
}

small.below-min::after {
  content: ' (minimum 50 characters)';
}

small.near-limit {
  color: #ff9800;
  font-weight: 600;
}

small.at-limit {
  color: #f44336;
  font-weight: 600;
}
</style>
