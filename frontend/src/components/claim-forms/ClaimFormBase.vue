<template>
  <div class="claim-form-base">
    <h3>{{ formTitle }}</h3>

    <!-- Core Fields (always shown) -->
    <div class="form-group">
      <label for="incident-date">Incident Date *</label>
      <input
        type="date"
        id="incident-date"
        v-model="formData.incident_date"
        required
        class="form-control"
        :max="todayDate"
      />
      <small class="help-text">When did this incident occur?</small>
    </div>

    <div class="form-group">
      <label for="incident-summary">Brief Incident Summary *</label>
      <textarea
        id="incident-summary"
        v-model="formData.incident_summary"
        required
        maxlength="250"
        rows="3"
        class="form-control"
        :class="{ 'at-limit': formData.incident_summary.length >= 250 }"
        placeholder="Briefly describe what happened..."
      ></textarea>
      <small :class="getCharCountClass(formData.incident_summary.length, 250)">
        {{ formData.incident_summary.length }}/250 characters
      </small>
    </div>

    <!-- Dynamic Fields Based on Configuration -->
    <div v-for="field in fields" :key="field.name" class="form-group" :class="{ 'form-group-half': field.width === '50%' }">
      <!-- Only show field if dependency is met -->
      <template v-if="shouldShowField(field)">
        <!-- Text Input -->
        <div v-if="field.type === 'text'">
          <label :for="field.name">
            {{ field.label }}
          </label>
          <input
            :id="field.name"
            type="text"
            v-model="formData[field.name]"
            :required="field.required && shouldShowField(field)"
            :maxlength="field.maxLength"
            :placeholder="field.placeholder"
            class="form-control"
            :class="{ 'invalid': hasValidationError(field.name) }"
            @blur="validateField(field)"
          />
          <small v-if="field.helpText" class="help-text">{{ field.helpText }}</small>
        </div>

        <!-- Number Input -->
        <div v-else-if="field.type === 'number'">
          <label :for="field.name">{{ field.label }}</label>
          <input
            :id="field.name"
            type="number"
            v-model.number="formData[field.name]"
            :required="field.required && shouldShowField(field)"
            :placeholder="field.placeholder"
            class="form-control"
            min="0"
          />
          <small v-if="field.helpText" class="help-text">{{ field.helpText }}</small>
        </div>

        <!-- Phone Input -->
        <div v-else-if="field.type === 'tel'">
          <label :for="field.name">{{ field.label }}</label>
          <input
            :id="field.name"
            type="tel"
            v-model="formData[field.name]"
            :required="field.required && shouldShowField(field)"
            :placeholder="field.placeholder"
            class="form-control"
            :class="{ 'invalid': hasValidationError(field.name) }"
            @input="formatPhoneField(field.name)"
            @blur="validateField(field)"
          />
          <small v-if="field.helpText" class="help-text">{{ field.helpText }}</small>
        </div>

        <!-- Textarea -->
        <div v-else-if="field.type === 'textarea'">
          <label :for="field.name">{{ field.label }}</label>
          <textarea
            :id="field.name"
            v-model="formData[field.name]"
            :required="field.required && shouldShowField(field)"
            :maxlength="field.maxLength"
            rows="3"
            class="form-control"
            :class="{ 'at-limit': field.maxLength && formData[field.name]?.length >= field.maxLength }"
            :placeholder="field.placeholder"
          ></textarea>
          <small v-if="field.characterCounter" :class="getCharCountClass(formData[field.name]?.length || 0, field.maxLength || 250)">
            {{ formData[field.name]?.length || 0 }}/{{ field.maxLength || 250 }} characters
          </small>
          <small v-else-if="field.helpText" class="help-text">{{ field.helpText }}</small>
        </div>

        <!-- Select Dropdown -->
        <div v-else-if="field.type === 'select'">
          <label :for="field.name">{{ field.label }}</label>
          <select
            :id="field.name"
            v-model="formData[field.name]"
            :required="field.required && shouldShowField(field)"
            class="form-control"
          >
            <option v-for="option in field.options" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
          <small v-if="field.helpText" class="help-text">{{ field.helpText }}</small>
        </div>

        <!-- Radio Buttons -->
        <div v-else-if="field.type === 'radio'" class="radio-group">
          <label class="field-label">{{ field.label }}</label>
          <div class="radio-options">
            <label v-for="option in field.options" :key="option.value" class="radio-label">
              <input
                type="radio"
                :name="field.name"
                :value="option.value"
                v-model="formData[field.name]"
                :required="field.required && shouldShowField(field)"
              />
              <span>{{ option.label }}</span>
            </label>
          </div>
          <small v-if="field.helpText" class="help-text">{{ field.helpText }}</small>
        </div>

        <!-- Checkboxes -->
        <div v-else-if="field.type === 'checkbox'" class="checkbox-group">
          <label class="field-label">{{ field.label }}</label>
          <div class="checkbox-options">
            <label v-for="option in field.options" :key="option.value" class="checkbox-label">
              <input
                type="checkbox"
                :value="option.value"
                v-model="formData[field.name]"
                @change="ensureArrayField(field.name)"
              />
              <span>{{ option.label }}</span>
            </label>
          </div>
          <small v-if="field.helpText" class="help-text">{{ field.helpText }}</small>
        </div>

        <!-- Date Input -->
        <div v-else-if="field.type === 'date'">
          <label :for="field.name">{{ field.label }}</label>
          <input
            :id="field.name"
            type="date"
            v-model="formData[field.name]"
            :required="field.required && shouldShowField(field)"
            :max="todayDate"
            class="form-control"
          />
          <small v-if="field.helpText" class="help-text">{{ field.helpText }}</small>
        </div>

        <!-- DateTime Input -->
        <div v-else-if="field.type === 'datetime'">
          <label :for="field.name">{{ field.label }}</label>
          <input
            :id="field.name"
            type="datetime-local"
            v-model="formData[field.name]"
            :required="field.required && shouldShowField(field)"
            class="form-control"
          />
          <small v-if="field.helpText" class="help-text">{{ field.helpText }}</small>
        </div>
      </template>
    </div>

    <!-- Contact Preference & Additional Notes (always shown at end) -->
    <div class="form-group">
      <label for="contact-preference">Contact Preference *</label>
      <select
        id="contact-preference"
        v-model="formData.contact_preference"
        required
        class="form-control"
      >
        <option value="">Select Preference</option>
        <option value="email">Email</option>
        <option value="phone">Phone</option>
        <option value="both">Both</option>
      </select>
    </div>

    <div class="form-group">
      <label for="preferred-contact-time">Preferred Contact Time</label>
      <select
        id="preferred-contact-time"
        v-model="formData.preferred_contact_time"
        class="form-control"
      >
        <option value="">Select Time</option>
        <option value="morning">Morning</option>
        <option value="afternoon">Afternoon</option>
        <option value="evening">Evening</option>
        <option value="anytime">Anytime</option>
      </select>
    </div>

    <div class="form-group">
      <label for="appointment-datetime">Preferred Appointment Date/Time</label>
      <input
        type="datetime-local"
        id="appointment-datetime"
        v-model="formData.appointment_requested"
        class="form-control"
      />
    </div>

    <div class="form-group">
      <label for="additional-notes">Additional Notes</label>
      <textarea
        id="additional-notes"
        v-model="formData.additional_notes"
        maxlength="250"
        rows="3"
        class="form-control"
        :class="{ 'at-limit': formData.additional_notes.length >= 250 }"
        placeholder="Any other information we should know..."
      ></textarea>
      <small :class="getCharCountClass(formData.additional_notes.length, 250)">
        {{ formData.additional_notes.length }}/250 characters
      </small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed, watch } from 'vue'
import { getClaimFields, type FieldConfig } from './claim-fields-config'
import { formatPhoneNumber } from '@/utils/formatters'
import { ValidationRules } from '@/utils/validation'

interface Props {
  category: string
  subcategory: string | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'update', data: Record<string, any>): void
  (e: 'valid', isValid: boolean): void
}>()

// Get fields for this claim type
const fields = computed(() => getClaimFields(props.category, props.subcategory))

// Form title
const formTitle = computed(() => {
  const categoryNames: Record<string, string> = {
    vehicle: 'Vehicle',
    property: 'Property',
    life: 'Life Insurance',
    business: 'Business',
    identity_protection: 'Identity Protection'
  }

  const subcategoryNames: Record<string, string> = {
    auto: 'Auto',
    motorcycle: 'Motorcycle',
    atv: 'ATV/Off-Road',
    roadside: 'Roadside Assistance',
    snowmobile: 'Snowmobile',
    boat: 'Boat',
    rv: 'RV',
    vehicle_protection: 'Vehicle Protection',
    homeowners: 'Homeowners',
    renters: 'Renters',
    condo: 'Condo',
    landlord: 'Landlord',
    mobile_home: 'Mobile Home',
    umbrella: 'Personal Umbrella Policy',
    individual_health: 'Individual Health',
    pet: 'Pet',
    event: 'Event',
    travel: 'Travel',
    jewelry: 'Jewelry',
    collectibles: 'Collectibles'
  }

  const catName = categoryNames[props.category] || props.category
  const subName = props.subcategory ? subcategoryNames[props.subcategory] : null

  return subName ? `${subName} Claim Details` : `${catName} Claim Details`
})

// Reactive form data
const formData = reactive<Record<string, any>>({
  incident_date: '',
  incident_summary: '',
  contact_preference: '',
  preferred_contact_time: '',
  appointment_requested: '',
  additional_notes: ''
})

// Initialize all field values to empty based on field type
watch(() => fields.value, (newFields) => {
  newFields.forEach(field => {
    if (!(field.name in formData)) {
      if (field.type === 'checkbox') {
        formData[field.name] = []
      } else if (field.type === 'number') {
        formData[field.name] = null
      } else {
        formData[field.name] = ''
      }
    }
  })
}, { immediate: true })

// Today's date for max date validation
const todayDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

// Validation errors
const validationErrors = reactive<Record<string, boolean>>({})

// Check if field should be shown based on dependencies
function shouldShowField(field: FieldConfig): boolean {
  if (!field.dependsOn) return true

  const dependentValue = formData[field.dependsOn.field]
  if (Array.isArray(field.dependsOn.value)) {
    return field.dependsOn.value.includes(dependentValue)
  }
  return dependentValue === field.dependsOn.value
}

// Ensure checkbox fields are arrays
function ensureArrayField(fieldName: string) {
  if (!Array.isArray(formData[fieldName])) {
    formData[fieldName] = []
  }
}

// Format phone field
function formatPhoneField(fieldName: string) {
  const value = formData[fieldName]
  if (value) {
    formData[fieldName] = formatPhoneNumber(value)
  }
}

// Validate individual field
function validateField(field: FieldConfig) {
  const value = formData[field.name]

  if (field.validation === 'fullName') {
    const result = ValidationRules.fullName.validate(value || '')
    validationErrors[field.name] = !result.isValid && value && value.length > 0
  } else if (field.validation === 'phone') {
    const result = ValidationRules.phone.validate(value || '')
    validationErrors[field.name] = !result.isValid && value && value.length > 0
  }
}

// Check if field has validation error
function hasValidationError(fieldName: string): boolean {
  return validationErrors[fieldName] === true
}

// Get character count class
function getCharCountClass(currentLength: number, maxLength: number): string {
  const percentage = (currentLength / maxLength) * 100
  if (currentLength >= maxLength) return 'at-limit'
  if (percentage >= 90) return 'near-limit'
  return 'normal'
}

// Computed form validity
const isFormValid = computed(() => {
  // Core required fields
  if (!formData.incident_date || !formData.incident_summary || !formData.contact_preference) {
    return false
  }

  // Check all visible required fields
  for (const field of fields.value) {
    if (field.required && shouldShowField(field)) {
      const value = formData[field.name]

      // Check if field has a value
      if (field.type === 'checkbox') {
        if (!Array.isArray(value) || value.length === 0) {
          return false
        }
      } else if (field.type === 'number') {
        if (value === null || value === undefined || value === '') {
          return false
        }
      } else {
        if (!value || (typeof value === 'string' && value.trim() === '')) {
          return false
        }
      }

      // Check validation errors
      if (validationErrors[field.name]) {
        return false
      }
    }
  }

  return true
})

// Watch form data and emit updates
watch(formData, (newData) => {
  emit('update', { ...newData })
}, { deep: true })

// Watch validity and emit
watch(isFormValid, (isValid) => {
  emit('valid', isValid)
}, { immediate: true })
</script>

<style scoped>
.claim-form-base {
  width: 100%;
}

h3 {
  color: var(--color-primary, var(--color-primary));
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group-half {
  display: inline-block;
  width: calc(50% - 0.5rem);
  vertical-align: top;
}

.form-group-half:nth-of-type(odd) {
  margin-right: 1rem;
}

@media (max-width: 768px) {
  .form-group-half {
    display: block;
    width: 100%;
    margin-right: 0 !important;
  }
}

.field-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
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

.form-control.at-limit {
  border-color: #dc3545;
  border-width: 2px;
}

select.form-control {
  cursor: pointer;
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}

.help-text {
  color: #666;
  font-size: 0.875rem;
  display: block;
  margin-top: 0.25rem;
}

small.normal {
  color: #666;
  font-size: 0.875rem;
  display: block;
  margin-top: 0.25rem;
}

small.near-limit {
  color: #ff9800;
  font-weight: 600;
  font-size: 0.875rem;
  display: block;
  margin-top: 0.25rem;
}

small.at-limit {
  color: #dc3545;
  font-weight: 600;
  font-size: 0.875rem;
  display: block;
  margin-top: 0.25rem;
}

/* Radio Buttons */
.radio-group {
  margin-bottom: 1.5rem;
}

.radio-options {
  display: flex;
  gap: 1.5rem;
  margin-top: 0.5rem;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: normal;
}

.radio-label input[type="radio"] {
  width: auto;
  margin: 0;
  cursor: pointer;
}

.radio-label span {
  color: #333;
}

/* Checkboxes */
.checkbox-group {
  margin-bottom: 1.5rem;
}

.checkbox-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: normal;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin: 0;
  cursor: pointer;
}

.checkbox-label span {
  color: #333;
}

@media (max-width: 768px) {
  .radio-options {
    flex-direction: column;
    gap: 0.75rem;
  }
}
</style>
