<template>
  <div class="claim-submit-page">
    <div class="container">
      <h1>File an Insurance Claim</h1>
      <p class="subtitle">Provide details about your incident and we'll process your claim promptly.</p>

      <!-- Progress Indicator -->
      <div class="progress-stepper">
        <div
          v-for="step in steps"
          :key="step.number"
          class="step-item"
          :class="{
            'completed': currentStep > step.number,
            'active': currentStep === step.number,
            'upcoming': currentStep < step.number
          }"
        >
          <div class="step-circle">
            <span v-if="currentStep > step.number" class="checkmark">✓</span>
            <span v-else>{{ step.number }}</span>
          </div>
          <div class="step-label">{{ step.label }}</div>
        </div>
        <div class="progress-line"></div>
      </div>

      <form @submit.prevent="handleSubmit" class="claim-form">
        <!-- Step 1: Incident Information -->
        <div v-show="currentStep === 1" class="step-content">
          <h2>Incident Information</h2>
          <p class="step-description">Tell us what type of insurance claim you're filing.</p>

          <div class="incident-row">
            <div class="form-group">
              <label for="insurance-category">Insurance Category *</label>
              <select
                id="insurance-category"
                v-model="formState.category"
                required
                class="form-control"
              >
                <option value="">Select Category</option>
                <option value="vehicle">Vehicle</option>
                <option value="property">Property</option>
                <option value="life">Life</option>
                <option value="business">Business</option>
                <option value="identity_protection">Identity Protection</option>
                <option value="other">Other</option>
              </select>
            </div>

            <!-- Subtype Selector (always visible, disabled until category selected) -->
            <div class="form-group">
              <label for="insurance-subtype">Type *</label>
              <select
                id="insurance-subtype"
                v-model="formState.subcategory"
                :required="hasSubcategories"
                :disabled="!formState.category"
                class="form-control"
              >
                <option value="">Select Type</option>
                <option v-for="subtype in subtypeOptions" :key="subtype.value" :value="subtype.value">
                  {{ subtype.label }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="incident-date">Incident Date *</label>
              <input
                type="date"
                id="incident-date"
                v-model="formState.incidentDate"
                required
                :max="maxDate"
                :min="minDate"
                @blur="validateIncidentDate"
                class="form-control"
              />
            </div>
          </div>
        </div>

        <!-- Step 2: Claim Details (Dynamic) -->
        <div v-show="currentStep === 2" class="step-content">
          <h2>Claim Details</h2>
          <p class="step-description">Provide specific details about your claim.</p>

          <div class="dynamic-section">
            <component
              :is="currentFormComponent"
              :key="selectedType"
              :selectedSubtype="formState.subcategory"
              :errors="validationErrors"
              @update="handleFormUpdate"
              @valid="handleValidationUpdate"
              @blur="handleFieldBlur"
            />
          </div>
        </div>

        <!-- Step 3: Incident Summary -->
        <div v-show="currentStep === 3" class="step-content">
          <h2>Incident Summary</h2>
          <p class="step-description">Describe what happened in your own words.</p>

          <div class="form-group">
            <label for="incident-summary">What Happened? *</label>
            <textarea
              id="incident-summary"
              v-model="formState.incidentSummary"
              rows="5"
              maxlength="250"
              required
              class="form-control"
              placeholder="Describe the incident (minimum 10 characters)"
            ></textarea>
            <small :class="summaryCharClass">{{ formState.incidentSummary.length }}/250 characters</small>
          </div>

          <div class="form-group">
            <label for="additional-notes">Additional Notes</label>
            <textarea
              id="additional-notes"
              v-model="formState.additionalNotes"
              rows="4"
              maxlength="250"
              class="form-control"
              placeholder="Any other information we should know (optional)"
            ></textarea>
            <small class="char-count">{{ formState.additionalNotes.length }}/250 characters</small>
          </div>
        </div>

        <!-- Step 4: Contact Information -->
        <div v-show="currentStep === 4" class="step-content">
          <h2>Contact Information</h2>
          <p class="step-description">Let us know how and when to reach you.</p>

          <div class="form-group">
            <label>How should we contact you? *</label>
            <div class="radio-group">
              <label class="radio-label">
                <input
                  type="radio"
                  v-model="formState.contactPreference"
                  value="email"
                  required
                />
                Email
              </label>
              <label class="radio-label">
                <input
                  type="radio"
                  v-model="formState.contactPreference"
                  value="phone"
                  required
                />
                Phone
              </label>
              <label class="radio-label">
                <input
                  type="radio"
                  v-model="formState.contactPreference"
                  value="either"
                  required
                />
                Either
              </label>
            </div>
          </div>

          <div class="contact-schedule-row">
            <div class="form-group">
              <label for="appointment-date">Preferred Date (Optional)</label>
              <input
                type="date"
                id="appointment-date"
                v-model="formState.appointmentRequested"
                :min="minAppointmentDate"
                @blur="validateAppointmentDate"
                :class="['form-control', { 'invalid': appointmentDateError }]"
              />
              <small v-if="appointmentDateError" class="error-text">
                {{ appointmentDateError }}
              </small>
            </div>

            <div class="form-group">
              <label for="preferred-time">Preferred Contact Time *</label>
              <select
                id="preferred-time"
                v-model="formState.preferredContactTime"
                required
                class="form-control"
              >
                <option value="">Select Time</option>
                <option value="morning">Morning (8am - 12pm)</option>
                <option value="afternoon">Afternoon (12pm - 5pm)</option>
                <option value="evening">Evening (5pm - 8pm)</option>
                <option value="anytime">Anytime</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="form-navigation">
          <button
            v-if="currentStep > 1"
            type="button"
            @click="previousStep"
            class="btn btn-secondary"
          >
            Back
          </button>
          <div v-else></div>

          <button
            v-if="currentStep < 4"
            type="button"
            @click="nextStep"
            :disabled="!isCurrentStepValid"
            class="btn btn-primary"
          >
            Continue
          </button>
          <button
            v-else
            type="submit"
            :disabled="isSubmitting || !isCurrentStepValid"
            class="btn btn-primary"
          >
            {{ isSubmitting ? 'Submitting...' : 'Submit Claim' }}
          </button>
        </div>

        <!-- Error Messages -->
        <div v-if="errorMessage" class="alert alert-error">
          {{ errorMessage }}
        </div>
      </form>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="modal-overlay" @click="handleModalClick">
      <div class="modal-content" @click.stop>
        <div class="modal-icon">✓</div>
        <h2>Claim Submitted Successfully!</h2>
        <p class="modal-message">{{ successMessage }}</p>
        <p class="countdown-text">Redirecting to dashboard in <span class="countdown">{{ countdown }}</span> seconds...</p>
        <div class="modal-actions">
          <button @click="redirectNow" class="btn btn-primary">Go to Dashboard Now</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, reactive } from 'vue'
import { useRouter } from 'vue-router'
import claimService from '@/services/claims'
import { cleanText } from '@/utils/formatters'
import { ValidationRules } from '@/utils/validation'

// Import claim form components
import AutoClaimForm from '@/components/claim-forms/AutoClaimForm.vue'
import MotorcycleClaimForm from '@/components/claim-forms/MotorcycleClaimForm.vue'
import AtvClaimForm from '@/components/claim-forms/AtvClaimForm.vue'
import RoadsideClaimForm from '@/components/claim-forms/RoadsideClaimForm.vue'
import SnowmobileClaimForm from '@/components/claim-forms/SnowmobileClaimForm.vue'
import BoatClaimForm from '@/components/claim-forms/BoatClaimForm.vue'
import RvClaimForm from '@/components/claim-forms/RvClaimForm.vue'
import VehicleProtectionClaimForm from '@/components/claim-forms/VehicleProtectionClaimForm.vue'
import HomeownersClaimForm from '@/components/claim-forms/HomeownersClaimForm.vue'
import RentersClaimForm from '@/components/claim-forms/RentersClaimForm.vue'
import CondoClaimForm from '@/components/claim-forms/CondoClaimForm.vue'
import LandlordClaimForm from '@/components/claim-forms/LandlordClaimForm.vue'
import MobileHomeClaimForm from '@/components/claim-forms/MobileHomeClaimForm.vue'
import LifeClaimForm from '@/components/claim-forms/LifeClaimForm.vue'
import BusinessClaimForm from '@/components/claim-forms/BusinessClaimForm.vue'
import IdentityProtectionClaimForm from '@/components/claim-forms/IdentityProtectionClaimForm.vue'
import UmbrellaClaimForm from '@/components/claim-forms/UmbrellaClaimForm.vue'
import HealthClaimForm from '@/components/claim-forms/HealthClaimForm.vue'
import PetClaimForm from '@/components/claim-forms/PetClaimForm.vue'
import EventClaimForm from '@/components/claim-forms/EventClaimForm.vue'
import TravelClaimForm from '@/components/claim-forms/TravelClaimForm.vue'
import JewelryClaimForm from '@/components/claim-forms/JewelryClaimForm.vue'
import CollectiblesClaimForm from '@/components/claim-forms/CollectiblesClaimForm.vue'

const router = useRouter()

// Current step (1-4)
const currentStep = ref(1)

// Steps configuration
const steps = [
  { number: 1, label: 'Incident Info' },
  { number: 2, label: 'Claim Details' },
  { number: 3, label: 'Summary' },
  { number: 4, label: 'Contact' }
]

// Form state - preserves all data across steps
const formState = reactive({
  category: '',
  subcategory: '',
  incidentDate: '',
  claimData: {} as any,
  incidentSummary: '',
  additionalNotes: '',
  contactPreference: '',
  preferredContactTime: '',
  appointmentRequested: ''
})

// Submission state
const isSubmitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const showSuccessModal = ref(false)
const countdown = ref(10)

// Dynamic form validation
const isFormValid = ref(false)
const validationErrors = ref<Record<string, string>>({})
const appointmentDateError = ref('')

// Countdown timer
let countdownInterval: number | null = null

// Date constraints
const today = new Date()
const maxDate = today.toISOString().split('T')[0]
const twoYearsAgo = new Date(today.getFullYear() - 2, today.getMonth(), today.getDate())
const minDate = twoYearsAgo.toISOString().split('T')[0]

// Appointment constraints - can't be in the past (date only, not datetime)
const minAppointmentDate = new Date().toISOString().slice(0, 10)

// Validate incident date using shared validation rules
const validateIncidentDate = () => {
  const result = ValidationRules.incidentDate.validate(formState.incidentDate)
  if (!result.isValid) {
    // Reset to today's date if invalid
    formState.incidentDate = maxDate
  }
}

// Validate appointment date - cannot be in the past
const validateAppointmentDate = () => {
  appointmentDateError.value = ''

  if (!formState.appointmentRequested) {
    return // Optional field, empty is ok
  }

  const selectedDate = new Date(formState.appointmentRequested)
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  if (selectedDate < today) {
    appointmentDateError.value = 'Date in past - defaulted to tomorrow'
    // Set to tomorrow instead of clearing
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    formState.appointmentRequested = tomorrow.toISOString().slice(0, 10)
  }
}

// Categories that have subcategories
const categoriesWithSubcategories = ['vehicle', 'property', 'other']

// Check if current category has subcategories
const hasSubcategories = computed(() => {
  return categoriesWithSubcategories.includes(formState.category)
})

// Subtype options based on selected category
const subtypeOptions = computed(() => {
  const options: Record<string, Array<{ value: string; label: string }>> = {
    vehicle: [
      { value: 'auto', label: 'Auto' },
      { value: 'motorcycle', label: 'Motorcycle' },
      { value: 'atv', label: 'ATV/Off-Road' },
      { value: 'roadside', label: 'Roadside' },
      { value: 'snowmobile', label: 'Snowmobile' },
      { value: 'boat', label: 'Boat' },
      { value: 'rv', label: 'RV' },
      { value: 'vehicle_protection', label: 'Vehicle Protection' }
    ],
    property: [
      { value: 'homeowners', label: 'Homeowners' },
      { value: 'renters', label: 'Renters' },
      { value: 'condo', label: 'Condo' },
      { value: 'landlord', label: 'Landlord' },
      { value: 'mobile_home', label: 'Mobile Home' }
    ],
    other: [
      { value: 'umbrella', label: 'Personal Umbrella Policy' },
      { value: 'individual_health', label: 'Individual Health' },
      { value: 'pet', label: 'Pet' },
      { value: 'event', label: 'Event' },
      { value: 'travel', label: 'Travel' },
      { value: 'jewelry', label: 'Jewelry' },
      { value: 'collectibles', label: 'Collectibles' }
    ]
  }
  return options[formState.category] || []
})

// Combined insurance type
const selectedType = computed(() => {
  if (!hasSubcategories.value && formState.category) {
    return formState.category
  }

  if (formState.category && formState.subcategory) {
    return `${formState.category}_${formState.subcategory}`
  }

  return ''
})

// Map insurance types to components
const formComponentMap: Record<string, any> = {
  // Vehicle forms
  vehicle_auto: AutoClaimForm,
  vehicle_motorcycle: MotorcycleClaimForm,
  vehicle_atv: AtvClaimForm,
  vehicle_roadside: RoadsideClaimForm,
  vehicle_snowmobile: SnowmobileClaimForm,
  vehicle_boat: BoatClaimForm,
  vehicle_rv: RvClaimForm,
  vehicle_vehicle_protection: VehicleProtectionClaimForm,

  // Property forms
  property_homeowners: HomeownersClaimForm,
  property_renters: RentersClaimForm,
  property_condo: CondoClaimForm,
  property_landlord: LandlordClaimForm,
  property_mobile_home: MobileHomeClaimForm,

  // Categories without subcategories
  life: LifeClaimForm,
  business: BusinessClaimForm,
  identity_protection: IdentityProtectionClaimForm,

  // Other services forms
  other_umbrella: UmbrellaClaimForm,
  other_individual_health: HealthClaimForm,
  other_pet: PetClaimForm,
  other_event: EventClaimForm,
  other_travel: TravelClaimForm,
  other_jewelry: JewelryClaimForm,
  other_collectibles: CollectiblesClaimForm
}

// Get current form component based on selected type
const currentFormComponent = computed(() => {
  return selectedType.value ? formComponentMap[selectedType.value] : null
})

// Character count styling
const summaryCharClass = computed(() => {
  const length = formState.incidentSummary.length
  const max = 250

  if (length >= max) return 'at-limit'
  if (length / max >= 0.9) return 'near-limit'
  return 'normal'
})

// Step validation
const isCurrentStepValid = computed(() => {
  switch (currentStep.value) {
    case 1:
      // Step 1: category + subcategory (if applicable) + incident date required
      if (!formState.category || !formState.incidentDate) return false
      if (hasSubcategories.value && !formState.subcategory) return false
      return true

    case 2:
      // Step 2: dynamic form must be valid
      return isFormValid.value

    case 3:
      // Step 3: incident summary must have content (at least 10 chars)
      return formState.incidentSummary.trim().length >= 10

    case 4:
      // Step 4: contact preference + preferred contact time required
      return formState.contactPreference !== '' && formState.preferredContactTime !== ''

    default:
      return false
  }
})

// Reset subcategory when category changes
watch(() => formState.category, () => {
  formState.subcategory = ''
  formState.claimData = {}
  isFormValid.value = false
  validationErrors.value = {}
})

// Reset form data when subtype changes
watch(() => formState.subcategory, () => {
  formState.claimData = {}
  isFormValid.value = false
  validationErrors.value = {}
})

// Handle form data updates from child components
const handleFormUpdate = (data: any) => {
  formState.claimData = data
}

// Handle validation state updates from child components
const handleValidationUpdate = (isValid: boolean) => {
  isFormValid.value = isValid
}

// Handle field blur events from child components
const handleFieldBlur = (_fieldName: string) => {
  // Can add validation logic here if needed
}

// Navigation functions
const nextStep = () => {
  if (isCurrentStepValid.value && currentStep.value < 4) {
    currentStep.value++
    scrollToTop()
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    scrollToTop()
  }
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Modal and countdown functions
const startCountdown = () => {
  countdown.value = 10
  countdownInterval = window.setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      redirectNow()
    }
  }, 1000)
}

const stopCountdown = () => {
  if (countdownInterval !== null) {
    clearInterval(countdownInterval)
    countdownInterval = null
  }
}

const redirectNow = () => {
  stopCountdown()
  router.push('/dashboard')
}

const handleModalClick = () => {
  redirectNow()
}

// Form submission
const handleSubmit = async () => {
  if (currentStep.value !== 4 || !isCurrentStepValid.value) return

  isSubmitting.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    await claimService.createClaim({
      category: formState.category,
      subcategory: formState.subcategory || null,
      incident_date: formState.incidentDate,
      incident_summary: cleanText(formState.incidentSummary),
      claim_data: formState.claimData,
      appointment_requested: formState.appointmentRequested || null,
      contact_preference: formState.contactPreference,
      preferred_contact_time: formState.preferredContactTime || null,
      additional_notes: formState.additionalNotes ? cleanText(formState.additionalNotes) : null
    })

    successMessage.value = 'Your claim has been submitted successfully! Our team will contact you within 1-2 business days via your preferred contact method.'
    showSuccessModal.value = true
    startCountdown()

  } catch (error: any) {
    console.error('Error submitting claim:', error)
    errorMessage.value = error.response?.data?.detail || 'Failed to submit claim. Please try again.'
    scrollToTop()
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.claim-submit-page {
  min-height: calc(100vh - 200px);
  padding: 3rem 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
}

h1 {
  color: var(--color-primary);
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  margin-bottom: 2.5rem;
}

/* Progress Stepper */
.progress-stepper {
  position: relative;
  display: flex;
  justify-content: space-between;
  margin-bottom: 3rem;
  padding: 0 2rem;
}

.progress-line {
  position: absolute;
  top: 20px;
  left: 10%;
  right: 10%;
  height: 3px;
  background: #e0e0e0;
  z-index: 0;
}

.step-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  z-index: 1;
  flex: 1;
}

.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  border: 3px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.1rem;
  color: #999;
  transition: all 0.3s ease;
}

.step-item.active .step-circle {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background: #e8f0fe;
  box-shadow: 0 0 0 4px rgba(0, 61, 165, 0.1);
}

.step-item.completed .step-circle {
  border-color: #28a745;
  background: #28a745;
  color: white;
}

.checkmark {
  font-size: 1.4rem;
  font-weight: bold;
}

.step-label {
  font-size: 0.85rem;
  font-weight: 500;
  color: #666;
  text-align: center;
}

.step-item.active .step-label {
  color: var(--color-primary);
  font-weight: 600;
}

.step-item.completed .step-label {
  color: #28a745;
  font-weight: 600;
}

/* Form */
.claim-form {
  background: white;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.step-content {
  /* Removed excessive min-height */
}

.step-content h2 {
  color: var(--color-primary);
  font-size: 1.6rem;
  margin-bottom: 0.5rem;
}

.step-description {
  color: #666;
  margin-bottom: 2rem;
  font-size: 1.05rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

/* Incident row - 3 fields side by side */
.incident-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.incident-row .form-group {
  margin-bottom: 0;
}

/* Removed invisible class - Type field always visible */

.contact-schedule-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.contact-schedule-row .form-group {
  margin-bottom: 0;
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
  box-shadow: 0 0 0 3px rgba(0, 61, 165, 0.1);
}

.form-control.invalid {
  border-color: #dc3545;
  border-width: 2px;
}

.form-control.invalid:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.25);
}

.error-text {
  color: #dc3545;
  font-size: 0.875rem;
  display: block;
  margin-top: 0.25rem;
}

select.form-control {
  cursor: pointer;
}

textarea.form-control {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.radio-group {
  display: flex;
  gap: 1.5rem;
  margin-top: 0.5rem;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 400;
  cursor: pointer;
}

.radio-label input[type="radio"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

small {
  color: #666;
  font-size: 0.875rem;
  display: block;
  margin-top: 0.25rem;
}

.help-text {
  font-style: italic;
  color: #999;
}

.char-count {
  color: #666;
}

small.normal {
  color: #666;
}

small.near-limit {
  color: #ff9800;
  font-weight: 600;
}

small.at-limit {
  color: #f44336;
  font-weight: 600;
}

.dynamic-section {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

/* Navigation Buttons */
.form-navigation {
  margin-top: 2.5rem;
  padding-top: 2rem;
  border-top: 2px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
  min-width: 120px;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 61, 165, 0.3);
}

.btn-secondary {
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

.btn-secondary:hover {
  background: #f5f7fa;
}

.btn:disabled {
  background: #cccccc !important;
  color: #666666 !important;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
  border-color: #cccccc !important;
}

.alert {
  margin-top: 1.5rem;
  padding: 1rem;
  border-radius: 4px;
}

.alert-error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* Success Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  padding: 3rem 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 90%;
  text-align: center;
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: white;
  animation: checkmarkPop 0.5s ease-out 0.2s both;
}

@keyframes checkmarkPop {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.modal-content h2 {
  color: var(--color-primary);
  margin-bottom: 1rem;
  font-size: 1.75rem;
}

.modal-message {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.countdown-text {
  color: #999;
  font-size: 0.95rem;
  margin-bottom: 2rem;
}

.countdown {
  color: var(--color-primary);
  font-weight: 700;
  font-size: 1.2rem;
}

.modal-actions {
  display: flex;
  justify-content: center;
}

.modal-actions .btn {
  font-size: 1.1rem;
  padding: 1rem 2.5rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .progress-stepper {
    padding: 0;
  }

  .step-circle {
    width: 35px;
    height: 35px;
    font-size: 1rem;
  }

  .step-label {
    font-size: 0.75rem;
  }

  .claim-form {
    padding: 1.5rem;
  }

  .step-content h2 {
    font-size: 1.4rem;
  }

  .step-description {
    font-size: 1rem;
  }

  .incident-row {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .incident-row .form-group {
    margin-bottom: 0;
  }

  /* Removed invisible class mobile override */

  .contact-schedule-row {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .contact-schedule-row .form-group {
    margin-bottom: 0;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .radio-group {
    flex-direction: column;
    gap: 0.75rem;
  }

  .form-navigation {
    flex-direction: row;
  }

  .btn {
    flex: 1;
    min-width: unset;
  }

  .modal-content {
    padding: 2rem 1.5rem;
  }

  .modal-icon {
    width: 60px;
    height: 60px;
    font-size: 2rem;
  }

  .modal-content h2 {
    font-size: 1.5rem;
  }
}
</style>
