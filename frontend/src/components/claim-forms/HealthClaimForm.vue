<template>
  <div class="health-claim-form">
    <h3>Individual Health Insurance Claim Details</h3>

    <div class="form-group">
      <label for="service-type">Service Type *</label>
      <select id="service-type" v-model="formData.service_type" required class="form-control">
        <option value="">Select Service Type</option>
        <option value="medical_procedure">Medical Procedure</option>
        <option value="hospital_stay">Hospital Stay</option>
        <option value="emergency_care">Emergency Care</option>
        <option value="prescription">Prescription</option>
        <option value="medical_equipment">Medical Equipment</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label for="service-date">Service Date *</label>
      <input
        type="date"
        id="service-date"
        v-model="formData.service_date"
        required
        :max="maxDate"
        class="form-control"
      />
    </div>

    <div class="form-group">
      <label for="healthcare-provider">Healthcare Provider *</label>
      <input
        type="text"
        id="healthcare-provider"
        v-model="formData.healthcare_provider"
        required
        maxlength="100"
        :class="['form-control', { 'invalid': touched.healthcare_provider && !isHealthcareProviderValid }]"
        placeholder="Provider name"
        @blur="touched.healthcare_provider = true"
      />
    </div>

    <div class="form-group">
      <label for="provider-type">Provider Type *</label>
      <select id="provider-type" v-model="formData.provider_type" required class="form-control">
        <option value="">Select Provider Type</option>
        <option value="hospital">Hospital</option>
        <option value="clinic">Clinic</option>
        <option value="doctors_office">Doctor's Office</option>
        <option value="urgent_care">Urgent Care</option>
        <option value="emergency_room">Emergency Room</option>
        <option value="pharmacy">Pharmacy</option>
        <option value="other">Other</option>
      </select>
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
        placeholder="Describe the medical service received"
        @blur="touched.service_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.service_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface HealthClaimFormData {
  service_type: string
  service_date: string
  healthcare_provider: string
  provider_type: string
  service_description: string
}

const emit = defineEmits<{
  (e: 'update', data: HealthClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<HealthClaimFormData>({
  service_type: '',
  service_date: '',
  healthcare_provider: '',
  provider_type: '',
  service_description: ''
})

const touched = reactive({
  healthcare_provider: false,
  service_description: false
})

const maxDate = computed(() => new Date().toISOString().split('T')[0])
const isHealthcareProviderValid = computed(() => formData.healthcare_provider.trim().length > 0)
const isServiceDescriptionValid = computed(() => formData.service_description.trim().length >= 50)

const isFormValid = computed(() => {
  return (
    formData.service_type !== '' &&
    formData.service_date !== '' &&
    isHealthcareProviderValid.value &&
    formData.provider_type !== '' &&
    isServiceDescriptionValid.value
  )
})

const charCountClass = computed(() => {
  const length = formData.service_description.length
  if (length < 50) return 'below-min'
  if (length >= 250) return 'at-limit'
  if (length / 250 >= 0.9) return 'near-limit'
  return 'normal'
})

watch(formData, (newData) => { emit('update', { ...newData }) }, { deep: true })
watch(isFormValid, (isValid) => { emit('valid', isValid) }, { immediate: true })
</script>

<style scoped>
.health-claim-form { width: 100%; }
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
