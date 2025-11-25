<template>
  <div class="condo-claim-form">
    <h3>Condo Insurance Claim Details</h3>

    <div class="form-group">
      <label for="incident-type">Type of Incident *</label>
      <select id="incident-type" v-model="formData.incident_type" required class="form-control">
        <option value="">Select Incident Type</option>
        <option value="fire">Fire</option>
        <option value="water_damage">Water Damage</option>
        <option value="wind_damage">Wind Damage</option>
        <option value="theft">Theft</option>
        <option value="vandalism">Vandalism</option>
        <option value="liability_claim">Liability Claim</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label>Area Affected *</label>
      <div class="checkbox-group">
        <label class="checkbox-label"><input type="checkbox" v-model="formData.area_affected" value="unit_interior" /> Unit Interior</label>
        <label class="checkbox-label"><input type="checkbox" v-model="formData.area_affected" value="balcony_patio" /> Balcony/Patio</label>
        <label class="checkbox-label"><input type="checkbox" v-model="formData.area_affected" value="personal_property" /> Personal Property</label>
        <label class="checkbox-label"><input type="checkbox" v-model="formData.area_affected" value="common_area" /> Common Area</label>
        <label class="checkbox-label"><input type="checkbox" v-model="formData.area_affected" value="other" /> Other</label>
      </div>
      <small v-if="touched.area_affected && !isAreaAffectedValid" class="below-min">Please select at least one area</small>
    </div>

    <div class="form-group">
      <label for="damage-extent">Extent of Damage *</label>
      <select id="damage-extent" v-model="formData.damage_extent" required class="form-control">
        <option value="">Select Damage Extent</option>
        <option value="minor">Minor</option>
        <option value="moderate">Moderate</option>
        <option value="severe">Severe</option>
        <option value="catastrophic">Catastrophic</option>
      </select>
    </div>

    <div class="form-group">
      <label>HOA Notified? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.hoa_notified" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.hoa_notified" value="no" /> No</label>
      </div>
    </div>

    <div class="form-group">
      <label>Common Area Issue? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.common_area_issue" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.common_area_issue" value="no" /> No</label>
      </div>
    </div>

    <div class="form-group">
      <label>Currently Living in Unit? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.currently_living_in_unit" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.currently_living_in_unit" value="no" /> No</label>
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
        placeholder="Describe the damage to your condo unit"
        @blur="touched.damage_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.damage_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface CondoClaimFormData {
  incident_type: string
  area_affected: string[]
  damage_extent: string
  hoa_notified: string
  common_area_issue: string
  currently_living_in_unit: string
  damage_description: string
}

const emit = defineEmits<{
  (e: 'update', data: CondoClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<CondoClaimFormData>({
  incident_type: '',
  area_affected: [],
  damage_extent: '',
  hoa_notified: '',
  common_area_issue: '',
  currently_living_in_unit: '',
  damage_description: ''
})

const touched = reactive({
  area_affected: false,
  damage_description: false
})

const isAreaAffectedValid = computed(() => formData.area_affected.length > 0)
const isDamageDescriptionValid = computed(() => formData.damage_description.trim().length >= 50)

const isFormValid = computed(() => {
  return (
    formData.incident_type !== '' &&
    isAreaAffectedValid.value &&
    formData.damage_extent !== '' &&
    formData.hoa_notified !== '' &&
    formData.common_area_issue !== '' &&
    formData.currently_living_in_unit !== '' &&
    isDamageDescriptionValid.value
  )
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
.condo-claim-form { width: 100%; }
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
.checkbox-group { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 0.75rem; margin-top: 0.5rem; }
.checkbox-label { display: flex; align-items: center; gap: 0.5rem; font-weight: 400; cursor: pointer; }
.checkbox-label input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; }
small { color: #666; font-size: 0.875rem; display: block; margin-top: 0.25rem; }
small.normal { color: #666; }
small.below-min { color: #ff9800; font-weight: 600; }
small.below-min::after { content: ' (minimum 50 characters)'; }
small.near-limit { color: #ff9800; font-weight: 600; }
small.at-limit { color: #f44336; font-weight: 600; }
@media (max-width: 768px) {
  .radio-group { flex-direction: column; gap: 0.75rem; }
  .checkbox-group { grid-template-columns: 1fr; }
}
</style>
