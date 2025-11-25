<template>
  <div class="event-quote-form">
    <h3>Event Insurance Details</h3>

    <div class="form-row">
      <div class="form-group">
        <label for="event-type">Type of Event *</label>
        <select id="event-type" v-model="formData.event_type" required class="form-control">
          <option value="">Select Event Type</option>
          <option value="wedding">Wedding</option>
          <option value="engagement">Engagement Party</option>
          <option value="anniversary">Anniversary Party</option>
          <option value="retirement">Retirement Party</option>
          <option value="business_meeting">Business Meeting</option>
          <option value="corporate_event">Corporate Event</option>
          <option value="non_profit">Non-Profit Function</option>
          <option value="other">Other Private Event</option>
        </select>
      </div>

      <div class="form-group">
        <label for="event-date">Event Date *</label>
        <input
          type="date"
          id="event-date"
          v-model="formData.event_date"
          required
          :min="minDate"
          class="form-control"
        />
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="event-location">Event Location/Venue *</label>
        <input
          type="text"
          id="event-location"
          v-model="formData.event_location"
          required
          class="form-control"
          placeholder="e.g., Grand Ballroom, Hilton Hotel"
        />
      </div>

      <div class="form-group">
        <label for="event-city">City & State *</label>
        <input
          type="text"
          id="event-city"
          v-model="formData.event_city"
          required
          class="form-control"
          placeholder="e.g., Portland, OR"
        />
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="guest-count">Expected Number of Guests *</label>
        <input
          type="number"
          id="guest-count"
          v-model="formData.guest_count"
          required
          min="1"
          max="500"
          class="form-control"
          placeholder="e.g., 150"
        />
        <small class="help-text">Events with more than 500 guests may not be eligible</small>
      </div>

      <div class="form-group">
        <label for="event-cost">Total Event Cost/Budget *</label>
        <input
          type="text"
          id="event-cost"
          :value="displayValues.event_cost"
          @input="handleCostInput"
          required
          class="form-control"
          placeholder="e.g., $25,000"
        />
        <small class="help-text">Include venue, catering, entertainment, etc.</small>
      </div>
    </div>

    <div class="form-group">
      <label class="section-label">Coverage Needed *</label>
      <div class="coverage-options">
        <label class="checkbox-label">
          <input
            type="checkbox"
            v-model="formData.cancellation_coverage"
            class="checkbox-input"
          />
          <span class="checkbox-text">
            <strong>Event Cancellation Coverage</strong>
            <small>Reimburses lost deposits if you need to cancel or postpone</small>
          </span>
        </label>

        <label class="checkbox-label">
          <input
            type="checkbox"
            v-model="formData.liability_coverage"
            class="checkbox-input"
          />
          <span class="checkbox-text">
            <strong>Event Liability Coverage</strong>
            <small>Protects you if held responsible for accidents or property damage</small>
          </span>
        </label>
      </div>
      <small v-if="!hasAnyCoverage" class="error-text">Please select at least one coverage type</small>
    </div>

    <div class="form-group">
      <label for="deposits-paid">Deposits Already Paid (if any)</label>
      <input
        type="text"
        id="deposits-paid"
        :value="displayValues.deposits_paid"
        @input="handleDepositsInput"
        class="form-control"
        placeholder="e.g., $5,000"
      />
      <small class="help-text">Optional: Amount already paid that you'd want covered</small>
    </div>

    <div class="form-group">
      <label for="event-description">Event Description</label>
      <textarea
        id="event-description"
        v-model="formData.event_description"
        rows="3"
        maxlength="250"
        class="form-control"
        placeholder="Tell us more about your event..."
      ></textarea>
      <small class="help-text">{{ formData.event_description.length }}/250 characters</small>
    </div>

    <!-- Warning for ineligible events -->
    <div v-if="Number(formData.guest_count) > 500" class="alert alert-warning">
      ⚠️ Events with more than 500 guests may not be eligible for coverage. We'll review your request and contact you.
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'
import { formatCurrency } from '@/utils/formatters'

const emit = defineEmits<{
  (e: 'update', data: any): void
  (e: 'valid', isValid: boolean): void
  (e: 'blur', fieldName: string): void
}>()

const formData = reactive({
  event_type: '',
  event_date: '',
  event_location: '',
  event_city: '',
  guest_count: '',
  event_cost: '',
  deposits_paid: '',
  cancellation_coverage: false,
  liability_coverage: false,
  event_description: ''
})

// Display values for formatted inputs
const displayValues = reactive({
  event_cost: '',
  deposits_paid: ''
})

// Min date is today
const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

// Check if at least one coverage is selected
const hasAnyCoverage = computed(() => {
  return formData.cancellation_coverage || formData.liability_coverage
})

// Handle cost input with currency formatting
const handleCostInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const rawValue = input.value.replace(/[^0-9]/g, '')

  if (rawValue === '') {
    formData.event_cost = ''
    displayValues.event_cost = ''
  } else {
    formData.event_cost = rawValue
    displayValues.event_cost = formatCurrency(rawValue)
  }
}

// Handle deposits input with currency formatting
const handleDepositsInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const rawValue = input.value.replace(/[^0-9]/g, '')

  if (rawValue === '') {
    formData.deposits_paid = ''
    displayValues.deposits_paid = ''
  } else {
    formData.deposits_paid = rawValue
    displayValues.deposits_paid = formatCurrency(rawValue)
  }
}

// Watch for form changes
watch(formData, () => {
  emit('update', { ...formData })

  // Validate form
  const isValid = !!(
    formData.event_type &&
    formData.event_date &&
    formData.event_location.trim() &&
    formData.event_city.trim() &&
    formData.guest_count &&
    formData.event_cost &&
    hasAnyCoverage.value
  )

  emit('valid', isValid)
}, { deep: true })
</script>

<style scoped>
.event-quote-form {
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
  font-size: 1rem;
  margin-bottom: 1rem;
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

select.form-control {
  cursor: pointer;
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
  color: #dc3545;
  font-weight: 600;
}

/* Coverage Options */
.coverage-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  border: 2px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.checkbox-label:hover {
  border-color: var(--color-primary);
  background: #f8f9fa;
}

.checkbox-input {
  width: 20px;
  height: 20px;
  margin-right: 1rem;
  cursor: pointer;
  flex-shrink: 0;
  margin-top: 2px;
}

.checkbox-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.checkbox-text strong {
  color: var(--color-primary);
  font-size: 1rem;
}

.checkbox-text small {
  color: #666;
  font-weight: normal;
  font-size: 0.875rem;
}

/* Alert */
.alert {
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.alert-warning {
  background: #fff3cd;
  border: 1px solid #ffc107;
  color: #856404;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
