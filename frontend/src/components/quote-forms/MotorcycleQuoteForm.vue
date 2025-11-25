<template>
  <div class="motorcycle-quote-form">
    <h3>Motorcycle Insurance Details</h3>

    <VehicleInfoFields
      v-model="vehicleInfo"
      field-prefix="motorcycle"
      year-placeholder="e.g., 2023"
      make-placeholder="e.g., Harley-Davidson"
      model-placeholder="e.g., Street 750"
    />

    <div class="form-row">
      <div class="form-group">
        <label for="motorcycle-use">Primary Use *</label>
        <select id="motorcycle-use" v-model="formData.primary_use" required class="form-control">
          <option value="">Select Primary Use</option>
          <option value="recreation">Recreation</option>
          <option value="commute">Commute</option>
        </select>
      </div>

      <div class="form-group">
        <label for="motorcycle-storage">Storage Location</label>
        <input
          type="text"
          id="motorcycle-storage"
          v-model="formData.storage_location"
          class="form-control"
          placeholder="e.g., Garage"
        />
      </div>
    </div>

    <div class="form-group">
      <label for="motorcycle-current-provider">Current Insurance Provider</label>
      <input
        type="text"
        id="motorcycle-current-provider"
        v-model="formData.current_provider"
        class="form-control"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import VehicleInfoFields, { type VehicleInfo } from './VehicleInfoFields.vue'

interface MotorcycleFormData {
  year: number | null
  make: string
  model: string
  vin: string
  primary_use: string
  storage_location: string
  current_provider: string
}

const emit = defineEmits<{
  (e: 'update', data: MotorcycleFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<MotorcycleFormData>({
  year: null,
  make: '',
  model: '',
  vin: '',
  primary_use: '',
  storage_location: '',
  current_provider: ''
})

// Create a computed property for vehicle info
const vehicleInfo = computed({
  get: (): VehicleInfo => ({
    year: formData.year,
    make: formData.make,
    model: formData.model,
    vin: formData.vin
  }),
  set: (value: VehicleInfo) => {
    formData.year = value.year
    formData.make = value.make
    formData.model = value.model
    formData.vin = value.vin || ''
  }
})

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  return (
    formData.year !== null &&
    formData.make.trim() !== '' &&
    formData.model.trim() !== '' &&
    formData.primary_use !== ''
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
