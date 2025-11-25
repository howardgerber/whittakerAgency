<template>
  <div class="home-quote-form">
    <h3>Home Insurance Details</h3>

    <div class="form-group">
      <label for="home-address">Property Address *</label>
      <input
        type="text"
        id="home-address"
        v-model="formData.address"
        required
        class="form-control"
        placeholder="123 Main St, Portland, OR 97201"
      />
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="home-year-built">Year Built *</label>
        <input
          type="text"
          id="home-year-built"
          :value="displayValues.year_built"
          @input="handleYearInput"
          required
          class="form-control"
          placeholder="e.g., 1995"
          inputmode="numeric"
        />
      </div>

      <div class="form-group">
        <label for="home-square-footage">Square Footage *</label>
        <input
          type="text"
          id="home-square-footage"
          :value="displayValues.square_footage"
          @input="handleSquareFootageInput"
          required
          class="form-control"
          placeholder="e.g., 2,000"
          inputmode="numeric"
        />
      </div>
    </div>

    <div class="form-group">
      <label for="home-coverage-amount">Desired Coverage Amount *</label>
      <input
        type="text"
        id="home-coverage-amount"
        :value="displayValues.coverage_amount"
        @input="handleCoverageAmountInput"
        required
        class="form-control"
        placeholder="e.g., $350,000"
        inputmode="numeric"
      />
    </div>

    <div class="form-group">
      <label for="home-current-provider">Current Insurance Provider</label>
      <input
        type="text"
        id="home-current-provider"
        v-model="formData.current_provider"
        class="form-control"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import {
  formatYear,
  formatNumberWithCommas,
  formatCurrency,
  parseFormattedNumber,
  parseFormattedCurrency
} from '@/utils/formatters'

interface HomeFormData {
  address: string
  year_built: string
  square_footage: number | null
  coverage_amount: number | null
  current_provider: string
}

const emit = defineEmits<{
  (e: 'update', data: HomeFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<HomeFormData>({
  address: '',
  year_built: '',
  square_footage: null,
  coverage_amount: null,
  current_provider: ''
})

// Display values for formatted fields
const displayValues = reactive({
  year_built: '',
  square_footage: '',
  coverage_amount: ''
})

// Handle year built input - only numbers, max 4 digits
const handleYearInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const formatted = formatYear(input.value)
  input.value = formatted // Update the input directly
  displayValues.year_built = formatted
  formData.year_built = formatted
}

// Handle square footage input - format with commas
const handleSquareFootageInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const formatted = formatNumberWithCommas(input.value)
  input.value = formatted // Update the input directly
  displayValues.square_footage = formatted
  formData.square_footage = parseFormattedNumber(formatted)
}

// Handle coverage amount input - format with $ and commas
const handleCoverageAmountInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const formatted = formatCurrency(input.value)
  input.value = formatted // Update the input directly
  displayValues.coverage_amount = formatted
  formData.coverage_amount = parseFormattedCurrency(formatted)
}

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  return (
    formData.address.trim() !== '' &&
    formData.year_built.trim() !== '' &&
    formData.square_footage !== null &&
    formData.coverage_amount !== null
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
