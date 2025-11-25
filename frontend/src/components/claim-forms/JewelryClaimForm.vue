<template>
  <div class="jewelry-claim-form">
    <h3>Jewelry Insurance Claim Details</h3>

    <div class="form-group">
      <label for="number-of-items">Number of Items Affected *</label>
      <select id="number-of-items" v-model="formData.number_of_items" required class="form-control">
        <option value="">Select Number of Items</option>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5+">5+</option>
      </select>
    </div>

    <div class="form-group">
      <label for="incident-type">Type of Incident *</label>
      <select id="incident-type" v-model="formData.incident_type" required class="form-control">
        <option value="">Select Incident Type</option>
        <option value="theft">Theft</option>
        <option value="loss">Loss</option>
        <option value="damage">Damage</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label for="incident-location">Location of Incident *</label>
      <input
        type="text"
        id="incident-location"
        v-model="formData.incident_location"
        required
        maxlength="250"
        :class="['form-control', { 'invalid': touched.incident_location && !isIncidentLocationValid }]"
        placeholder="Where the incident occurred"
        @blur="touched.incident_location = true"
      />
    </div>

    <div class="form-group">
      <label>Police Report Filed? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.police_report_filed" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.police_report_filed" value="no" /> No</label>
      </div>
    </div>

    <div v-if="formData.police_report_filed === 'yes'" class="conditional-section">
      <h4>Police Report Information</h4>
      <div class="form-group">
        <label for="police-report-number">Report Number *</label>
        <input
          type="text"
          id="police-report-number"
          v-model="formData.police_report_number"
          :required="formData.police_report_filed === 'yes'"
          maxlength="50"
          :class="['form-control', { 'invalid': touched.police_report_number && !isPoliceReportNumberValid }]"
          @blur="touched.police_report_number = true"
        />
      </div>
      <div class="form-group">
        <label for="police-department">Police Department *</label>
        <input
          type="text"
          id="police-department"
          v-model="formData.police_department"
          :required="formData.police_report_filed === 'yes'"
          maxlength="100"
          :class="['form-control', { 'invalid': touched.police_department && !isPoliceDepartmentValid }]"
          @blur="touched.police_department = true"
        />
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
        placeholder="Describe the incident and jewelry items affected"
        @blur="touched.incident_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.incident_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface JewelryClaimFormData {
  number_of_items: string
  incident_type: string
  incident_location: string
  police_report_filed: string
  police_report_number: string
  police_department: string
  incident_description: string
}

const emit = defineEmits<{
  (e: 'update', data: JewelryClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<JewelryClaimFormData>({
  number_of_items: '',
  incident_type: '',
  incident_location: '',
  police_report_filed: '',
  police_report_number: '',
  police_department: '',
  incident_description: ''
})

const touched = reactive({
  incident_location: false,
  police_report_number: false,
  police_department: false,
  incident_description: false
})

const isIncidentLocationValid = computed(() => formData.incident_location.trim().length >= 3)
const isPoliceReportNumberValid = computed(() => {
  if (formData.police_report_filed !== 'yes') return true
  return formData.police_report_number.trim().length > 0
})
const isPoliceDepartmentValid = computed(() => {
  if (formData.police_report_filed !== 'yes') return true
  return formData.police_department.trim().length > 0
})
const isIncidentDescriptionValid = computed(() => formData.incident_description.trim().length >= 50)

const isFormValid = computed(() => {
  const baseValid = (
    formData.number_of_items !== '' &&
    formData.incident_type !== '' &&
    isIncidentLocationValid.value &&
    formData.police_report_filed !== '' &&
    isIncidentDescriptionValid.value
  )
  if (formData.police_report_filed === 'yes' && (!isPoliceReportNumberValid.value || !isPoliceDepartmentValid.value)) return false
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
.jewelry-claim-form { width: 100%; }
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
