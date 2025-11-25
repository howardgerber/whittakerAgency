<template>
  <div class="vehicle-info-fields">
    <div class="form-row">
      <div class="form-group">
        <label :for="`${fieldPrefix}-year`">Year *</label>
        <input
          :id="`${fieldPrefix}-year`"
          type="text"
          :value="modelValue.year || ''"
          @input="handleYearInput"
          @blur="$emit('blur', 'year')"
          required
          class="form-control"
          :class="{ 'is-invalid': errors?.year }"
          :placeholder="yearPlaceholder"
        />
        <div v-if="errors?.year" class="error-message">{{ errors.year }}</div>
      </div>

      <div class="form-group">
        <label :for="`${fieldPrefix}-make`">Make *</label>
        <input
          :id="`${fieldPrefix}-make`"
          type="text"
          :value="modelValue.make"
          @input="handleMakeInput"
          @blur="$emit('blur', 'make')"
          maxlength="50"
          required
          class="form-control"
          :class="{ 'is-invalid': errors?.make }"
          :placeholder="makePlaceholder"
        />
        <div v-if="errors?.make" class="error-message">{{ errors.make }}</div>
      </div>

      <div class="form-group">
        <label :for="`${fieldPrefix}-model`">Model *</label>
        <input
          :id="`${fieldPrefix}-model`"
          type="text"
          :value="modelValue.model"
          @input="handleModelInput"
          @blur="$emit('blur', 'model')"
          maxlength="50"
          required
          class="form-control"
          :class="{ 'is-invalid': errors?.model }"
          :placeholder="modelPlaceholder"
        />
        <div v-if="errors?.model" class="error-message">{{ errors.model }}</div>
      </div>
    </div>

    <div v-if="showVIN" class="form-group">
      <label :for="`${fieldPrefix}-vin`">VIN (Optional)</label>
      <input
        :id="`${fieldPrefix}-vin`"
        type="text"
        :value="modelValue.vin"
        @input="handleVINInput"
        @blur="$emit('blur', 'vin')"
        maxlength="17"
        class="form-control"
        :class="{ 'is-invalid': errors?.vin }"
        placeholder="17-character Vehicle Identification Number"
      />
      <small class="help-text">Auto-formats to uppercase. Letters I, O, Q not allowed.</small>
      <div v-if="errors?.vin" class="error-message">{{ errors.vin }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatVIN, formatYear, formatVehicleText } from '@/utils/formatters'

export interface VehicleInfo {
  year: number | null
  make: string
  model: string
  vin?: string
}

interface Props {
  modelValue: VehicleInfo
  errors?: Record<string, string>
  showVIN?: boolean
  fieldPrefix?: string
  yearPlaceholder?: string
  makePlaceholder?: string
  modelPlaceholder?: string
}

const props = withDefaults(defineProps<Props>(), {
  showVIN: true,
  fieldPrefix: 'vehicle',
  yearPlaceholder: 'e.g., 2024',
  makePlaceholder: 'e.g., Toyota',
  modelPlaceholder: 'e.g., Camry'
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: VehicleInfo): void
  (e: 'blur', field: string): void
}>()

const handleYearInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const formatted = formatYear(input.value)
  const year = formatted ? parseInt(formatted, 10) : null
  input.value = formatted

  emit('update:modelValue', {
    ...props.modelValue,
    year
  })
}

const handleMakeInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const make = formatVehicleText(input.value)

  emit('update:modelValue', {
    ...props.modelValue,
    make
  })
}

const handleModelInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const model = formatVehicleText(input.value)

  emit('update:modelValue', {
    ...props.modelValue,
    model
  })
}

const handleVINInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const vin = formatVIN(input.value)

  emit('update:modelValue', {
    ...props.modelValue,
    vin
  })
}
</script>

<style scoped>
@import './form-styles.css';

.vehicle-info-fields {
  width: 100%;
}
</style>
