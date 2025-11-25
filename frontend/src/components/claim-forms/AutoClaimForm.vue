<template>
  <div class="auto-claim-form">
    <h3>Auto Insurance Claim Details</h3>

    <div class="form-group">
      <label for="incident-type">Type of Incident *</label>
      <select
        id="incident-type"
        v-model="formData.incident_type"
        required
        class="form-control"
      >
        <option value="">Select Incident Type</option>
        <option value="collision">Collision with Another Vehicle</option>
        <option value="single_vehicle">Single Vehicle Accident</option>
        <option value="theft">Theft</option>
        <option value="vandalism">Vandalism</option>
        <option value="weather">Weather Damage</option>
        <option value="hit_and_run">Hit and Run</option>
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
        :class="['form-control', { 'invalid': touched.incident_location && !isIncidentLocationValid }]"
        placeholder="Street address or intersection"
        @blur="touched.incident_location = true"
      />
    </div>

    <!-- Only show "other party" question for incident types where it makes sense -->
    <div v-if="canHaveOtherParty" class="form-group">
      <label>Was Another Party Involved? *</label>
      <div class="radio-group">
        <label class="radio-label">
          <input
            type="radio"
            v-model="formData.other_party_involved"
            value="yes"
          />
          Yes
        </label>
        <label class="radio-label">
          <input
            type="radio"
            v-model="formData.other_party_involved"
            value="no"
          />
          No
        </label>
      </div>
    </div>

    <!-- Other Party Details (conditional) -->
    <div v-if="formData.other_party_involved === 'yes'" class="conditional-section">
      <h4>Other Party Information</h4>

      <div class="form-group">
        <label for="other-party-name">Other Party Full Name *</label>
        <input
          type="text"
          id="other-party-name"
          v-model="formData.other_party_name"
          :required="formData.other_party_involved === 'yes'"
          :class="['form-control', { 'invalid': touched.other_party_name && !isOtherPartyNameValid }]"
          placeholder="First Last"
          @blur="touched.other_party_name = true"
        />
        <small v-if="touched.other_party_name && !isOtherPartyNameValid" class="error-text">
          Please enter both first and last name
        </small>
      </div>

      <div class="form-group">
        <label for="other-party-insurance">Insurance Company</label>
        <input
          type="text"
          id="other-party-insurance"
          v-model="formData.other_party_insurance"
          class="form-control"
          placeholder="e.g., State Farm, Geico"
        />
      </div>

      <div class="form-group">
        <label for="other-party-phone">Other Party Phone</label>
        <input
          type="tel"
          id="other-party-phone"
          v-model="formData.other_party_phone"
          @input="handlePhoneInput($event, 'other_party_phone')"
          :class="['form-control', { 'invalid': touched.other_party_phone && !isOtherPartyPhoneValid }]"
          placeholder="XXX.XXX.XXXX"
          @blur="touched.other_party_phone = true"
        />
      </div>
    </div>

    <div class="form-group">
      <label for="police-report">Police Report Filed? *</label>
      <select
        id="police-report"
        v-model="formData.police_report_filed"
        required
        class="form-control"
      >
        <option value="">Select Option</option>
        <option value="yes">Yes - Report Number Available</option>
        <option value="no">No</option>
        <option value="pending">Report Pending</option>
      </select>
    </div>

    <div v-if="formData.police_report_filed === 'yes'" class="form-group">
      <label for="police-report-number">Police Report Number</label>
      <input
        type="text"
        id="police-report-number"
        v-model="formData.police_report_number"
        class="form-control"
      />
    </div>

    <div class="form-group">
      <label>Is the Vehicle Drivable? *</label>
      <div class="radio-group">
        <label class="radio-label">
          <input
            type="radio"
            v-model="formData.vehicle_drivable"
            value="yes"
          />
          Yes
        </label>
        <label class="radio-label">
          <input
            type="radio"
            v-model="formData.vehicle_drivable"
            value="no"
          />
          No
        </label>
        <label class="radio-label">
          <input
            type="radio"
            v-model="formData.vehicle_drivable"
            value="unknown"
          />
          Unknown
        </label>
      </div>
    </div>

    <div class="form-group">
      <label for="damage-description">Damage Description *</label>
      <textarea
        id="damage-description"
        v-model="formData.damage_description"
        rows="4"
        maxlength="500"
        required
        :class="['form-control', { 'invalid': touched.damage_description && !isDamageDescriptionValid }]"
        placeholder="Describe the damage to your vehicle (e.g., front bumper cracked, driver side door dented)"
        @blur="touched.damage_description = true"
      ></textarea>
      <small :class="damageCharClass">{{ formData.damage_description.length }}/500 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import { ValidationRules } from '@/utils/validation'
import { formatPhoneNumber } from '@/utils/formatters'

interface AutoClaimFormData {
  incident_type: string
  incident_location: string
  other_party_involved: string
  other_party_name: string
  other_party_insurance: string
  other_party_phone: string
  police_report_filed: string
  police_report_number: string
  vehicle_drivable: string
  damage_description: string
}

interface Props {
  errors?: Record<string, string>
}

withDefaults(defineProps<Props>(), {
  errors: () => ({})
})

const emit = defineEmits<{
  (e: 'update', data: AutoClaimFormData): void
  (e: 'valid', isValid: boolean): void
  (e: 'blur', field: string): void
}>()

const formData = reactive<AutoClaimFormData>({
  incident_type: '',
  incident_location: '',
  other_party_involved: '',
  other_party_name: '',
  other_party_insurance: '',
  other_party_phone: '',
  police_report_filed: '',
  police_report_number: '',
  vehicle_drivable: '',
  damage_description: ''
})

// Track which fields have been touched (blurred)
const touched = reactive({
  incident_location: false,
  other_party_name: false,
  other_party_phone: false,
  damage_description: false
})

// Validation computed properties
const isIncidentLocationValid = computed(() => {
  const trimmed = formData.incident_location.trim()
  return trimmed.length >= 3
})

const isOtherPartyNameValid = computed(() => {
  // Only validate if other party is involved
  if (formData.other_party_involved !== 'yes') return true
  if (!formData.other_party_name.trim()) return false
  return ValidationRules.fullName.validate(formData.other_party_name).isValid
})

const isOtherPartyPhoneValid = computed(() => {
  // Phone is optional, but if provided must be valid
  if (!formData.other_party_phone.trim()) return true
  return ValidationRules.phone.validate(formData.other_party_phone).isValid
})

const isDamageDescriptionValid = computed(() => {
  return formData.damage_description.trim().length >= 10
})

// Computed: Can this incident type have another party involved?
const canHaveOtherParty = computed(() => {
  // Only collision and other can have another party
  // Hit and run = they fled (no info), theft/vandalism = criminal (not "other party"), weather = no party, single vehicle = just you
  return ['collision', 'other'].includes(formData.incident_type)
})

// Watch incident type and auto-set other_party_involved to 'no' when it doesn't make sense
watch(() => formData.incident_type, (newType) => {
  if (!['collision', 'other'].includes(newType)) {
    formData.other_party_involved = 'no'
    // Clear other party fields
    formData.other_party_name = ''
    formData.other_party_insurance = ''
    formData.other_party_phone = ''
  }
})

// Handle phone input with auto-formatting
const handlePhoneInput = (event: Event, fieldName: string) => {
  const input = event.target as HTMLInputElement
  formData[fieldName as keyof AutoClaimFormData] = formatPhoneNumber(input.value) as any
}

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  const baseValid = (
    formData.incident_type !== '' &&
    isIncidentLocationValid.value &&
    formData.police_report_filed !== '' &&
    formData.vehicle_drivable !== '' &&
    isDamageDescriptionValid.value &&
    isOtherPartyPhoneValid.value
  )

  // If the incident type can have another party, require the question to be answered
  if (canHaveOtherParty.value) {
    if (formData.other_party_involved === '') return false

    // If other party involved, their name is required and must be valid
    if (formData.other_party_involved === 'yes') {
      return baseValid && isOtherPartyNameValid.value
    }
  }

  return baseValid
})

// Character count styling for damage description
const damageCharClass = computed(() => {
  const length = formData.damage_description.length
  const min = 10
  const max = 500

  if (length < min) return 'below-min'
  if (length >= max) return 'at-limit'
  if (length / max >= 0.9) return 'near-limit'
  return 'normal'
})

// Watch for changes and emit to parent
watch(formData, (newData) => {
  emit('update', { ...newData })
}, { deep: true })

// Watch validation state and emit to parent
watch(isFormValid, (isValid) => {
  emit('valid', isValid)
}, { immediate: true })
</script>

<style scoped>
.auto-claim-form {
  width: 100%;
}

h3 {
  color: var(--color-primary, var(--color-primary));
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
}

h4 {
  color: var(--color-primary);
  font-size: 1.1rem;
  margin-bottom: 1rem;
  margin-top: 0;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
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

.error-text {
  color: #dc3545;
  font-size: 0.875rem;
  display: block;
  margin-top: 0.25rem;
}

select.form-control {
  cursor: pointer;
}

textarea.form-control {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.radio-group {
  display: flex;
  gap: 1.5rem;
  margin-top: 0.5rem;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 400;
  cursor: pointer;
}

.radio-label input[type="radio"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.conditional-section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  border-left: 4px solid var(--color-primary);
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
  content: ' (minimum 10 characters)';
}

small.near-limit {
  color: #ff9800;
  font-weight: 600;
}

small.at-limit {
  color: #f44336;
  font-weight: 600;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .radio-group {
    flex-direction: column;
    gap: 0.75rem;
  }
}
</style>
