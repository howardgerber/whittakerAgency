<template>
  <div class="life-claim-form">
    <h3>Life Insurance Claim Details</h3>
    <p class="compassionate-message">We understand this is a difficult time. Please provide basic information to help us prepare for your visit.</p>

    <div class="form-group">
      <label for="claim-type">Claim Type *</label>
      <select id="claim-type" v-model="formData.claim_type" required class="form-control">
        <option value="">Select Claim Type</option>
        <option value="death_of_insured">Death of Insured</option>
        <option value="terminal_illness">Terminal Illness Diagnosis</option>
        <option value="critical_illness">Critical Illness Diagnosis</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label for="date-of-event">Date of Death/Diagnosis *</label>
      <input
        type="date"
        id="date-of-event"
        v-model="formData.date_of_event"
        required
        :max="maxDate"
        class="form-control"
      />
    </div>

    <div class="form-group">
      <label for="physician-name">Physician Name</label>
      <input
        type="text"
        id="physician-name"
        v-model="formData.physician_name"
        maxlength="100"
        class="form-control"
        placeholder="Optional"
      />
    </div>

    <div class="form-group">
      <label for="medical-facility">Medical Facility</label>
      <input
        type="text"
        id="medical-facility"
        v-model="formData.medical_facility"
        maxlength="100"
        class="form-control"
        placeholder="Optional"
      />
    </div>

    <div class="form-group">
      <label for="brief-description">Brief Description *</label>
      <textarea
        id="brief-description"
        v-model="formData.brief_description"
        rows="4"
        maxlength="250"
        required
        :class="['form-control', { 'invalid': touched.brief_description && !isBriefDescriptionValid }]"
        placeholder="Brief description of the situation"
        @blur="touched.brief_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.brief_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface LifeClaimFormData {
  claim_type: string
  date_of_event: string
  physician_name: string
  medical_facility: string
  brief_description: string
}

const emit = defineEmits<{
  (e: 'update', data: LifeClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<LifeClaimFormData>({
  claim_type: '',
  date_of_event: '',
  physician_name: '',
  medical_facility: '',
  brief_description: ''
})

const touched = reactive({
  brief_description: false
})

const maxDate = computed(() => new Date().toISOString().split('T')[0])
const isBriefDescriptionValid = computed(() => formData.brief_description.trim().length >= 50)

const isFormValid = computed(() => {
  return (
    formData.claim_type !== '' &&
    formData.date_of_event !== '' &&
    isBriefDescriptionValid.value
  )
})

const charCountClass = computed(() => {
  const length = formData.brief_description.length
  if (length < 50) return 'below-min'
  if (length >= 250) return 'at-limit'
  if (length / 250 >= 0.9) return 'near-limit'
  return 'normal'
})

watch(formData, (newData) => { emit('update', { ...newData }) }, { deep: true })
watch(isFormValid, (isValid) => { emit('valid', isValid) }, { immediate: true })
</script>

<style scoped>
.life-claim-form { width: 100%; }
h3 { color: var(--color-primary, var(--color-primary)); font-size: 1.3rem; margin-bottom: 0.5rem; }
.compassionate-message { color: #666; font-size: 0.95rem; margin-bottom: 1.5rem; line-height: 1.5; }
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
