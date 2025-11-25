<template>
  <div class="identity-protection-quote-form">
    <h3>Identity Theft Protection Details</h3>

    <div class="form-group">
      <label for="identity-plan">Protection Plan *</label>
      <select id="identity-plan" v-model="formData.plan_type" required class="form-control">
        <option value="">Select Plan Type</option>
        <option value="individual">Individual</option>
        <option value="couple">Couple</option>
        <option value="family">Family (up to 4 children)</option>
      </select>
    </div>

    <div class="form-group">
      <label>Services Desired *</label>
      <div class="checkbox-group">
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.services.credit_monitoring" />
          Credit Monitoring (3 Bureaus)
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.services.dark_web" />
          Dark Web Monitoring
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.services.identity_restoration" />
          Identity Restoration Services
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.services.fraud_resolution" />
          Fraud Resolution Support
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.services.lost_wallet" />
          Lost Wallet Protection
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="formData.services.social_media" />
          Social Media Monitoring
        </label>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="identity-coverage">Desired Coverage Amount</label>
        <select id="identity-coverage" v-model="formData.coverage_amount" class="form-control">
          <option value="">Select Amount</option>
          <option value="25000">$25,000</option>
          <option value="50000">$50,000</option>
          <option value="100000">$100,000</option>
          <option value="1000000">$1,000,000</option>
        </select>
      </div>

      <div class="form-group">
        <label for="identity-current-provider">Current Provider</label>
        <input
          type="text"
          id="identity-current-provider"
          v-model="formData.current_provider"
          class="form-control"
          placeholder="e.g., LifeLock, IdentityGuard"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue'

interface IdentityProtectionFormData {
  plan_type: string
  services: {
    credit_monitoring: boolean
    dark_web: boolean
    identity_restoration: boolean
    fraud_resolution: boolean
    lost_wallet: boolean
    social_media: boolean
  }
  coverage_amount: string
  current_provider: string
}

const emit = defineEmits<{
  (e: 'update', data: IdentityProtectionFormData): void
  (e: 'valid', isValid: boolean): void
}>()

const formData = reactive<IdentityProtectionFormData>({
  plan_type: '',
  services: {
    credit_monitoring: false,
    dark_web: false,
    identity_restoration: false,
    fraud_resolution: false,
    lost_wallet: false,
    social_media: false
  },
  coverage_amount: '',
  current_provider: ''
})

// Computed property to check if all required fields are filled
const isFormValid = computed(() => {
  return (
    formData.plan_type !== '' &&
    Object.values(formData.services).some(v => v === true)
  )
})

watch(formData, (newData) => {
  emit('update', { ...newData })
}, { deep: true })

// Watch validation state and emit to parent
watch(isFormValid, (isValid) => {
  emit('valid', isValid)
}, { immediate: true })
</script>

<style scoped>
@import './form-styles.css';
</style>
