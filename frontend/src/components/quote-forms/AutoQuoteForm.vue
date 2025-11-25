<template>
  <div class="auto-quote-form">
    <h3>Auto Insurance Details</h3>

    <VehicleInfoFields
      v-model="vehicleInfo"
      :errors="errors"
      field-prefix="auto"
      @blur="$emit('blur', $event)"
    />

    <div class="form-group">
      <label for="auto-coverage">Coverage Level *</label>
      <select
        id="auto-coverage"
        :value="formData.coverage_level"
        @change="updateCoverageLevel"
        required
        class="form-control"
      >
        <option value="">Select Coverage Level</option>
        <option value="liability">Liability Only</option>
        <option value="full">Full Coverage</option>
        <option value="comprehensive">Comprehensive</option>
      </select>
    </div>

    <div class="form-group">
      <label for="auto-current-provider">Current Insurance Provider</label>
      <input
        type="text"
        id="auto-current-provider"
        :value="formData.current_provider"
        @input="updateCurrentProvider"
        class="form-control"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import VehicleInfoFields, { type VehicleInfo } from './VehicleInfoFields.vue'

interface AutoFormData {
  year: number | null
  make: string
  model: string
  vin: string
  coverage_level: string
  current_provider: string
}

interface Props {
  errors?: Record<string, string>
}

withDefaults(defineProps<Props>(), {
  errors: () => ({})
})

const emit = defineEmits<{
  (e: 'update', data: AutoFormData): void
  (e: 'valid', isValid: boolean): void
  (e: 'blur', field: string): void
}>()

const formData = reactive<AutoFormData>({
  year: null,
  make: '',
  model: '',
  vin: '',
  coverage_level: '',
  current_provider: ''
})

// Create a computed property for vehicle info to use with VehicleInfoFields
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
    formData.coverage_level !== ''
  )
})

// Watch for changes and emit to parent
watch(formData, (newData) => {
  emit('update', { ...newData })
}, { deep: true })

// Watch validation state and emit to parent
watch(isFormValid, (isValid) => {
  emit('valid', isValid)
}, { immediate: true })

const updateCoverageLevel = (event: Event) => {
  const select = event.target as HTMLSelectElement
  formData.coverage_level = select.value
}

const updateCurrentProvider = (event: Event) => {
  const input = event.target as HTMLInputElement
  formData.current_provider = input.value
}
</script>

<style scoped>
.auto-quote-form {
  width: 100%;
}

h3 {
  color: var(--color-primary, var(--color-primary));
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: var(--color-primary, var(--color-primary));
}

.form-control.is-invalid {
  border-color: #dc3545;
}

.form-control.is-invalid:focus {
  outline: none;
  border-color: #dc3545;
  box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

select.form-control {
  cursor: pointer;
}

.help-text {
  color: #999;
  font-size: 0.8rem;
  font-style: italic;
  display: block;
  margin-top: 0.25rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
