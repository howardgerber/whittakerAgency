<template>
  <div class="collectibles-quote-form">
    <h3>Collectibles Insurance Details</h3>

    <div class="form-group">
      <label for="collectibles-amount">Coverage Amount Requested *</label>
      <input
        type="text"
        id="collectibles-amount"
        :value="displayValues.coverage_amount"
        @input="handleAmountInput"
        required
        class="form-control"
        placeholder="e.g., $50,000"
        inputmode="numeric"
      />
      <small class="help-text">Enter the total value of collectibles you wish to insure</small>
    </div>

    <div class="form-group checkbox-group">
      <label class="checkbox-label">
        <input
          type="checkbox"
          v-model="formData.has_alarm_system"
          :disabled="alarmRequired"
          class="checkbox-input"
        />
        <span>Alarm System Installed</span>
      </label>
      <small v-if="alarmRequired" class="alarm-note required">
        ⚠️ Alarm system is required for coverage amounts over $500,000
      </small>
      <small v-else class="alarm-note">
        An alarm system may reduce your premium
      </small>
    </div>

    <div class="form-group">
      <label for="collectibles-description">Description of Collectibles *</label>
      <textarea
        id="collectibles-description"
        v-model="formData.description"
        required
        rows="4"
        maxlength="250"
        class="form-control"
        placeholder="Describe your collectibles (e.g., art, coins, stamps, antiques, memorabilia, etc.)"
      ></textarea>
      <small class="help-text">{{ formData.description.length }}/250 characters</small>
    </div>

    <div class="form-group">
      <label for="collectibles-storage">Storage Location</label>
      <select id="collectibles-storage" v-model="formData.storage_location" class="form-control">
        <option value="">Select Storage Location</option>
        <option value="home">Home</option>
        <option value="safe_deposit">Safe Deposit Box</option>
        <option value="secure_facility">Secure Storage Facility</option>
        <option value="mixed">Multiple Locations</option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import { formatCurrency, parseFormattedCurrency } from '@/utils/formatters'

const emit = defineEmits<{
  (e: 'update', data: any): void
  (e: 'valid', isValid: boolean): void
  (e: 'blur', fieldName: string): void
}>()

const formData = reactive({
  coverage_amount: '',
  has_alarm_system: false,
  description: '',
  storage_location: ''
})

const displayValues = reactive({
  coverage_amount: ''
})

// Check if alarm is required (amount > $500,000)
const alarmRequired = computed(() => {
  const amount = parseFormattedCurrency(formData.coverage_amount)
  return amount !== null && amount > 500000
})

// Auto-check alarm if required
watch(alarmRequired, (required) => {
  if (required) {
    formData.has_alarm_system = true
  }
})

const handleAmountInput = (e: Event) => {
  const target = e.target as HTMLInputElement
  const rawValue = parseFormattedCurrency(target.value)

  if (rawValue !== null) {
    formData.coverage_amount = rawValue.toString()
    displayValues.coverage_amount = formatCurrency(rawValue.toString())
  } else {
    formData.coverage_amount = ''
    displayValues.coverage_amount = ''
  }
}

// Watch for form changes
watch(formData, () => {
  emit('update', { ...formData })

  // Validate form
  const amount = parseFormattedCurrency(formData.coverage_amount)
  const isValid = !!(
    formData.coverage_amount &&
    amount !== null &&
    amount > 0 &&
    formData.description.trim() &&
    (!alarmRequired.value || formData.has_alarm_system)
  )

  emit('valid', isValid)
}, { deep: true })
</script>

<style scoped>
.collectibles-quote-form {
  width: 100%;
}

h3 {
  color: var(--color-primary);
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
}

.form-group {
  margin-bottom: 1.5rem;
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
  border-color: var(--color-primary);
}

textarea.form-control {
  resize: vertical;
  font-family: inherit;
}

.help-text {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #666;
}

.checkbox-group {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-weight: normal;
  margin-bottom: 0.5rem;
}

.checkbox-label span {
  font-weight: 600;
}

.checkbox-input {
  width: 20px;
  height: 20px;
  margin-right: 0.75rem;
  cursor: pointer;
}

.checkbox-input:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.alarm-note {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #666;
}

.alarm-note.required {
  color: #d9534f;
  font-weight: 600;
}

select.form-control {
  cursor: pointer;
}
</style>
