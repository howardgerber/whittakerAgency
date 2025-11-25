<template>
  <div class="boat-claim-form">
    <h3>Boat Insurance Claim Details</h3>

    <div class="form-group">
      <label for="incident-type">Type of Incident *</label>
      <select id="incident-type" v-model="formData.incident_type" required class="form-control">
        <option value="">Select Incident Type</option>
        <option value="collision_vessel">Collision with Vessel</option>
        <option value="collision_object">Collision with Object</option>
        <option value="sinking">Sinking</option>
        <option value="fire">Fire</option>
        <option value="theft">Theft</option>
        <option value="vandalism">Vandalism</option>
        <option value="weather_damage">Weather Damage</option>
        <option value="grounding">Grounding</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label for="incident-location">Incident Location *</label>
      <select id="incident-location" v-model="formData.incident_location" required class="form-control">
        <option value="">Select Location Type</option>
        <option value="lake">Lake</option>
        <option value="river">River</option>
        <option value="ocean">Ocean</option>
        <option value="marina">Marina</option>
        <option value="storage_facility">Storage Facility</option>
        <option value="trailer">Trailer</option>
      </select>
    </div>

    <div class="form-group">
      <label for="water-conditions">Water Conditions *</label>
      <select id="water-conditions" v-model="formData.water_conditions" required class="form-control">
        <option value="">Select Water Conditions</option>
        <option value="calm">Calm</option>
        <option value="moderate">Moderate</option>
        <option value="rough">Rough</option>
        <option value="storm">Storm</option>
      </select>
    </div>

    <div class="form-group">
      <label>Was Another Vessel Involved? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.other_vessel_involved" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.other_vessel_involved" value="no" /> No</label>
      </div>
    </div>

    <div v-if="formData.other_vessel_involved === 'yes'" class="conditional-section">
      <h4>Other Vessel Information</h4>
      <div class="form-group">
        <label for="other-vessel-operator">Other Vessel Operator Name *</label>
        <input
          type="text"
          id="other-vessel-operator"
          v-model="formData.other_vessel_operator"
          :required="formData.other_vessel_involved === 'yes'"
          :class="['form-control', { 'invalid': touched.other_vessel_operator && !isOtherVesselOperatorValid }]"
          placeholder="First Last"
          @blur="touched.other_vessel_operator = true"
        />
      </div>
      <div class="form-group">
        <label for="other-vessel-registration">Other Vessel Registration</label>
        <input type="text" id="other-vessel-registration" v-model="formData.other_vessel_registration" maxlength="50" class="form-control" />
      </div>
    </div>

    <div class="form-group">
      <label>Coast Guard Report Filed? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.coast_guard_report_filed" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.coast_guard_report_filed" value="no" /> No</label>
      </div>
    </div>

    <div v-if="formData.coast_guard_report_filed === 'yes'" class="conditional-section">
      <h4>Coast Guard Report Information</h4>
      <div class="form-group">
        <label for="coast-guard-report-number">Report Number *</label>
        <input
          type="text"
          id="coast-guard-report-number"
          v-model="formData.coast_guard_report_number"
          :required="formData.coast_guard_report_filed === 'yes'"
          maxlength="50"
          :class="['form-control', { 'invalid': touched.coast_guard_report_number && !isCoastGuardReportNumberValid }]"
          @blur="touched.coast_guard_report_number = true"
        />
      </div>
    </div>

    <div class="form-group">
      <label>Is the Boat Operational? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.boat_operational" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.boat_operational" value="no" /> No</label>
      </div>
    </div>

    <div class="form-group">
      <label for="damage-description">Damage Description *</label>
      <textarea
        id="damage-description"
        v-model="formData.damage_description"
        rows="4"
        maxlength="250"
        required
        :class="['form-control', { 'invalid': touched.damage_description && !isDamageDescriptionValid }]"
        placeholder="Describe the damage to your boat"
        @blur="touched.damage_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.damage_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import { ValidationRules } from '@/utils/validation'

interface BoatClaimFormData {
  incident_type: string
  incident_location: string
  water_conditions: string
  other_vessel_involved: string
  other_vessel_operator: string
  other_vessel_registration: string
  coast_guard_report_filed: string
  coast_guard_report_number: string
  boat_operational: string
  damage_description: string
}

const emit = defineEmits<{
  (e: 'update', data: BoatClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<BoatClaimFormData>({
  incident_type: '',
  incident_location: '',
  water_conditions: '',
  other_vessel_involved: '',
  other_vessel_operator: '',
  other_vessel_registration: '',
  coast_guard_report_filed: '',
  coast_guard_report_number: '',
  boat_operational: '',
  damage_description: ''
})

const touched = reactive({
  other_vessel_operator: false,
  coast_guard_report_number: false,
  damage_description: false
})

const isOtherVesselOperatorValid = computed(() => {
  if (formData.other_vessel_involved !== 'yes') return true
  if (!formData.other_vessel_operator.trim()) return false
  return ValidationRules.fullName.validate(formData.other_vessel_operator).isValid
})
const isCoastGuardReportNumberValid = computed(() => {
  if (formData.coast_guard_report_filed !== 'yes') return true
  return formData.coast_guard_report_number.trim().length > 0
})
const isDamageDescriptionValid = computed(() => formData.damage_description.trim().length >= 50)

const isFormValid = computed(() => {
  const baseValid = (
    formData.incident_type !== '' &&
    formData.incident_location !== '' &&
    formData.water_conditions !== '' &&
    formData.other_vessel_involved !== '' &&
    formData.coast_guard_report_filed !== '' &&
    formData.boat_operational !== '' &&
    isDamageDescriptionValid.value
  )
  if (formData.other_vessel_involved === 'yes' && !isOtherVesselOperatorValid.value) return false
  if (formData.coast_guard_report_filed === 'yes' && !isCoastGuardReportNumberValid.value) return false
  return baseValid
})

const charCountClass = computed(() => {
  const length = formData.damage_description.length
  if (length < 50) return 'below-min'
  if (length >= 250) return 'at-limit'
  if (length / 250 >= 0.9) return 'near-limit'
  return 'normal'
})

watch(formData, (newData) => { emit('update', { ...newData }) }, { deep: true })
watch(isFormValid, (isValid) => { emit('valid', isValid) }, { immediate: true })
</script>

<style scoped>
.boat-claim-form { width: 100%; }
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
