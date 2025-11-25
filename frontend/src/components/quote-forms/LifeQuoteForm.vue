<template>
  <div class="life-quote-form">
    <h3>Life Insurance Details</h3>

    <div class="form-group">
      <label for="life-coverage-amount">Coverage Amount Desired *</label>
      <input
        type="text"
        id="life-coverage-amount"
        :value="displayValues.coverage_amount"
        @input="handleCoverageAmountInput"
        required
        class="form-control"
        placeholder="e.g., $500,000"
        inputmode="numeric"
      />
    </div>

    <div v-if="selectedSubtype === 'term'" class="form-group">
      <label for="life-term-length">Term Length *</label>
      <select id="life-term-length" v-model="formData.term_length" required class="form-control">
        <option value="">Select Term Length</option>
        <option value="10">10 Years</option>
        <option value="15">15 Years</option>
        <option value="20">20 Years</option>
        <option value="30">30 Years</option>
      </select>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="beneficiary-name">Beneficiary Name</label>
        <input
          type="text"
          id="beneficiary-name"
          v-model="formData.beneficiary_name"
          :class="['form-control', { 'invalid': beneficiaryTouched && formData.beneficiary_name && !isValidFullName(formData.beneficiary_name) }]"
          placeholder="e.g., Jane Doe"
          @blur="beneficiaryTouched = true"
        />
      </div>

      <div class="form-group">
        <label for="beneficiary-relationship">Relationship</label>
        <select
          id="beneficiary-relationship"
          v-model="formData.beneficiary_relationship"
          class="form-control"
        >
          <option value="">Select Relationship</option>
          <option value="spouse">Spouse</option>
          <option value="parent">Parent</option>
          <option value="sibling">Sibling</option>
          <option value="child">Child</option>
          <option value="other">Other</option>
        </select>
      </div>
    </div>

    <div v-if="formData.beneficiary_relationship === 'other'" class="form-group">
      <label for="beneficiary-other">Specify Relationship</label>
      <input
        type="text"
        id="beneficiary-other"
        v-model="formData.beneficiary_other"
        class="form-control"
        placeholder="e.g., Friend, Cousin, etc."
      />
    </div>

    <div class="form-group">
      <label for="life-health-info">Basic Health Information *</label>
      <select id="life-health-info" v-model="formData.health_info" required class="form-control">
        <option value="">Select Health Status</option>
        <option value="excellent">Excellent</option>
        <option value="good">Good</option>
        <option value="fair">Fair</option>
        <option value="pre_existing">Have Pre-Existing Conditions</option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed } from 'vue'
import { formatCurrency, parseFormattedCurrency } from '@/utils/formatters'
import { ValidationRules } from '@/utils/validation'

interface LifeFormData {
  coverage_amount: number | null
  term_length: string
  beneficiary_name: string
  beneficiary_relationship: string
  beneficiary_other: string
  health_info: string
}

interface Props {
  selectedSubtype?: string
}

const props = withDefaults(defineProps<Props>(), {
  selectedSubtype: ''
})

const emit = defineEmits<{
  (e: 'update', data: LifeFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const beneficiaryTouched = ref(false)

const formData = reactive<LifeFormData>({
  coverage_amount: null,
  term_length: '',
  beneficiary_name: '',
  beneficiary_relationship: '',
  beneficiary_other: '',
  health_info: ''
})

// Validate full name using shared validation rules
const isValidFullName = (name: string): boolean => {
  if (!name || !name.trim()) return true // Empty is okay (beneficiary is optional)
  return ValidationRules.fullName.validate(name).isValid
}

// Display values for formatted fields
const displayValues = reactive({
  coverage_amount: ''
})

// Handle coverage amount input - format with $ and commas
const handleCoverageAmountInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const formatted = formatCurrency(input.value)
  input.value = formatted
  displayValues.coverage_amount = formatted
  formData.coverage_amount = parseFormattedCurrency(formatted)
}

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  const baseValid = formData.coverage_amount !== null && formData.health_info !== ''

  // If term life, also require term_length
  if (props.selectedSubtype === 'term') {
    return baseValid && formData.term_length !== ''
  }

  return baseValid
})

watch(formData, (newData) => {
  emit('update', { ...newData })
}, { deep: true })

// Watch validation state and emit to parent
watch(isFormValid, (isValid) => {
  emit('valid', isValid)
}, { immediate: true })
</script>

<style scoped>
@import './form-styles.css';

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-control.invalid {
  border-color: #dc3545;
  border-width: 2px;
}

.form-control.invalid:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
