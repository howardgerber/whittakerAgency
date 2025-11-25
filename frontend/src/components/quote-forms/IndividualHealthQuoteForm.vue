<template>
  <div class="individual-health-quote-form">
    <h3>Individual Health Insurance Details</h3>

    <div class="form-group">
      <label class="section-label">Select Health Insurance Types Needed *</label>
      <p class="help-text">Check all that apply</p>

      <div class="checkbox-grid">
        <label class="checkbox-card" :class="{ selected: formData.short_term_medical }">
          <input
            type="checkbox"
            v-model="formData.short_term_medical"
            class="checkbox-input"
          />
          <div class="checkbox-icon">🏥</div>
          <div class="checkbox-label">Short Term Medical</div>
        </label>

        <label class="checkbox-card" :class="{ selected: formData.accident_insurance }">
          <input
            type="checkbox"
            v-model="formData.accident_insurance"
            class="checkbox-input"
          />
          <div class="checkbox-icon">🩹</div>
          <div class="checkbox-label">Accident Insurance</div>
        </label>

        <label class="checkbox-card" :class="{ selected: formData.critical_illness }">
          <input
            type="checkbox"
            v-model="formData.critical_illness"
            class="checkbox-input"
          />
          <div class="checkbox-icon">💙</div>
          <div class="checkbox-label">Critical Illness</div>
        </label>

        <label class="checkbox-card" :class="{ selected: formData.dental_insurance }">
          <input
            type="checkbox"
            v-model="formData.dental_insurance"
            class="checkbox-input"
          />
          <div class="checkbox-icon">🦷</div>
          <div class="checkbox-label">Dental Insurance</div>
        </label>

        <label class="checkbox-card" :class="{ selected: formData.medicare_insurance }">
          <input
            type="checkbox"
            v-model="formData.medicare_insurance"
            class="checkbox-input"
          />
          <div class="checkbox-icon">📋</div>
          <div class="checkbox-label">Medicare Insurance</div>
        </label>
      </div>

      <small v-if="!hasSelection" class="error-text">Please select at least one insurance type</small>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="health-num-people">Number of People to Insure *</label>
        <input
          type="number"
          id="health-num-people"
          v-model="formData.num_people"
          required
          min="1"
          max="20"
          class="form-control"
          placeholder="e.g., 3"
        />
        <small class="help-text">Include yourself and dependents</small>
      </div>

      <div class="form-group">
        <label for="health-age-range">Primary Applicant Age</label>
        <select id="health-age-range" v-model="formData.age_range" class="form-control">
          <option value="">Select Age Range</option>
          <option value="18-25">18-25</option>
          <option value="26-35">26-35</option>
          <option value="36-45">36-45</option>
          <option value="46-55">46-55</option>
          <option value="56-64">56-64</option>
          <option value="65+">65+</option>
        </select>
      </div>
    </div>

    <div class="form-group">
      <label for="health-current-insurance">Current Insurance Status</label>
      <select id="health-current-insurance" v-model="formData.current_insurance" class="form-control">
        <option value="">Select Status</option>
        <option value="none">No Current Coverage</option>
        <option value="employer">Employer Coverage</option>
        <option value="individual">Individual Plan</option>
        <option value="medicare">Medicare</option>
        <option value="medicaid">Medicaid</option>
      </select>
    </div>

    <div class="form-group">
      <label for="health-coverage-start">Desired Coverage Start Date</label>
      <input
        type="date"
        id="health-coverage-start"
        v-model="formData.coverage_start_date"
        class="form-control"
        :min="minDate"
      />
      <small class="help-text">When do you need coverage to begin?</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed, watch } from 'vue'

const emit = defineEmits<{
  (e: 'update', data: any): void
  (e: 'valid', isValid: boolean): void
  (e: 'blur', fieldName: string): void
}>()

const formData = reactive({
  short_term_medical: false,
  accident_insurance: false,
  critical_illness: false,
  dental_insurance: false,
  medicare_insurance: false,
  num_people: '',
  age_range: '',
  current_insurance: '',
  coverage_start_date: ''
})

// Check if at least one insurance type is selected
const hasSelection = computed(() => {
  return formData.short_term_medical ||
    formData.accident_insurance ||
    formData.critical_illness ||
    formData.dental_insurance ||
    formData.medicare_insurance
})

// Minimum date is today
const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

// Watch for form changes
watch(formData, () => {
  emit('update', { ...formData })

  // Validate form
  const isValid = hasSelection.value &&
    formData.num_people !== '' &&
    parseInt(formData.num_people) > 0

  emit('valid', isValid)
}, { deep: true })
</script>

<style scoped>
.individual-health-quote-form {
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

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.section-label {
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
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
  font-weight: normal;
}

.error-text {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #d9534f;
  font-weight: 600;
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.checkbox-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.5rem 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
  position: relative;
}

.checkbox-card:hover {
  border-color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 61, 165, 0.1);
}

.checkbox-card.selected {
  border-color: var(--color-primary);
  background: #f0f4ff;
  box-shadow: 0 2px 8px rgba(0, 61, 165, 0.15);
}

.checkbox-input {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.checkbox-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.checkbox-label {
  text-align: center;
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
  line-height: 1.3;
}

select.form-control {
  cursor: pointer;
}

@media (max-width: 768px) {
  .checkbox-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }

  .checkbox-card {
    padding: 1rem 0.5rem;
  }

  .checkbox-icon {
    font-size: 2rem;
  }

  .checkbox-label {
    font-size: 0.8rem;
  }
}
</style>
