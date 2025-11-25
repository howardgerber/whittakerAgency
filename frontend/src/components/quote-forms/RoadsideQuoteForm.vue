<template>
  <div class="roadside-quote-form">
    <h3>Roadside Assistance Details</h3>

    <div class="form-group">
      <label for="roadside-coverage">Coverage Level *</label>
      <select id="roadside-coverage" v-model="formData.coverage_level" required class="form-control">
        <option value="">Select Coverage Level</option>
        <option value="basic">Basic (Towing, Flat Tire, Battery)</option>
        <option value="plus">Plus (Basic + Lockout, Fuel Delivery)</option>
        <option value="premium">Premium (Plus + Trip Interruption)</option>
      </select>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="roadside-vehicles">Number of Vehicles *</label>
        <input
          type="number"
          id="roadside-vehicles"
          v-model.number="formData.num_vehicles"
          min="1"
          max="10"
          required
          class="form-control"
          placeholder="e.g., 2"
        />
      </div>

      <div class="form-group">
        <label for="roadside-drivers">Number of Drivers</label>
        <input
          type="number"
          id="roadside-drivers"
          v-model.number="formData.num_drivers"
          min="1"
          max="10"
          class="form-control"
          placeholder="e.g., 2"
        />
      </div>
    </div>

    <div class="form-group">
      <label for="roadside-current-provider">Current Roadside Provider</label>
      <input
        type="text"
        id="roadside-current-provider"
        v-model="formData.current_provider"
        class="form-control"
        placeholder="e.g., AAA, Motor Club"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface RoadsideFormData {
  coverage_level: string
  num_vehicles: number | null
  num_drivers: number | null
  current_provider: string
}

const emit = defineEmits<{
  (e: 'update', data: RoadsideFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<RoadsideFormData>({
  coverage_level: '',
  num_vehicles: null,
  num_drivers: null,
  current_provider: ''
})

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  return (
    formData.coverage_level !== '' &&
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
