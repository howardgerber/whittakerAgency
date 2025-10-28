<template>
  <div class="container">
    <div class="register-form">
      <h1>Create Your Account</h1>
      <p>Join Whittaker Agency to manage your insurance needs</p>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="full_name" class="form-label">Full Name</label>
          <input
            id="full_name"
            v-model="form.full_name"
            type="text"
            class="form-input"
            required
          />
        </div>

        <div class="form-group">
          <label for="email" class="form-label">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="form-input"
            required
          />
        </div>

        <div class="form-group">
          <label for="phone" class="form-label">Phone (optional)</label>
          <input
            id="phone"
            v-model="form.phone"
            type="tel"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="form-input"
            required
            minlength="8"
          />
        </div>

        <div class="form-group">
          <button type="submit" class="btn btn-primary" :disabled="loading">
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
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { authService } from '@/services/authService'

const router = useRouter()

const form = ref({
  full_name: '',
  email: '',
  phone: '',
  password: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    await authService.register(form.value)
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
}

.register-form h1 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.register-form > p {
  margin-bottom: var(--spacing-lg);
  color: var(--color-gray-medium);
}

.login-link {
  margin-top: var(--spacing-md);
  text-align: center;
}
</style>
