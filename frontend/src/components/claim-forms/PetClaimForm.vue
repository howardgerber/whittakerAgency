<template>
  <div class="pet-claim-form">
    <h3>Pet Insurance Claim Details</h3>

    <div class="form-group">
      <label for="pet-name">Pet Name *</label>
      <input
        type="text"
        id="pet-name"
        v-model="formData.pet_name"
        required
        maxlength="50"
        :class="['form-control', { 'invalid': touched.pet_name && !isPetNameValid }]"
        placeholder="Your pet's name"
        @blur="touched.pet_name = true"
      />
    </div>

    <div class="form-group">
      <label for="incident-type">Type of Incident *</label>
      <select id="incident-type" v-model="formData.incident_type" required class="form-control">
        <option value="">Select Incident Type</option>
        <option value="illness">Illness</option>
        <option value="injury">Injury</option>
        <option value="surgery">Surgery</option>
        <option value="emergency_care">Emergency Care</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label for="treatment-date">Treatment Date *</label>
      <input
        type="date"
        id="treatment-date"
        v-model="formData.treatment_date"
        required
        :max="maxDate"
        class="form-control"
      />
    </div>

    <div class="form-group">
      <label for="veterinary-clinic">Veterinary Clinic *</label>
      <input
        type="text"
        id="veterinary-clinic"
        v-model="formData.veterinary_clinic"
        required
        maxlength="100"
        :class="['form-control', { 'invalid': touched.veterinary_clinic && !isVeterinaryClinicValid }]"
        placeholder="Clinic name"
        @blur="touched.veterinary_clinic = true"
      />
    </div>

    <div class="form-group">
      <label for="treatment-description">Treatment Description *</label>
      <textarea
        id="treatment-description"
        v-model="formData.treatment_description"
        rows="4"
        maxlength="250"
        required
        :class="['form-control', { 'invalid': touched.treatment_description && !isTreatmentDescriptionValid }]"
        placeholder="Describe the treatment your pet received"
        @blur="touched.treatment_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.treatment_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface PetClaimFormData {
  pet_name: string
  incident_type: string
  treatment_date: string
  veterinary_clinic: string
  treatment_description: string
}

const emit = defineEmits<{
  (e: 'update', data: PetClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<PetClaimFormData>({
  pet_name: '',
  incident_type: '',
  treatment_date: '',
  veterinary_clinic: '',
  treatment_description: ''
})

const touched = reactive({
  pet_name: false,
  veterinary_clinic: false,
  treatment_description: false
})

const maxDate = computed(() => new Date().toISOString().split('T')[0])
const isPetNameValid = computed(() => formData.pet_name.trim().length > 0)
const isVeterinaryClinicValid = computed(() => formData.veterinary_clinic.trim().length > 0)
const isTreatmentDescriptionValid = computed(() => formData.treatment_description.trim().length >= 50)

const isFormValid = computed(() => {
  return (
    isPetNameValid.value &&
    formData.incident_type !== '' &&
    formData.treatment_date !== '' &&
    isVeterinaryClinicValid.value &&
    isTreatmentDescriptionValid.value
  )
})

const charCountClass = computed(() => {
  const length = formData.treatment_description.length
  if (length < 50) return 'below-min'
  if (length >= 250) return 'at-limit'
  if (length / 250 >= 0.9) return 'near-limit'
  return 'normal'
})

watch(formData, (newData) => { emit('update', { ...newData }) }, { deep: true })
watch(isFormValid, (isValid) => { emit('valid', isValid) }, { immediate: true })
</script>

<style scoped>
.pet-claim-form { width: 100%; }
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
