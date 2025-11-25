<template>
  <div class="travel-quote-form">
    <h3>Travel Insurance Details</h3>

    <!-- U.S. Address Section -->
    <div class="section-header">Your U.S. Address</div>
    <div class="form-row">
      <div class="form-group">
        <label for="street-address">Street Address *</label>
        <input
          type="text"
          id="street-address"
          v-model="formData.street_address"
          required
          class="form-control"
          placeholder="123 Main Street"
        />
      </div>
    </div>

    <div class="form-row city-state-zip">
      <div class="form-group">
        <label for="city">City *</label>
        <input
          type="text"
          id="city"
          v-model="formData.city"
          required
          class="form-control"
          placeholder="Portland"
        />
      </div>

      <div class="form-group">
        <label for="state">State *</label>
        <input
          type="text"
          id="state"
          v-model="formData.state"
          required
          maxlength="2"
          class="form-control"
          placeholder="OR"
        />
      </div>

      <div class="form-group">
        <label for="zip">ZIP Code *</label>
        <input
          type="text"
          id="zip"
          v-model="formData.zip_code"
          required
          maxlength="10"
          class="form-control"
          placeholder="97330"
        />
      </div>
    </div>

    <!-- Trip Details Section -->
    <div class="section-header">Trip Details</div>
    <div class="form-row">
      <div class="form-group">
        <label for="destination">Destination *</label>
        <input
          type="text"
          id="destination"
          v-model="formData.destination"
          required
          class="form-control"
          placeholder="e.g., Paris, France"
        />
      </div>

      <div class="form-group">
        <label for="trip-cost">Total Trip Cost *</label>
        <input
          type="text"
          id="trip-cost"
          :value="displayValues.trip_cost"
          @input="handleTripCostInput"
          required
          class="form-control"
          placeholder="e.g., $5,000"
        />
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="departure-date">Departure Date *</label>
        <input
          type="date"
          id="departure-date"
          v-model="formData.departure_date"
          required
          :min="minDate"
          class="form-control"
        />
      </div>

      <div class="form-group">
        <label for="return-date">Return Date *</label>
        <input
          type="date"
          id="return-date"
          v-model="formData.return_date"
          required
          :min="formData.departure_date || minDate"
          class="form-control"
        />
      </div>

      <div class="form-group">
        <label for="deposit-date">Initial Trip Deposit Date</label>
        <input
          type="date"
          id="deposit-date"
          v-model="formData.deposit_date"
          :max="formData.departure_date || undefined"
          class="form-control"
        />
      </div>
    </div>

    <!-- Travelers Section -->
    <div class="section-header">Travelers</div>
    <p class="form-instructions">Add the legal name and birthdate for each traveler.</p>

    <div class="travelers-grid">
      <div class="grid-header">
        <div class="header-name">Legal Name *</div>
        <div class="header-birthdate">Date of Birth *</div>
        <div class="header-age">Age</div>
        <div class="header-actions"></div>
      </div>

      <div v-for="(traveler, index) in travelers" :key="traveler.id" class="traveler-row">
        <div class="traveler-name">
          <input
            type="text"
            v-model="traveler.legal_name"
            required
            :class="['form-control', { 'invalid': traveler.touched && !isValidFullName(traveler.legal_name) }]"
            placeholder="First Last"
            @input="updateFormData"
            @blur="traveler.touched = true"
          />
        </div>

        <div class="traveler-birthdate">
          <input
            type="date"
            v-model="traveler.birthdate"
            required
            :max="maxDate"
            class="form-control"
            @change="calculateAge(index)"
          />
        </div>

        <div class="traveler-age">
          <span class="age-display">{{ traveler.age || '-' }}</span>
        </div>

        <div class="traveler-actions">
          <button
            type="button"
            @click="removeTraveler(index)"
            class="btn-remove"
            :disabled="travelers.length === 1"
            title="Remove traveler"
          >
            ✕
          </button>
        </div>
      </div>
    </div>

    <button type="button" @click="addTraveler" class="btn-add-item">
      + Add Another Traveler
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { formatCurrency } from '@/utils/formatters'
import { ValidationRules } from '@/utils/validation'

const emit = defineEmits<{
  (e: 'update', data: any): void
  (e: 'valid', isValid: boolean): void
  (e: 'blur', fieldName: string): void
}>()

interface Traveler {
  id: number
  legal_name: string
  birthdate: string
  age: number | null
  touched: boolean
}

const formData = reactive({
  street_address: '',
  city: '',
  state: '',
  zip_code: '',
  destination: '',
  trip_cost: '',
  departure_date: '',
  return_date: '',
  deposit_date: ''
})

// Display values for formatted inputs
const displayValues = reactive({
  trip_cost: ''
})

let nextId = 1

// Initialize with one empty traveler
const travelers = ref<Traveler[]>([
  {
    id: nextId++,
    legal_name: '',
    birthdate: '',
    age: null,
    touched: false
  }
])

// Validate full name using shared validation rules
const isValidFullName = (name: string): boolean => {
  if (!name || !name.trim()) return false
  return ValidationRules.fullName.validate(name).isValid
}

// Min date is today
const minDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

// Max date is today (for birthdates and deposit date)
const maxDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

// Calculate age from birthdate
const calculateAge = (index: number) => {
  const traveler = travelers.value[index]
  if (!traveler.birthdate) {
    traveler.age = null
    return
  }

  const birthDate = new Date(traveler.birthdate)
  const today = new Date()
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()

  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }

  traveler.age = age
  updateFormData()
}

// Add a new traveler
const addTraveler = () => {
  travelers.value.push({
    id: nextId++,
    legal_name: '',
    birthdate: '',
    age: null,
    touched: false
  })
}

// Remove a traveler
const removeTraveler = (index: number) => {
  if (travelers.value.length > 1) {
    travelers.value.splice(index, 1)
    updateFormData()
  }
}

// Handle trip cost input with currency formatting
const handleTripCostInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const rawValue = input.value.replace(/[^0-9]/g, '')

  if (rawValue === '') {
    formData.trip_cost = ''
    displayValues.trip_cost = ''
  } else {
    formData.trip_cost = rawValue
    displayValues.trip_cost = formatCurrency(rawValue)
  }
}

// Update form data and emit
const updateFormData = () => {
  const data = {
    ...formData,
    travelers: travelers.value.map(t => ({
      legal_name: t.legal_name,
      birthdate: t.birthdate,
      age: t.age
    }))
  }

  emit('update', data)

  // Validate: all address fields, trip details, and at least one complete traveler with valid full name
  const hasValidTraveler = travelers.value.some(t => isValidFullName(t.legal_name) && t.birthdate)
  const isValid = !!(
    formData.street_address.trim() &&
    formData.city.trim() &&
    formData.state.trim() &&
    formData.zip_code.trim() &&
    formData.destination.trim() &&
    formData.trip_cost &&
    formData.departure_date &&
    formData.return_date &&
    hasValidTraveler
  )

  emit('valid', isValid)
}

// Watch for changes
watch([formData, travelers], () => {
  updateFormData()
}, { deep: true })
</script>

<style scoped>
.travel-quote-form {
  width: 100%;
}

h3 {
  color: var(--color-primary);
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
}

.section-header {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-primary);
  margin: 2rem 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--color-primary);
}

.section-header:first-of-type {
  margin-top: 0;
}

.form-instructions {
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

/* Specific layout for City/State/ZIP row */
.form-row.city-state-zip {
  grid-template-columns: 1fr 100px 140px;
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

.form-control.invalid {
  border-color: #dc3545;
  border-width: 2px;
}

.form-control.invalid:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

.short-input {
  max-width: 120px;
}

textarea.form-control {
  resize: vertical;
  font-family: inherit;
}

/* Travelers Grid */
.travelers-grid {
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.grid-header {
  display: grid;
  grid-template-columns: 1fr 180px 60px 50px;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border-bottom: 2px solid #ddd;
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.traveler-row {
  display: grid;
  grid-template-columns: 1fr 180px 60px 50px;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  align-items: center;
}

.traveler-row:last-child {
  border-bottom: none;
}

.traveler-name,
.traveler-birthdate,
.traveler-age {
  display: flex;
  align-items: center;
}

.age-display {
  color: #666;
  font-weight: 600;
  font-size: 1rem;
}

.traveler-actions {
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove {
  width: 32px;
  height: 32px;
  border: 1px solid #dc3545;
  background: white;
  color: #dc3545;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-remove:hover:not(:disabled) {
  background: #dc3545;
  color: white;
}

.btn-remove:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.btn-add-item {
  padding: 0.75rem 1.5rem;
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.btn-add-item:hover {
  background: var(--color-primary);
  color: white;
}

@media (max-width: 968px) {
  .grid-header,
  .traveler-row {
    grid-template-columns: 1fr 150px 50px 45px;
    gap: 0.5rem;
    padding: 0.75rem;
  }

  .grid-header {
    font-size: 0.85rem;
  }

  .form-control {
    font-size: 0.9rem;
    padding: 0.5rem;
  }

  .short-input {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  /* City/State/ZIP row stacks on mobile */
  .form-row.city-state-zip {
    grid-template-columns: 1fr;
  }

  .grid-header {
    display: none;
  }

  .traveler-row {
    grid-template-columns: 1fr;
    gap: 0.75rem;
    padding: 1rem;
    position: relative;
  }

  .traveler-actions {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
  }

  .traveler-age {
    justify-content: flex-start;
  }

  .age-display::before {
    content: 'Age: ';
    color: #666;
    font-weight: normal;
    margin-right: 0.25rem;
  }
}
</style>
