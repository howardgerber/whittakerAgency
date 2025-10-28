<template>
  <div class="contact-page">
    <!-- Visit Our Office Section (only for non-authenticated users) -->
    <section v-if="!isAuthenticated" class="visit-office">
      <div class="container-wide">
        <h1>Contact Us</h1>
        <div class="office-content">
          <div class="office-info">
            <div class="address-box">
              <h3>Whittaker Agency</h3>
              <p class="address">
                12520 SW 68th Ave A<br>
                Tigard, OR 97223
              </p>
              <p class="hours">
                <strong>Hours:</strong><br>
                Monday - Friday: 8:00 AM - 5:00 PM<br>
                Saturday - Sunday: Available by appointment
              </p>
              <p class="contact-info">
                <strong>Phone:</strong> <a href="tel:+15036205999">(503) 620-5999</a><br>
                <strong>Email:</strong> <a href="mailto:info@whittakeragency.com">info@whittakeragency.com</a>
              </p>
            </div>
          </div>
          <div class="office-map">
            <iframe
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2797.5!2d-122.7524!3d45.4227!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x54950c3e3c3c3c3c%3A0x1234567890!2s12520%20SW%2068th%20Ave%20A%2C%20Tigard%2C%20OR%2097223!5e0!3m2!1sen!2sus!4v1234567890"
              width="100%"
              height="400"
              style="border:0;"
              allowfullscreen
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade">
            </iframe>
          </div>
        </div>
      </div>
    </section>

    <!-- Contact Form Section -->
    <div class="container">
      <h1 v-if="isAuthenticated">Contact Us</h1>
      <h2 v-else>Send Us a Message</h2>
      <p class="subtitle">Have a question? Send us a message and we'll get back to you soon.</p>

      <form @submit.prevent="submitMessage" class="contact-form">
        <!-- Full Name -->
        <div class="form-group">
          <label for="full-name">Full Name *</label>
          <input
            id="full-name"
            v-model="formData.full_name"
            type="text"
            class="form-control"
            :class="{ 'invalid': touchedFields.full_name && !isFullNameValid }"
            placeholder="John Smith"
            maxlength="200"
            @blur="touchedFields.full_name = true"
          />
        </div>

        <!-- Email and Phone (side by side on desktop) -->
        <div class="form-row">
          <div class="form-group">
            <label for="email">Email Address *</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              class="form-control"
              :class="{ 'invalid': touchedFields.email && !isEmailValid }"
              placeholder="john@example.com"
              maxlength="254"
              @blur="touchedFields.email = true"
            />
          </div>

          <div class="form-group">
            <label for="phone">Phone Number (optional)</label>
            <input
              id="phone"
              v-model="formData.phone"
              type="tel"
              class="form-control"
              :class="{ 'invalid': touchedFields.phone && !isPhoneValid }"
              placeholder="555.555.5555"
              maxlength="12"
              @input="handlePhoneInput"
              @blur="touchedFields.phone = true"
            />
          </div>
        </div>

        <!-- Subject -->
        <div class="form-group">
          <label for="subject">Subject *</label>
          <select
            id="subject"
            v-model="formData.subject"
            class="form-control"
            :class="{ 'invalid': touchedFields.subject && !formData.subject }"
            @blur="touchedFields.subject = true"
          >
            <option value="">Select a subject</option>
            <option value="general">General Question</option>
            <option value="quote">Quote Question</option>
            <option value="claim">Claim Question</option>
            <option value="policy">Policy Question</option>
            <option value="other">Other</option>
          </select>
        </div>

        <!-- Message -->
        <div class="form-group">
          <label for="message">Message *</label>
          <textarea
            id="message"
            v-model="formData.message"
            class="form-control"
            :class="{ 'invalid': touchedFields.message && !isMessageValid }"
            rows="6"
            maxlength="250"
            placeholder="Tell us how we can help you..."
            @blur="touchedFields.message = true"
          ></textarea>
          <small :class="messageCharClass">{{ formData.message.length }}/250 characters (50 character minimum)</small>
        </div>

        <!-- Submit Button -->
        <div class="form-actions">
          <button type="submit" :disabled="isSubmitting || !isFormValid" class="btn btn-primary">
            {{ isSubmitting ? 'Sending...' : 'Send Message' }}
          </button>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="alert alert-error">
          {{ errorMessage }}
        </div>
      </form>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="modal-overlay" @click="handleModalClick">
      <div class="modal-content" @click.stop>
        <div class="modal-icon">✓</div>
        <h2>Message Sent!</h2>
        <p class="modal-message">Thanks for your message! We'll get back to you soon.</p>
        <p v-if="isAuthenticated" class="countdown-text">Redirecting to dashboard in <span class="countdown">{{ countdown }}</span> seconds...</p>
        <div class="modal-actions">
          <button v-if="isAuthenticated" @click="redirectNow" class="btn btn-primary">Go to Dashboard Now</button>
          <button v-else @click="closeModal" class="btn btn-primary">OK</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import contactService from '@/services/contact'
import { ValidationRules } from '@/utils/validation'
import { formatPhoneNumber } from '@/utils/formatters'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

const formData = ref({
  full_name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
})

const touchedFields = ref({
  full_name: false,
  email: false,
  phone: false,
  subject: false,
  message: false
})

const isSubmitting = ref(false)
const errorMessage = ref('')
const showSuccessModal = ref(false)
const countdown = ref(10)

// Countdown timer
let countdownInterval: number | null = null

// Validation computed properties
const isFullNameValid = computed(() => {
  return ValidationRules.fullName.validate(formData.value.full_name).isValid
})

const isEmailValid = computed(() => {
  return ValidationRules.email.validate(formData.value.email).isValid
})

const isPhoneValid = computed(() => {
  // Phone is optional, so valid if empty OR matches format
  return ValidationRules.phone.validate(formData.value.phone).isValid
})

const isMessageValid = computed(() => {
  const msg = formData.value.message.trim()
  return msg.length >= 50 && msg.length <= 250
})

const isFormValid = computed(() => {
  return isFullNameValid.value &&
         isEmailValid.value &&
         isPhoneValid.value &&
         formData.value.subject !== '' &&
         isMessageValid.value
})

// Character counter styling
const messageCharClass = computed(() => {
  const length = formData.value.message.length
  const max = 250
  const percentage = (length / max) * 100

  if (length >= max) return 'at-limit'
  if (percentage >= 90) return 'near-limit'
  return 'normal'
})

// Phone number auto-formatting
const handlePhoneInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  formData.value.phone = formatPhoneNumber(target.value)
}

// Countdown and modal functions
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
  if (isAuthenticated.value) {
    redirectNow()
  } else {
    closeModal()
  }
}

const closeModal = () => {
  stopCountdown()
  showSuccessModal.value = false
}

const submitMessage = async () => {
  // Mark all fields as touched
  touchedFields.value = {
    full_name: true,
    email: true,
    phone: true,
    subject: true,
    message: true
  }

  // Don't submit if form is invalid
  if (!isFormValid.value) {
    errorMessage.value = 'Please fill out all required fields correctly.'
    return
  }

  isSubmitting.value = true
  errorMessage.value = ''

  try {
    // Submit contact message
    await contactService.submitContactMessage({
      full_name: formData.value.full_name.trim(),
      email: formData.value.email.trim().toLowerCase(),
      phone: formData.value.phone || undefined,
      subject: formData.value.subject,
      message: formData.value.message.trim()
    })

    // Show success modal
    showSuccessModal.value = true

    // Start countdown if authenticated
    if (isAuthenticated.value) {
      startCountdown()
    }

    // Reset form
    formData.value = {
      full_name: '',
      email: '',
      phone: '',
      subject: '',
      message: ''
    }
    touchedFields.value = {
      full_name: false,
      email: false,
      phone: false,
      subject: false,
      message: false
    }

  } catch (error: any) {
    console.error('Error submitting contact message:', error)
    errorMessage.value = error.response?.data?.detail || 'Failed to send message. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.contact-page {
  min-height: calc(100vh - 200px);
  background: #f5f7fa;
}

/* Visit Our Office Section */
.visit-office {
  padding: 3rem 0;
  background: white;
}

.container-wide {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.visit-office h1 {
  color: var(--color-primary);
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-align: center;
}

.office-content {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 2rem;
  align-items: stretch;
}

.office-info {
  display: flex;
  flex-direction: column;
}

.address-box {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 12px;
  border-left: 5px solid var(--color-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.address-box h3 {
  color: var(--color-primary);
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.address-box p {
  margin-bottom: 1rem;
  line-height: 1.7;
  color: #666;
}

.address {
  font-size: 1.1rem;
  font-weight: 500;
  color: #444;
}

.hours,
.contact-info {
  font-size: 1rem;
}

.contact-info {
  margin-bottom: 0;
}

.contact-info a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.3s ease;
}

.contact-info a:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}

.office-map {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  height: 100%;
}

.office-map iframe {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 400px;
}

/* Form Section */
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.container h1 {
  color: var(--color-primary);
  margin-bottom: 0.5rem;
  text-align: center;
  font-size: 2.5rem;
}

.container h2 {
  color: var(--color-primary);
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  color: #666;
  margin-bottom: 2rem;
  text-align: center;
}

.contact-form {
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

select.form-control {
  cursor: pointer;
}

textarea.form-control {
  resize: vertical;
  min-height: 120px;
  font-family: inherit;
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
  text-decoration: none;
  display: inline-block;
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

.btn-secondary {
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

.btn-secondary:hover {
  background: var(--color-primary);
  color: white;
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
  gap: 1rem;
}

.modal-actions .btn {
  font-size: 1.1rem;
  padding: 1rem 2.5rem;
}

@media (max-width: 768px) {
  .container-wide {
    padding: 0 1rem;
  }

  .office-content {
    grid-template-columns: 1fr;
  }

  .visit-office h1 {
    font-size: 2rem;
  }

  .container {
    padding: 2rem 1rem;
  }

  .contact-form {
    padding: 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
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

  .modal-actions {
    justify-content: center;
  }
}
</style>
