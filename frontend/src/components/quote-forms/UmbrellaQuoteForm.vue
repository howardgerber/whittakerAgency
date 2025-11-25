<template>
  <div class="umbrella-quote-form">
    <h3>Umbrella Insurance Details</h3>

    <div class="form-row">
      <div class="form-group">
        <label for="umbrella-auto-limits">Current Auto Insurance Limits *</label>
        <input
          type="text"
          id="umbrella-auto-limits"
          :value="displayValues.auto_limits"
          @input="handleAutoLimitsInput"
          required
          class="form-control"
          placeholder="e.g., $250,000"
          inputmode="numeric"
        />
      </div>

      <div class="form-group">
        <label for="umbrella-home-limits">Current Home Insurance Limits *</label>
        <input
          type="text"
          id="umbrella-home-limits"
          :value="displayValues.home_limits"
          @input="handleHomeLimitsInput"
          required
          class="form-control"
          placeholder="e.g., $500,000"
          inputmode="numeric"
        />
      </div>
    </div>

    <div class="form-group">
      <label for="umbrella-coverage-amount">Desired Umbrella Coverage Amount *</label>
      <select id="umbrella-coverage-amount" v-model="formData.umbrella_coverage" required class="form-control">
        <option value="">Select Coverage Amount</option>
        <option value="1000000">$1,000,000</option>
        <option value="2000000">$2,000,000</option>
        <option value="3000000">$3,000,000</option>
        <option value="5000000">$5,000,000</option>
      </select>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="umbrella-properties">Number of Properties Owned *</label>
        <input
          type="text"
          id="umbrella-properties"
          :value="displayValues.num_properties"
          @input="handlePropertiesInput"
          required
          class="form-control"
          placeholder="e.g., 2"
          inputmode="numeric"
        />
      </div>

      <div class="form-group">
        <label for="umbrella-vehicles">Number of Vehicles Owned *</label>
        <input
          type="text"
          id="umbrella-vehicles"
          :value="displayValues.num_vehicles"
          @input="handleVehiclesInput"
          required
          class="form-control"
          placeholder="e.g., 3"
          inputmode="numeric"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import { formatCurrency } from '@/utils/formatters'

interface UmbrellaFormData {
  auto_limits: string
  home_limits: string
  umbrella_coverage: string
  num_properties: number | null
  num_vehicles: number | null
}

const emit = defineEmits<{
  (e: 'update', data: UmbrellaFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<UmbrellaFormData>({
  auto_limits: '',
  home_limits: '',
  umbrella_coverage: '',
  num_properties: null,
  num_vehicles: null
})

// Display values for formatted fields
const displayValues = reactive({
  auto_limits: '',
  home_limits: '',
  num_properties: '',
  num_vehicles: ''
})

// Handle auto limits input - format with $ and commas
const handleAutoLimitsInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const formatted = formatCurrency(input.value)
  input.value = formatted
  displayValues.auto_limits = formatted
  formData.auto_limits = formatted
}

// Handle home limits input - format with $ and commas
const handleHomeLimitsInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const formatted = formatCurrency(input.value)
  input.value = formatted
  displayValues.home_limits = formatted
  formData.home_limits = formatted
}

// Handle number of properties input - numbers only
const handlePropertiesInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const digitsOnly = input.value.replace(/\D/g, '')
  input.value = digitsOnly
  displayValues.num_properties = digitsOnly
  formData.num_properties = digitsOnly ? parseInt(digitsOnly, 10) : null
}

// Handle number of vehicles input - numbers only
const handleVehiclesInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const digitsOnly = input.value.replace(/\D/g, '')
  input.value = digitsOnly
  displayValues.num_vehicles = digitsOnly
  formData.num_vehicles = digitsOnly ? parseInt(digitsOnly, 10) : null
}

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  return (
    formData.auto_limits.trim() !== '' &&
    formData.home_limits.trim() !== '' &&
    formData.umbrella_coverage !== '' &&
    formData.num_properties !== null &&
    formData.num_vehicles !== null
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
