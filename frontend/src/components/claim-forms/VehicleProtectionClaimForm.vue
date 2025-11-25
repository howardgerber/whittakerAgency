<template>
  <div class="vehicle-protection-claim-form">
    <h3>Vehicle Protection Claim Details</h3>

    <div class="form-group">
      <label for="issue-type">Type of Issue *</label>
      <select id="issue-type" v-model="formData.issue_type" required class="form-control">
        <option value="">Select Issue Type</option>
        <option value="mechanical_breakdown">Mechanical Breakdown</option>
        <option value="engine_failure">Engine Failure</option>
        <option value="transmission_failure">Transmission Failure</option>
        <option value="electrical_issue">Electrical Issue</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label for="current-mileage">Current Mileage *</label>
      <input
        type="number"
        id="current-mileage"
        v-model.number="formData.current_mileage"
        required
        min="0"
        :class="['form-control', { 'invalid': touched.current_mileage && !isCurrentMileageValid }]"
        placeholder="e.g., 75000"
        @blur="touched.current_mileage = true"
      />
    </div>

    <div class="form-group">
      <label for="warning-signs">Warning Signs Before Failure</label>
      <textarea
        id="warning-signs"
        v-model="formData.warning_signs"
        rows="3"
        maxlength="250"
        class="form-control"
        placeholder="Describe any warning signs before the failure (optional)"
      ></textarea>
      <small class="normal">{{ formData.warning_signs.length }}/250 characters</small>
    </div>

    <div class="form-group">
      <label>Vehicle Currently Operable? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.vehicle_operable" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.vehicle_operable" value="no" /> No</label>
      </div>
    </div>

    <div class="form-group">
      <label for="issue-description">Issue Description *</label>
      <textarea
        id="issue-description"
        v-model="formData.issue_description"
        rows="4"
        maxlength="250"
        required
        :class="['form-control', { 'invalid': touched.issue_description && !isIssueDescriptionValid }]"
        placeholder="Describe the mechanical issue in detail"
        @blur="touched.issue_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.issue_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface VehicleProtectionClaimFormData {
  issue_type: string
  current_mileage: number | null
  warning_signs: string
  vehicle_operable: string
  issue_description: string
}

const emit = defineEmits<{
  (e: 'update', data: VehicleProtectionClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<VehicleProtectionClaimFormData>({
  issue_type: '',
  current_mileage: null,
  warning_signs: '',
  vehicle_operable: '',
  issue_description: ''
})

const touched = reactive({
  current_mileage: false,
  issue_description: false
})

const isCurrentMileageValid = computed(() => {
  return formData.current_mileage !== null && formData.current_mileage >= 0
})
const isIssueDescriptionValid = computed(() => formData.issue_description.trim().length >= 50)

const isFormValid = computed(() => {
  return (
    formData.issue_type !== '' &&
    isCurrentMileageValid.value &&
    formData.vehicle_operable !== '' &&
    isIssueDescriptionValid.value
  )
})

const charCountClass = computed(() => {
  const length = formData.issue_description.length
  if (length < 50) return 'below-min'
  if (length >= 250) return 'at-limit'
  if (length / 250 >= 0.9) return 'near-limit'
  return 'normal'
})

watch(formData, (newData) => { emit('update', { ...newData }) }, { deep: true })
watch(isFormValid, (isValid) => { emit('valid', isValid) }, { immediate: true })
</script>

<style scoped>
.vehicle-protection-claim-form { width: 100%; }
h3 { color: var(--color-primary, var(--color-primary)); font-size: 1.3rem; margin-bottom: 1.5rem; }
.form-group { margin-bottom: 1.5rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: 600; color: #333; }
.form-control { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; transition: border-color 0.3s; }
.form-control:focus { outline: none; border-color: var(--color-primary, var(--color-primary)); }
.form-control.invalid { border-color: #dc3545; border-width: 2px; }
.form-control.invalid:focus { border-color: #dc3545; box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25); }
select.form-control { cursor: pointer; }
textarea.form-control { resize: vertical; min-height: 100px; font-family: inherit; }
.radio-group { display: flex; gap: 1.5rem; margin-top: 0.5rem; }
.radio-label { display: flex; align-items: center; gap: 0.5rem; font-weight: 400; cursor: pointer; }
.radio-label input[type="radio"] { width: 18px; height: 18px; cursor: pointer; }
small { color: #666; font-size: 0.875rem; display: block; margin-top: 0.25rem; }
small.normal { color: #666; }
small.below-min { color: #ff9800; font-weight: 600; }
small.below-min::after { content: ' (minimum 50 characters)'; }
small.near-limit { color: #ff9800; font-weight: 600; }
small.at-limit { color: #f44336; font-weight: 600; }
@media (max-width: 768px) {
  .radio-group { flex-direction: column; gap: 0.75rem; }
}
</style>
