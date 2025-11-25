<template>
  <div class="landlord-claim-form">
    <h3>Landlord Insurance Claim Details</h3>

    <div class="form-group">
      <label for="incident-type">Type of Incident *</label>
      <select id="incident-type" v-model="formData.incident_type" required class="form-control">
        <option value="">Select Incident Type</option>
        <option value="fire">Fire</option>
        <option value="water_damage">Water Damage</option>
        <option value="wind_damage">Wind Damage</option>
        <option value="tenant_damage">Tenant Damage</option>
        <option value="vandalism">Vandalism</option>
        <option value="liability_claim">Liability Claim</option>
        <option value="other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label>Tenant Involved? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.tenant_involved" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.tenant_involved" value="no" /> No</label>
      </div>
    </div>

    <div v-if="formData.tenant_involved === 'yes'" class="conditional-section">
      <h4>Tenant Information</h4>
      <div class="form-group">
        <label for="tenant-name">Tenant Name *</label>
        <input
          type="text"
          id="tenant-name"
          v-model="formData.tenant_name"
          :required="formData.tenant_involved === 'yes'"
          :class="['form-control', { 'invalid': touched.tenant_name && !isTenantNameValid }]"
          placeholder="First Last"
          @blur="touched.tenant_name = true"
        />
      </div>
      <div class="form-group">
        <label>Tenant Caused Damage? *</label>
        <div class="radio-group">
          <label class="radio-label"><input type="radio" v-model="formData.tenant_caused_damage" value="yes" /> Yes</label>
          <label class="radio-label"><input type="radio" v-model="formData.tenant_caused_damage" value="no" /> No</label>
        </div>
      </div>
    </div>

    <div class="form-group">
      <label>Property Currently Occupied? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.property_currently_occupied" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.property_currently_occupied" value="no" /> No</label>
      </div>
    </div>

    <div class="form-group">
      <label>Rent Interruption Expected? *</label>
      <div class="radio-group">
        <label class="radio-label"><input type="radio" v-model="formData.rent_interruption_expected" value="yes" /> Yes</label>
        <label class="radio-label"><input type="radio" v-model="formData.rent_interruption_expected" value="no" /> No</label>
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
        placeholder="Describe the damage to your rental property"
        @blur="touched.damage_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.damage_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import { ValidationRules } from '@/utils/validation'

interface LandlordClaimFormData {
  incident_type: string
  tenant_involved: string
  tenant_name: string
  tenant_caused_damage: string
  property_currently_occupied: string
  rent_interruption_expected: string
  damage_description: string
}

const emit = defineEmits<{
  (e: 'update', data: LandlordClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<LandlordClaimFormData>({
  incident_type: '',
  tenant_involved: '',
  tenant_name: '',
  tenant_caused_damage: '',
  property_currently_occupied: '',
  rent_interruption_expected: '',
  damage_description: ''
})

const touched = reactive({
  tenant_name: false,
  damage_description: false
})

const isTenantNameValid = computed(() => {
  if (formData.tenant_involved !== 'yes') return true
  if (!formData.tenant_name.trim()) return false
  return ValidationRules.fullName.validate(formData.tenant_name).isValid
})
const isDamageDescriptionValid = computed(() => formData.damage_description.trim().length >= 50)

const isFormValid = computed(() => {
  const baseValid = (
    formData.incident_type !== '' &&
    formData.tenant_involved !== '' &&
    formData.property_currently_occupied !== '' &&
    formData.rent_interruption_expected !== '' &&
    isDamageDescriptionValid.value
  )
  if (formData.tenant_involved === 'yes' && (!isTenantNameValid.value || formData.tenant_caused_damage === '')) return false
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
.landlord-claim-form { width: 100%; }
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
