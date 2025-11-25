<template>
  <div class="vehicle-protection-quote-form">
    <h3>Vehicle Protection Details</h3>

    <div class="form-group">
      <label for="protection-type">Protection Type *</label>
      <select id="protection-type" v-model="formData.protection_type" required class="form-control">
        <option value="">Select Protection Type</option>
        <option value="extended_warranty">Extended Warranty</option>
        <option value="gap">GAP Insurance</option>
        <option value="tire_wheel">Tire & Wheel Protection</option>
        <option value="paintless_dent">Paintless Dent Repair</option>
        <option value="comprehensive">Comprehensive Package</option>
      </select>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="protection-year">Vehicle Year *</label>
        <input
          type="text"
          id="protection-year"
          v-model="formData.year"
          required
          class="form-control"
          placeholder="e.g., 2023"
        />
      </div>

      <div class="form-group">
        <label for="protection-make">Make *</label>
        <input
          type="text"
          id="protection-make"
          v-model="formData.make"
          required
          class="form-control"
          placeholder="e.g., Toyota"
        />
      </div>

      <div class="form-group">
        <label for="protection-model">Model *</label>
        <input
          type="text"
          id="protection-model"
          v-model="formData.model"
          required
          class="form-control"
          placeholder="e.g., Camry"
        />
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="protection-mileage">Current Mileage *</label>
        <input
          type="number"
          id="protection-mileage"
          v-model.number="formData.mileage"
          min="0"
          required
          class="form-control"
          placeholder="e.g., 35000"
        />
      </div>

      <div class="form-group">
        <label for="protection-warranty">Under Manufacturer Warranty? *</label>
        <select id="protection-warranty" v-model="formData.under_warranty" required class="form-control">
          <option value="">Select</option>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface VehicleProtectionFormData {
  protection_type: string
  year: string
  make: string
  model: string
  mileage: number | null
  under_warranty: string
}

const emit = defineEmits<{
  (e: 'update', data: VehicleProtectionFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<VehicleProtectionFormData>({
  protection_type: '',
  year: '',
  make: '',
  model: '',
  mileage: null,
  under_warranty: ''
})

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  return (
    formData.protection_type !== '' &&
    formData.year.trim() !== '' &&
    formData.make.trim() !== '' &&
    formData.model.trim() !== '' &&
    formData.mileage !== null &&
    formData.under_warranty !== ''
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
