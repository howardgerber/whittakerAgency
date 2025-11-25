<template>
  <div class="business-quote-form">
    <h3>Business Insurance Details</h3>

    <div class="form-group">
      <label for="business-name">Business Name *</label>
      <input
        type="text"
        id="business-name"
        v-model="formData.business_name"
        required
        class="form-control"
      />
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="business-type">Business Type/Industry *</label>
        <input
          type="text"
          id="business-type"
          v-model="formData.business_type"
          required
          class="form-control"
          placeholder="e.g., Retail, Restaurant, Tech"
        />
      </div>

      <div class="form-group">
        <label for="business-employees">Number of Employees *</label>
        <input
          type="text"
          id="business-employees"
          :value="displayValues.num_employees"
          @input="handleEmployeesInput"
          required
          class="form-control"
          placeholder="e.g., 25"
          inputmode="numeric"
        />
      </div>
    </div>

    <div class="form-group">
      <label for="business-revenue">Annual Revenue *</label>
      <input
        type="text"
        id="business-revenue"
        :value="displayValues.annual_revenue"
        @input="handleRevenueInput"
        required
        class="form-control"
        placeholder="e.g., $500,000"
        inputmode="numeric"
      />
    </div>

    <div class="form-group">
      <label for="business-property-value">Property Value</label>
      <input
        type="text"
        id="business-property-value"
        :value="displayValues.property_value"
        @input="handlePropertyValueInput"
        class="form-control"
        placeholder="e.g., $250,000"
        inputmode="numeric"
      />
    </div>

    <div class="form-group">
      <label>Coverage Types Needed *</label>
      <div class="checkbox-group">
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.coverage_types.general_liability" />
          General Liability
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.coverage_types.property" />
          Property Insurance
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.coverage_types.workers_comp" />
          Workers Compensation
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.coverage_types.professional_liability" />
          Professional Liability
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.coverage_types.cyber" />
          Cyber Insurance
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import { formatCurrency, parseFormattedCurrency } from '@/utils/formatters'

interface BusinessFormData {
  business_name: string
  business_type: string
  num_employees: number | null
  annual_revenue: number | null
  property_value: number | null
  coverage_types: {
    general_liability: boolean
    property: boolean
    workers_comp: boolean
    professional_liability: boolean
    cyber: boolean
  }
}

const emit = defineEmits<{
  (e: 'update', data: BusinessFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<BusinessFormData>({
  business_name: '',
  business_type: '',
  num_employees: null,
  annual_revenue: null,
  property_value: null,
  coverage_types: {
    general_liability: false,
    property: false,
    workers_comp: false,
    professional_liability: false,
    cyber: false
  }
})

// Display values for formatted fields
const displayValues = reactive({
  num_employees: '',
  annual_revenue: '',
  property_value: ''
})

// Handle number of employees input - numbers only, no formatting
const handleEmployeesInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const digitsOnly = input.value.replace(/\D/g, '')
  input.value = digitsOnly
  displayValues.num_employees = digitsOnly
  formData.num_employees = digitsOnly ? parseInt(digitsOnly, 10) : null
}

// Handle annual revenue input - format with $ and commas
const handleRevenueInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const formatted = formatCurrency(input.value)
  input.value = formatted
  displayValues.annual_revenue = formatted
  formData.annual_revenue = parseFormattedCurrency(formatted)
}

// Handle property value input - format with $ and commas
const handlePropertyValueInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const formatted = formatCurrency(input.value)
  input.value = formatted
  displayValues.property_value = formatted
  formData.property_value = parseFormattedCurrency(formatted)
}

// Check if at least one coverage type is selected
const hasCoverageType = computed(() => {
  return Object.values(formData.coverage_types).some(value => value === true)
})

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  return (
    formData.business_name.trim() !== '' &&
    formData.business_type.trim() !== '' &&
    formData.num_employees !== null &&
    formData.annual_revenue !== null &&
    hasCoverageType.value
  )
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
</style>
