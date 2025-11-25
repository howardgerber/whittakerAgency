<template>
  <div class="rv-quote-form">
    <h3>RV Insurance Details</h3>

    <VehicleInfoFields
      v-model="vehicleInfo"
      field-prefix="rv"
      year-placeholder="e.g., 2020"
      make-placeholder="e.g., Winnebago"
      model-placeholder="e.g., Vista"
    />

    <div class="form-group">
      <label for="rv-type">RV Type *</label>
      <select id="rv-type" v-model="formData.rv_type" required class="form-control">
        <option value="">Select RV Type</option>
        <option value="class_a">Class A Motorhome</option>
        <option value="class_b">Class B Motorhome</option>
        <option value="class_c">Class C Motorhome</option>
        <option value="travel_trailer">Travel Trailer</option>
        <option value="fifth_wheel">Fifth Wheel</option>
      </select>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="rv-usage">Usage *</label>
        <select id="rv-usage" v-model="formData.usage" required class="form-control">
          <option value="">Select Usage</option>
          <option value="full_time">Full-Time Living</option>
          <option value="vacation">Vacation/Part-Time</option>
        </select>
      </div>

      <div class="form-group">
        <label for="rv-current-provider">Current Insurance Provider</label>
        <input
          type="text"
          id="rv-current-provider"
          v-model="formData.current_provider"
          class="form-control"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import VehicleInfoFields, { type VehicleInfo } from './VehicleInfoFields.vue'

interface RVFormData {
  year: number | null
  make: string
  model: string
  rv_type: string
  vin: string
  usage: string
  current_provider: string
}

const emit = defineEmits<{
  (e: 'update', data: RVFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<RVFormData>({
  year: null,
  make: '',
  model: '',
  rv_type: '',
  vin: '',
  usage: '',
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
    formData.rv_type !== '' &&
    formData.usage !== ''
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
