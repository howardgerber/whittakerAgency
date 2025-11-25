<template>
  <div class="motorcycle-claim-form">
    <h3>Motorcycle Insurance Claim Details</h3>

    <div class="form-group">
      <label for="incident-type">Type of Incident *</label>
      <select
        id="incident-type"
        v-model="formData.incident_type"
        required
        class="form-control"
      >
        <option value="">Select Incident Type</option>
        <option value="collision_vehicle">Collision with Vehicle</option>
        <option value="collision_object">Collision with Object</option>
        <option value="dropped_bike">Dropped Bike</option>
        <option value="theft">Theft</option>
        <option value="vandalism">Vandalism</option>
        <option value="weather_damage">Weather Damage</option>
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
        placeholder="Street address or general location"
        @blur="touched.incident_location = true"
      />
    </div>

    <div class="form-group">
      <label>Protective Gear Worn</label>
      <div class="checkbox-group">
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.protective_gear" value="helmet" />
          Helmet
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.protective_gear" value="jacket" />
          Jacket
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.protective_gear" value="gloves" />
          Gloves
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.protective_gear" value="boots" />
          Boots
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.protective_gear" value="pants" />
          Pants
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.protective_gear" value="none" />
          None
        </label>
      </div>
    </div>

    <div class="form-group">
      <label>Was Another Party Involved? *</label>
      <div class="radio-group">
        <label class="radio-label">
          <input type="radio" v-model="formData.other_party_involved" value="yes" />
          Yes
        </label>
        <label class="radio-label">
          <input type="radio" v-model="formData.other_party_involved" value="no" />
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
          maxlength="100"
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
      <label>Police Report Filed? *</label>
      <div class="radio-group">
        <label class="radio-label">
          <input type="radio" v-model="formData.police_report_filed" value="yes" />
          Yes
        </label>
        <label class="radio-label">
          <input type="radio" v-model="formData.police_report_filed" value="no" />
          No
        </label>
      </div>
    </div>

    <!-- Police Report Details (conditional) -->
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
      <label>Is the Motorcycle Drivable? *</label>
      <div class="radio-group">
        <label class="radio-label">
          <input type="radio" v-model="formData.motorcycle_drivable" value="yes" />
          Yes
        </label>
        <label class="radio-label">
          <input type="radio" v-model="formData.motorcycle_drivable" value="no" />
          No
        </label>
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
        placeholder="Describe the damage to your motorcycle"
        @blur="touched.damage_description = true"
      ></textarea>
      <small :class="charCountClass">{{ formData.damage_description.length }}/250 characters</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import { ValidationRules } from '@/utils/validation'
import { formatPhoneNumber } from '@/utils/formatters'

interface MotorcycleClaimFormData {
  incident_type: string
  incident_location: string
  protective_gear: string[]
  other_party_involved: string
  other_party_name: string
  other_party_insurance: string
  other_party_phone: string
  police_report_filed: string
  police_report_number: string
  police_department: string
  motorcycle_drivable: string
  damage_description: string
}

const emit = defineEmits<{
  (e: 'update', data: MotorcycleClaimFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<MotorcycleClaimFormData>({
  incident_type: '',
  incident_location: '',
  protective_gear: [],
  other_party_involved: '',
  other_party_name: '',
  other_party_insurance: '',
  other_party_phone: '',
  police_report_filed: '',
  police_report_number: '',
  police_department: '',
  motorcycle_drivable: '',
  damage_description: ''
})

const touched = reactive({
  incident_location: false,
  other_party_name: false,
  other_party_phone: false,
  police_report_number: false,
  police_department: false,
  damage_description: false
})

// Validation computed properties
const isIncidentLocationValid = computed(() => {
  const trimmed = formData.incident_location.trim()
  return trimmed.length >= 3
})

const isOtherPartyNameValid = computed(() => {
  if (formData.other_party_involved !== 'yes') return true
  if (!formData.other_party_name.trim()) return false
  return ValidationRules.fullName.validate(formData.other_party_name).isValid
})

const isOtherPartyPhoneValid = computed(() => {
  if (!formData.other_party_phone.trim()) return true
  return ValidationRules.phone.validate(formData.other_party_phone).isValid
})

const isPoliceReportNumberValid = computed(() => {
  if (formData.police_report_filed !== 'yes') return true
  return formData.police_report_number.trim().length > 0
})

const isPoliceDepartmentValid = computed(() => {
  if (formData.police_report_filed !== 'yes') return true
  return formData.police_department.trim().length > 0
})

const isDamageDescriptionValid = computed(() => {
  return formData.damage_description.trim().length >= 50
})

// Handle phone input with auto-formatting
const handlePhoneInput = (event: Event, fieldName: string) => {
  const input = event.target as HTMLInputElement
  formData[fieldName as keyof MotorcycleClaimFormData] = formatPhoneNumber(input.value) as any
}

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  const baseValid = (
    formData.incident_type !== '' &&
    isIncidentLocationValid.value &&
    formData.other_party_involved !== '' &&
    formData.police_report_filed !== '' &&
    formData.motorcycle_drivable !== '' &&
    isDamageDescriptionValid.value &&
    isOtherPartyPhoneValid.value
  )

  // If other party involved, their name is required
  if (formData.other_party_involved === 'yes' && !isOtherPartyNameValid.value) {
    return false
  }

  // If police report filed, report number and department are required
  if (formData.police_report_filed === 'yes') {
    return baseValid && isPoliceReportNumberValid.value && isPoliceDepartmentValid.value
  }

  return baseValid
})

// Character count styling
const charCountClass = computed(() => {
  const length = formData.damage_description.length
  const min = 50
  const max = 250

  if (length < min) return 'below-min'
  if (length >= max) return 'at-limit'
  if (length / max >= 0.9) return 'near-limit'
  return 'normal'
})

// Watch for changes and emit to parent
watch(formData, (newData) => {
  emit('update', { ...newData })
}, { deep: true })

watch(isFormValid, (isValid) => {
  emit('valid', isValid)
}, { immediate: true })
</script>

<style scoped>
.motorcycle-claim-form {
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

.checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 400;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
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
  content: ' (minimum 50 characters)';
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
  .radio-group {
    flex-direction: column;
    gap: 0.75rem;
  }

  .checkbox-group {
    grid-template-columns: 1fr;
  }
}
</style>
