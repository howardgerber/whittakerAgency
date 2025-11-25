<template>
  <div class="atv-quote-form">
    <h3>ATV/Off-Road Insurance Details</h3>

    <VehicleInfoFields
      v-model="vehicleInfo"
      field-prefix="atv"
      year-placeholder="e.g., 2022"
      make-placeholder="e.g., Polaris"
      model-placeholder="e.g., Sportsman 570"
    />

    <div class="form-row">
      <div class="form-group">
        <label for="atv-type">Vehicle Type *</label>
        <select id="atv-type" v-model="formData.vehicle_type" required class="form-control">
          <option value="">Select Type</option>
          <option value="atv">ATV</option>
          <option value="utv">UTV/Side-by-Side</option>
          <option value="dirt_bike">Dirt Bike</option>
          <option value="other">Other Off-Road</option>
        </select>
      </div>

      <div class="form-group">
        <label for="atv-use">Primary Use *</label>
        <select id="atv-use" v-model="formData.primary_use" required class="form-control">
          <option value="">Select Primary Use</option>
          <option value="recreation">Recreation</option>
          <option value="work">Work/Farm Use</option>
          <option value="racing">Racing</option>
        </select>
      </div>
    </div>

    <div class="form-group">
      <label for="atv-storage">Storage Location</label>
      <input
        type="text"
        id="atv-storage"
        v-model="formData.storage_location"
        class="form-control"
        placeholder="e.g., Garage, Shed"
      />
    </div>

    <div class="form-group">
      <label for="atv-current-provider">Current Insurance Provider</label>
      <input
        type="text"
        id="atv-current-provider"
        v-model="formData.current_provider"
        class="form-control"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import VehicleInfoFields, { type VehicleInfo } from './VehicleInfoFields.vue'

interface ATVFormData {
  year: number | null
  make: string
  model: string
  vin: string
  vehicle_type: string
  primary_use: string
  storage_location: string
  current_provider: string
}

const emit = defineEmits<{
  (e: 'update', data: ATVFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<ATVFormData>({
  year: null,
  make: '',
  model: '',
  vin: '',
  vehicle_type: '',
  primary_use: '',
  storage_location: '',
  current_provider: ''
})

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
    formData.vehicle_type !== '' &&
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
