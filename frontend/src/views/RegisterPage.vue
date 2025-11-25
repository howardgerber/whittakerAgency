<template>
  <div class="container">
    <div class="register-form">
      <h1>Create Your Account</h1>
      <p>Join Whittaker Agency to manage your insurance needs</p>

      <form @submit.prevent="handleRegister">
        <!-- Username -->
        <div class="form-group">
          <label for="username" class="form-label">Username *</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            :class="['form-input', { 'error': fieldErrors.username.length > 0 && touched.username }]"
            :maxlength="50"
            @blur="handleBlur('username')"
            @input="handleUsernameInput"
            placeholder="Choose a unique username"
          />
          <div v-if="touched.username && fieldErrors.username.length > 0" class="error-messages">
            <p v-for="(error, index) in fieldErrors.username" :key="index" class="error-text">
              {{ error }}
            </p>
          </div>
          <p class="help-text">3-50 characters, lowercase letters, numbers, underscores, and dashes</p>
        </div>

        <!-- Full Name -->
        <div class="form-group">
          <label for="full_name" class="form-label">Full Name *</label>
          <input
            id="full_name"
            v-model="form.full_name"
            type="text"
            :class="['form-input', { 'error': fieldErrors.full_name.length > 0 && touched.full_name }]"
            :maxlength="200"
            @blur="handleBlur('full_name')"
            @input="handleInput('full_name')"
          />
          <div v-if="touched.full_name && fieldErrors.full_name.length > 0" class="error-messages">
            <p v-for="(error, index) in fieldErrors.full_name" :key="index" class="error-text">
              {{ error }}
            </p>
          </div>
        </div>

        <!-- Email -->
        <div class="form-group">
          <label for="email" class="form-label">Email *</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            :class="['form-input', { 'error': fieldErrors.email.length > 0 && touched.email }]"
            :maxlength="254"
            @blur="handleBlur('email')"
            @input="handleInput('email')"
          />
          <div v-if="touched.email && fieldErrors.email.length > 0" class="error-messages">
            <p v-for="(error, index) in fieldErrors.email" :key="index" class="error-text">
              {{ error }}
            </p>
          </div>
        </div>

        <!-- Phone (Optional) -->
        <div class="form-group">
          <label for="phone" class="form-label">Phone (Optional)</label>
          <input
            id="phone"
            ref="phoneInput"
            v-model="form.phone"
            type="tel"
            :class="['form-input', { 'error': fieldErrors.phone.length > 0 && touched.phone }]"
            placeholder="XXX.XXX.XXXX"
            maxlength="12"
            @input="handlePhoneInput"
            @keydown="handlePhoneBackspace"
            @blur="handleBlur('phone')"
          />
          <div v-if="touched.phone && fieldErrors.phone.length > 0" class="error-messages">
            <p v-for="(error, index) in fieldErrors.phone" :key="index" class="error-text">
              {{ error }}
            </p>
          </div>
        </div>

        <!-- Password -->
        <div class="form-group">
          <label for="password" class="form-label">Password *</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            :class="['form-input', { 'error': fieldErrors.password.length > 0 && touched.password }]"
            :maxlength="100"
            @blur="handleBlur('password')"
            @input="handleInput('password')"
          />
          <div v-if="touched.password && fieldErrors.password.length > 0" class="error-messages">
            <p v-for="(error, index) in fieldErrors.password" :key="index" class="error-text">
              {{ error }}
            </p>
          </div>
          <p class="help-text">At least 8 characters with uppercase, lowercase, and number</p>
        </div>

        <!-- Submit Button -->
        <div class="form-group">
          <button
            type="submit"
            :class="['btn', 'btn-primary', { 'disabled': !isFormValid || loading }]"
            :disabled="!isFormValid || loading"
          >
            {{ loading ? 'Creating Account...' : 'Register' }}
          </button>
        </div>

        <p v-if="error" class="error-message">{{ error }}</p>
        <p v-if="success" class="success-message">{{ success }}</p>

        <p class="login-link">
          Already have an account? <RouterLink to="/login">Sign in</RouterLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { authService } from '@/services/authService'
import { validateField } from '@/utils/validation'
import { formatPhoneNumber } from '@/utils/formatters'

const router = useRouter()
const phoneInput = ref<HTMLInputElement | null>(null)

const form = reactive({
  username: '',
  full_name: '',
  email: '',
  phone: '',
  password: ''
})

// Track which fields have been touched (blurred)
const touched = reactive({
  username: false,
  full_name: false,
  email: false,
  phone: false,
  password: false
})

const loading = ref(false)
const error = ref('')
const success = ref('')

// Computed validation errors for each field
const fieldErrors = computed(() => ({
  username: validateField('username', form.username).errors,
  full_name: validateField('fullName', form.full_name).errors,
  email: validateField('email', form.email).errors,
  phone: validateField('phone', form.phone).errors,
  password: validateField('password', form.password).errors
}))

// Check if entire form is valid
const isFormValid = computed(() => {
  // All required fields must be filled and valid
  const usernameValid = validateField('username', form.username).isValid
  const fullNameValid = validateField('fullName', form.full_name).isValid
  const emailValid = validateField('email', form.email).isValid
  const passwordValid = validateField('password', form.password).isValid

  // Phone is optional, but if filled must be valid
  const phoneValid = !form.phone || validateField('phone', form.phone).isValid

  return usernameValid && fullNameValid && emailValid && passwordValid && phoneValid
})

// Handle field blur (mark as touched)
const handleBlur = (fieldName: keyof typeof touched) => {
  touched[fieldName] = true
}

// Handle regular input (validate if already touched)
const handleInput = (fieldName: keyof typeof touched) => {
  // Only validate after field has been touched
  if (touched[fieldName]) {
    // Validation happens automatically via computed property
  }
}

// Handle username input (auto-convert to lowercase)
const handleUsernameInput = () => {
  form.username = form.username.toLowerCase()
  if (touched.username) {
    // Validation happens automatically via computed property
  }
}

// Handle phone input with auto-formatting
const handlePhoneInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const cursorPosition = input.selectionStart || 0
  const oldValue = form.phone
  const newValue = input.value

  // Format the phone number
  const formatted = formatPhoneNumber(newValue, oldValue)
  form.phone = formatted

  // Restore cursor position intelligently
  // If a dot was auto-inserted, move cursor after it
  if (formatted.length > newValue.length && (cursorPosition === 3 || cursorPosition === 7)) {
    setTimeout(() => {
      input.setSelectionRange(cursorPosition + 1, cursorPosition + 1)
    }, 0)
  }
}

// Handle backspace for phone number (smart dot deletion)
const handlePhoneBackspace = (event: KeyboardEvent) => {
  if (event.key !== 'Backspace') return

  const input = phoneInput.value
  if (!input) return

  const cursorPosition = input.selectionStart || 0

  // If cursor is right after a dot, delete both dot and previous digit
  if (cursorPosition === 4 || cursorPosition === 8) {
    event.preventDefault()
    form.phone = form.phone.substring(0, cursorPosition - 2) + form.phone.substring(cursorPosition)

    // Set cursor position
    setTimeout(() => {
      input.setSelectionRange(cursorPosition - 2, cursorPosition - 2)
    }, 0)
  }
}

const handleRegister = async () => {
  // Mark all fields as touched to show errors
  Object.keys(touched).forEach(key => {
    touched[key as keyof typeof touched] = true
  })

  // Don't submit if form is invalid
  if (!isFormValid.value) {
    error.value = 'Please fix the errors above'
    return
  }

  loading.value = true
  error.value = ''
  success.value = ''

  try {
    // Format email before sending
    const registerData = {
      ...form,
      email: form.email.trim().toLowerCase(),
      phone: form.phone || undefined // Don't send empty string
    }

    await authService.register(registerData)
    success.value = 'Account created successfully! Redirecting to login...'

    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-form {
  max-width: 500px;
  margin: var(--spacing-xl) auto;
  padding: var(--spacing-lg);
  border: 1px solid var(--color-gray-light);
  border-radius: var(--radius-md);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: white;
}

.register-form h1 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.register-form > p {
  margin-bottom: var(--spacing-lg);
  color: var(--color-gray-medium);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: all 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.form-input.error {
  border-color: #dc3545;
  background-color: #fff5f5;
}

.error-messages {
  margin-top: 0.5rem;
}

.error-text {
  color: #dc3545;
  font-size: 0.875rem;
  margin: 0.25rem 0;
}

.help-text {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #666;
}

.btn {
  width: 100%;
  padding: 0.75rem;
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

.btn-primary:hover:not(.disabled) {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 61, 165, 0.3);
}

.btn.disabled {
  background: #ccc;
  color: #888;
  cursor: not-allowed;
  opacity: 0.6;
}

.btn.disabled:hover {
  transform: none;
  box-shadow: none;
}

.error-message {
  color: #dc3545;
  background: #fff5f5;
  padding: 0.75rem;
  border-radius: 4px;
  border: 1px solid #dc3545;
  margin-top: 1rem;
}

.success-message {
  color: #28a745;
  background: #f0fff4;
  padding: 0.75rem;
  border-radius: 4px;
  border: 1px solid #28a745;
  margin-top: 1rem;
}

.login-link {
  margin-top: var(--spacing-md);
  text-align: center;
}

.login-link a {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
