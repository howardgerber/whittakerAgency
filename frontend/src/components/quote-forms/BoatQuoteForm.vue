<template>
  <div class="boat-quote-form">
    <h3>Boat Insurance Details</h3>

    <VehicleInfoFields
      v-model="vehicleInfo"
      :show-v-i-n="false"
      field-prefix="boat"
      year-placeholder="e.g., 2019"
      make-placeholder="e.g., Sea Ray"
      model-placeholder="e.g., Sundancer"
    />

    <div class="form-row">
      <div class="form-group">
        <label for="boat-type">Boat Type *</label>
        <select id="boat-type" v-model="formData.boat_type" required class="form-control">
          <option value="">Select Boat Type</option>
          <option value="power">Power Boat</option>
          <option value="sail">Sailboat</option>
          <option value="pwc">Personal Watercraft (Jet Ski)</option>
        </select>
      </div>

      <div class="form-group">
        <label for="boat-length">Length (feet) *</label>
        <input
          type="number"
          id="boat-length"
          v-model.number="formData.length"
          min="1"
          required
          class="form-control"
          placeholder="e.g., 24"
        />
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="boat-storage">Storage Location</label>
        <input
          type="text"
          id="boat-storage"
          v-model="formData.storage_location"
          class="form-control"
          placeholder="e.g., Marina, Dry storage"
        />
      </div>

      <div class="form-group">
        <label for="boat-usage">Usage Frequency</label>
        <select id="boat-usage" v-model="formData.usage_frequency" class="form-control">
          <option value="">Select Frequency</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
          <option value="seasonal">Seasonal</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import VehicleInfoFields, { type VehicleInfo } from './VehicleInfoFields.vue'

interface BoatFormData {
  year: number | null
  make: string
  model: string
  boat_type: string
  length: number | null
  storage_location: string
  usage_frequency: string
}

const emit = defineEmits<{
  (e: 'update', data: BoatFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<BoatFormData>({
  year: null,
  make: '',
  model: '',
  boat_type: '',
  length: null,
  storage_location: '',
  usage_frequency: ''
})

// Create a computed property for vehicle info (no VIN for boats)
const vehicleInfo = computed({
  get: (): VehicleInfo => ({
    year: formData.year,
    make: formData.make,
    model: formData.model
  }),
  set: (value: VehicleInfo) => {
    formData.year = value.year
    formData.make = value.make
    formData.model = value.model
  }
})

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  return (
    formData.year !== null &&
    formData.make.trim() !== '' &&
    formData.model.trim() !== '' &&
    formData.boat_type !== '' &&
    formData.length !== null
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
