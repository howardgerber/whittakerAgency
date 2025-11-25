<template>
  <div class="container">
    <div class="login-form">
      <h1>Sign In to Your Account</h1>
      <p>Access your insurance dashboard</p>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username" class="form-label">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="form-input"
            required
            placeholder="Enter your username"
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
          />
        </div>

        <div class="form-group">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Signing In...' : 'Login' }}
          </button>
        </div>

        <p v-if="error" class="error-message">{{ error }}</p>

        <p class="register-link">
          Don't have an account? <RouterLink to="/register">Register here</RouterLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { authService } from '@/services/authService'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    const token = await authService.login(form.value)
    authStore.setToken(token.access_token)

    // Get user profile
    const user = await authService.getCurrentUser()
    authStore.setUser(user)

    // Redirect to home
    router.push('/')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Login failed. Please check your credentials.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-form {
  max-width: 500px;
  margin: var(--spacing-xl) auto;
  padding: var(--spacing-lg);
  border: 1px solid var(--color-gray-light);
  border-radius: var(--radius-md);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.login-form h1 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.login-form > p {
  margin-bottom: var(--spacing-lg);
  color: var(--color-gray-medium);
}

.register-link {
  margin-top: var(--spacing-md);
  text-align: center;
}
</style>
