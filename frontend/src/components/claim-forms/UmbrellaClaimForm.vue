<template>
  <div class="umbrella-claim-form">
    <h3>Personal Umbrella Policy Claim Details</h3>

    <div class="form-group">
      <label for="underlying-incident-type">Underlying Incident Type *</label>
      <select id="underlying-incident-type" v-model="formData.underlying_incident_type" required class="form-control">
        <option value="">Select Underlying Incident Type</option>
        <option value="auto_liability">Auto Liability</option>
        <option value="home_liability">Home Liability</option>
        <option value="boat_liability">Boat Liability</option>
        <option value="business_liability">Business Liability</option>
        <option value="other_liability">Other Liability</option>
      </select>
    </div>

    <div class="form-group">
      <label>Primary Insurance Claim Filed? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.primary_insurance_claim_filed" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.primary_insurance_claim_filed" value="no" /> No</label>
      </div>
    </div>

    <div v-if="formData.primary_insurance_claim_filed === 'yes'" class="conditional-section">
      <h4>Primary Insurance Information</h4>
      <div class="form-group">
        <label for="primary-insurance-company">Primary Insurance Company *</label>
        <input
          type="text"
          id="primary-insurance-company"
          v-model="formData.primary_insurance_company"
          :required="formData.primary_insurance_claim_filed === 'yes'"
          maxlength="100"
          :class="['form-control', { 'invalid': touched.primary_insurance_company && !isPrimaryInsuranceCompanyValid }]"
          @blur="touched.primary_insurance_company = true"
        />
      </div>
    </div>

    <div class="form-group">
      <label>Third Party Involved? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.third_party_involved" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.third_party_involved" value="no" /> No</label>
      </div>
    </div>

    <div class="form-group">
      <label>Lawsuit Filed? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.lawsuit_filed" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.lawsuit_filed" value="no" /> No</label>
      </div>
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
        placeholder="Describe the liability incident"
        @blur="touched.incident_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.incident_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface UmbrellaClaimFormData {
  underlying_incident_type: string
  primary_insurance_claim_filed: string
  primary_insurance_company: string
  third_party_involved: string
  lawsuit_filed: string
  incident_description: string
}

const emit = defineEmits<{
  (e: 'update', data: UmbrellaClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<UmbrellaClaimFormData>({
  underlying_incident_type: '',
  primary_insurance_claim_filed: '',
  primary_insurance_company: '',
  third_party_involved: '',
  lawsuit_filed: '',
  incident_description: ''
})

const touched = reactive({
  primary_insurance_company: false,
  incident_description: false
})

const isPrimaryInsuranceCompanyValid = computed(() => {
  if (formData.primary_insurance_claim_filed !== 'yes') return true
  return formData.primary_insurance_company.trim().length > 0
})
const isIncidentDescriptionValid = computed(() => formData.incident_description.trim().length >= 50)

const isFormValid = computed(() => {
  const baseValid = (
    formData.underlying_incident_type !== '' &&
    formData.primary_insurance_claim_filed !== '' &&
    formData.third_party_involved !== '' &&
    formData.lawsuit_filed !== '' &&
    isIncidentDescriptionValid.value
  )
  if (formData.primary_insurance_claim_filed === 'yes' && !isPrimaryInsuranceCompanyValid.value) return false
  return baseValid
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
.umbrella-claim-form { width: 100%; }
h3 { color: var(--color-primary, var(--color-primary)); font-size: 1.3rem; margin-bottom: 1.5rem; }
h4 { color: var(--color-primary); font-size: 1.1rem; margin-bottom: 1rem; margin-top: 0; }
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
.conditional-section { background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary); }
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
