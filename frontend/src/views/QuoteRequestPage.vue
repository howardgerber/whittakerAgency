<template>
  <div class="quote-request-page">
    <div class="container">
      <h1>Request an Insurance Quote</h1>
      <p class="subtitle">Tell us about your insurance needs and we'll get back to you with a personalized quote.</p>

      <form @submit.prevent="submitQuote" class="quote-form">
        <!-- Insurance Category Selector -->
        <div class="form-row">
          <div class="form-group">
            <label for="insurance-category">Insurance Category *</label>
            <select
              id="insurance-category"
              v-model="selectedCategory"
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

          <!-- Subtype Selector (only show if category has subcategories) -->
          <div v-if="hasSubcategories" class="form-group">
            <label for="insurance-subtype">Type *</label>
            <select
              id="insurance-subtype"
              v-model="selectedSubtype"
              required
              class="form-control"
            >
              <option value="">Select Type</option>
              <option v-for="subtype in subtypeOptions" :key="subtype.value" :value="subtype.value">
                {{ subtype.label }}
              </option>
            </select>
          </div>
        </div>

        <!-- Dynamic Form Component -->
        <div v-if="canShowForm" class="insurance-fields">
          <component
            :is="currentFormComponent"
            :key="selectedType"
            :selectedSubtype="selectedSubtype"
            :errors="validationErrors"
            @update="handleFormUpdate"
            @valid="handleValidationUpdate"
            @blur="handleFieldBlur"
          />
        </div>

        <!-- Customer Notes -->
        <div v-if="canShowForm" class="form-group">
          <label for="customer-notes">Additional Notes or Questions</label>
          <textarea
            id="customer-notes"
            v-model="customerNotes"
            rows="4"
            maxlength="1000"
            class="form-control"
            placeholder="Tell us anything else we should know about your insurance needs..."
          ></textarea>
          <small :class="notesCharClass">{{ customerNotes.length }}/1000 characters</small>
        </div>

        <!-- Submit Button -->
        <div v-if="canShowForm" class="form-actions">
          <button type="submit" :disabled="isSubmitting || !isFormValid" class="btn btn-primary">
            {{ isSubmitting ? 'Submitting...' : 'Submit Quote Request' }}
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
        <h2>Quote Request Submitted!</h2>
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
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import quoteService from '@/services/quotes'
import { cleanText } from '@/utils/formatters'

// Import all quote form components
import AutoQuoteForm from '@/components/quote-forms/AutoQuoteForm.vue'
import HomeQuoteForm from '@/components/quote-forms/HomeQuoteForm.vue'
import LifeQuoteForm from '@/components/quote-forms/LifeQuoteForm.vue'
import BusinessQuoteForm from '@/components/quote-forms/BusinessQuoteForm.vue'
import MotorcycleQuoteForm from '@/components/quote-forms/MotorcycleQuoteForm.vue'
import RVQuoteForm from '@/components/quote-forms/RVQuoteForm.vue'
import BoatQuoteForm from '@/components/quote-forms/BoatQuoteForm.vue'
import UmbrellaQuoteForm from '@/components/quote-forms/UmbrellaQuoteForm.vue'
import CollectiblesQuoteForm from '@/components/quote-forms/CollectiblesQuoteForm.vue'
import IndividualHealthQuoteForm from '@/components/quote-forms/IndividualHealthQuoteForm.vue'
import PetQuoteForm from '@/components/quote-forms/PetQuoteForm.vue'
import JewelryQuoteForm from '@/components/quote-forms/JewelryQuoteForm.vue'
import EventQuoteForm from '@/components/quote-forms/EventQuoteForm.vue'
import TravelQuoteForm from '@/components/quote-forms/TravelQuoteForm.vue'
import ATVQuoteForm from '@/components/quote-forms/ATVQuoteForm.vue'
import SnowmobileQuoteForm from '@/components/quote-forms/SnowmobileQuoteForm.vue'
import RoadsideQuoteForm from '@/components/quote-forms/RoadsideQuoteForm.vue'
import VehicleProtectionQuoteForm from '@/components/quote-forms/VehicleProtectionQuoteForm.vue'
import IdentityProtectionQuoteForm from '@/components/quote-forms/IdentityProtectionQuoteForm.vue'

const router = useRouter()

const selectedCategory = ref('')
const selectedSubtype = ref('')
const customerNotes = ref('')
const isSubmitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const showSuccessModal = ref(false)
const countdown = ref(10)

// Store form data from child component
const formData = ref<any>({})

// Track if form is valid (has all required fields)
const isFormValid = ref(false)

// Validation errors (can be populated if we add validation)
const validationErrors = ref<Record<string, string>>({})

// Countdown timer
let countdownInterval: number | null = null

// Categories that have subcategories (per CATEGORIES.md)
const categoriesWithSubcategories = ['vehicle', 'property', 'other']

// Check if current category has subcategories
const hasSubcategories = computed(() => {
  return categoriesWithSubcategories.includes(selectedCategory.value)
})

// Subtype options based on selected category
const subtypeOptions = computed(() => {
  const options: Record<string, Array<{ value: string; label: string }>> = {
    vehicle: [
      { value: 'auto', label: 'Auto' },
      { value: 'motorcycle', label: 'Motorcycle' },
      { value: 'atv', label: 'ATV/Off-Road' },
      { value: 'roadside', label: 'Roadside Assistance' },
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
  return options[selectedCategory.value] || []
})

// Combined insurance type (category or category_subtype)
const selectedType = computed(() => {
  // Categories without subcategories
  if (!hasSubcategories.value && selectedCategory.value) {
    return selectedCategory.value
  }

  // Categories with subcategories
  if (selectedCategory.value && selectedSubtype.value) {
    return `${selectedCategory.value}_${selectedSubtype.value}`
  }

  return ''
})

// Can show form if:
// - Category without subcategories is selected, OR
// - Category with subcategories AND subcategory is selected
const canShowForm = computed(() => {
  if (!selectedCategory.value) return false

  if (!hasSubcategories.value) {
    return true // No subcategory needed
  }

  return !!selectedSubtype.value // Subcategory is required
})

// Map insurance types to components
const formComponentMap: Record<string, any> = {
  // Vehicle forms
  vehicle_auto: AutoQuoteForm,
  vehicle_motorcycle: MotorcycleQuoteForm,
  vehicle_atv: ATVQuoteForm,
  vehicle_roadside: RoadsideQuoteForm,
  vehicle_snowmobile: SnowmobileQuoteForm,
  vehicle_boat: BoatQuoteForm,
  vehicle_rv: RVQuoteForm,
  vehicle_vehicle_protection: VehicleProtectionQuoteForm,

  // Property forms
  property_homeowners: HomeQuoteForm,
  property_renters: HomeQuoteForm,
  property_condo: HomeQuoteForm,
  property_landlord: HomeQuoteForm,
  property_mobile_home: HomeQuoteForm,

  // Categories without subcategories
  life: LifeQuoteForm,
  business: BusinessQuoteForm,
  identity_protection: IdentityProtectionQuoteForm,

  // Other services forms
  other_umbrella: UmbrellaQuoteForm,
  other_collectibles: CollectiblesQuoteForm,
  other_individual_health: IndividualHealthQuoteForm,
  other_pet: PetQuoteForm,
  other_jewelry: JewelryQuoteForm,
  other_event: EventQuoteForm,
  other_travel: TravelQuoteForm
}

// Get current form component based on selected type
const currentFormComponent = computed(() => {
  return selectedType.value ? formComponentMap[selectedType.value] : null
})

// Character count styling for notes
const notesCharClass = computed(() => {
  const length = customerNotes.value.length
  const max = 1000
  const percentage = (length / max) * 100

  if (length >= max) return 'at-limit'
  if (percentage >= 90) return 'near-limit'
  return 'normal'
})

// Reset subtype when category changes
watch(selectedCategory, () => {
  selectedSubtype.value = ''
  formData.value = {}
  isFormValid.value = false
  validationErrors.value = {}
  customerNotes.value = ''
  successMessage.value = ''
  errorMessage.value = ''
})

// Reset form data when subtype changes
watch(selectedSubtype, () => {
  formData.value = {}
  isFormValid.value = false
  validationErrors.value = {}
  customerNotes.value = ''
  successMessage.value = ''
  errorMessage.value = ''
})

// Handle form data updates from child components
const handleFormUpdate = (data: any) => {
  formData.value = data
}

// Handle validation state updates from child components
const handleValidationUpdate = (isValid: boolean) => {
  isFormValid.value = isValid
}

// Handle field blur events from child components
const handleFieldBlur = (_fieldName: string) => {
  // Can add validation logic here if needed
}

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
  // Allow clicking outside modal to close and redirect
  redirectNow()
}

const submitQuote = async () => {
  isSubmitting.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    await quoteService.createQuote({
      category: selectedCategory.value,
      subcategory: selectedSubtype.value || null,
      quote_data: formData.value,
      customer_notes: customerNotes.value ? cleanText(customerNotes.value) : undefined
    })

    successMessage.value = `Your quote request has been received and our team will review it shortly.`
    showSuccessModal.value = true
    startCountdown()

  } catch (error: any) {
    console.error('Error submitting quote:', error)
    errorMessage.value = error.response?.data?.detail || 'Failed to submit quote request. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.quote-request-page {
  min-height: calc(100vh - 200px);
  padding: 3rem 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 2rem;
}

h1 {
  color: var(--color-primary);
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  margin-bottom: 2rem;
}

.quote-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
  border-color: var(--color-primary);
}

select.form-control {
  cursor: pointer;
}

textarea.form-control {
  resize: vertical;
  min-height: 100px;
}

small {
  color: #666;
  font-size: 0.875rem;
  display: block;
  margin-top: 0.25rem;
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

.insurance-fields {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.form-actions {
  margin-top: 2rem;
  text-align: center;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
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

.btn:disabled {
  background: #cccccc !important;
  color: #666666 !important;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

.alert {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 4px;
}

.alert-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
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

  .quote-form {
    padding: 1.5rem;
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
