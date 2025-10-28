<template>
  <div class="claims-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <h1>We're Here When You Need Us Most</h1>
        <p class="hero-subtitle">Filing a claim doesn't have to be stressful. Our team is ready to guide you through every step of the process.</p>
        <div class="hero-actions">
          <router-link v-if="isAuthenticated" to="/claims/submit" class="btn btn-secondary btn-large">
            File a Claim
          </router-link>
          <router-link v-else to="/login" class="btn btn-secondary btn-large">
            Login to File a Claim
          </router-link>
          <a href="tel:555-123-4567" class="btn btn-secondary btn-large btn-call-hero">
            <span class="phone-icon">📞</span>
            <div class="call-text">
              <span class="call-label">Call Now</span>
              <span class="phone-number">(555) 123-4567</span>
            </div>
          </a>
        </div>
      </div>
    </section>

    <!-- Claims Process Section -->
    <section class="process-section">
      <div class="container">
        <h2>Our Claims Process</h2>
        <p class="section-subtitle">Five simple steps from report to resolution</p>

        <div class="process-steps">
          <div class="step">
            <div class="step-number">1</div>
            <div class="step-icon">📝</div>
            <h3>Report</h3>
            <p>Submit your claim online or call us. Provide details about the incident and upload any supporting documentation.</p>
          </div>

          <div class="step">
            <div class="step-number">2</div>
            <div class="step-icon">🔍</div>
            <h3>Review</h3>
            <p>Our team reviews your claim within 24 hours and assigns a dedicated adjuster to your case.</p>
          </div>

          <div class="step">
            <div class="step-number">3</div>
            <div class="step-icon">📊</div>
            <h3>Assessment</h3>
            <p>Your adjuster evaluates the damage, reviews documentation, and determines coverage based your policy.</p>
          </div>

          <div class="step">
            <div class="step-number">4</div>
            <div class="step-icon">✅</div>
            <h3>Resolution</h3>
            <p>We approve your claim and communicate the settlement amount and next steps clearly and promptly.</p>
          </div>

          <div class="step">
            <div class="step-number">5</div>
            <div class="step-icon">💰</div>
            <h3>Payment</h3>
            <p>Receive your claim payment quickly via direct deposit or check, so you can move forward.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- What You'll Need Section -->
    <section class="requirements-section">
      <div class="container">
        <h2>What You'll Need</h2>
        <p class="section-subtitle">Have these items ready to speed up your claim</p>

        <div class="requirements-grid">
          <div class="requirement-card">
            <div class="requirement-icon">📝</div>
            <h3>Policy Number</h3>
            <p>Your insurance policy number (found on your policy documents or ID card)</p>
          </div>

          <div class="requirement-card">
            <div class="requirement-icon">📅</div>
            <h3>Incident Details</h3>
            <p>Date, time, and location of the incident with a detailed description of what happened</p>
          </div>

          <div class="requirement-card">
            <div class="requirement-icon">📸</div>
            <h3>Photos</h3>
            <p>Clear photos of damage to property, vehicles, or items (multiple angles if possible)</p>
          </div>

          <div class="requirement-card">
            <div class="requirement-icon">👮</div>
            <h3>Police Report</h3>
            <p>Report number if law enforcement was involved (required for theft, vandalism, or accidents)</p>
          </div>

          <div class="requirement-card">
            <div class="requirement-icon">👥</div>
            <h3>Contact Information</h3>
            <p>Names, phone numbers, and insurance details of any other parties involved</p>
          </div>

          <div class="requirement-card">
            <div class="requirement-icon">💵</div>
            <h3>Receipts & Estimates</h3>
            <p>Repair estimates, receipts, or invoices for emergency repairs or services</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Claim Types Section -->
    <section class="claim-types-section">
      <div class="container">
        <h2>Types of Claims We Handle</h2>

        <div class="claim-types-grid">
          <div class="claim-type-card">
            <div class="type-icon">🚗</div>
            <h3>Auto Claims</h3>
            <p>Accidents, collisions, theft, vandalism, weather damage, and hit-and-run incidents</p>
          </div>

          <div class="claim-type-card">
            <div class="type-icon">🏠</div>
            <h3>Home & Property</h3>
            <p>Fire, water damage, theft, storm damage, liability incidents, and structural issues</p>
          </div>

          <div class="claim-type-card">
            <div class="type-icon">⚡</div>
            <h3>Liability Claims</h3>
            <p>Personal injury, property damage to others, legal defense, and medical payments</p>
          </div>

          <div class="claim-type-card">
            <div class="type-icon">💼</div>
            <h3>Business Claims</h3>
            <p>Property damage, business interruption, liability, equipment breakdown, and cyber incidents</p>
          </div>

          <div class="claim-type-card">
            <div class="type-icon">❤️</div>
            <h3>Life Insurance</h3>
            <p>Death benefits, terminal illness, and beneficiary claims with compassionate support</p>
          </div>

          <div class="claim-type-card">
            <div class="type-icon">🚤</div>
            <h3>Specialty Coverage</h3>
            <p>RV, boat, motorcycle, jewelry, collectibles, pet insurance, and travel claims</p>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<style scoped>
.claims-page {
  min-height: calc(100vh - 200px);
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, var(--color-primary) 0%, #0052CC 100%);
  color: white;
  padding: 5rem 0;
  text-align: center;
}

.hero .container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero-subtitle {
  font-size: 1.3rem;
  margin-bottom: 2.5rem;
  opacity: 0.95;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s;
}

.btn-large {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
}

.btn-primary {
  background: white;
  color: var(--color-primary);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 255, 255, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: white;
  color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.btn-outline {
  background: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

.btn-outline:hover {
  background: var(--color-primary);
  color: white;
}

.phone-icon {
  font-size: 1.2rem;
}

/* Hero Call Button */
.btn-call-hero {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-call-hero .phone-icon {
  font-size: 1.3rem;
}

.btn-call-hero .call-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.15rem;
}

.btn-call-hero .call-label {
  font-size: 0.75rem;
  opacity: 0.9;
  font-weight: 500;
  line-height: 1;
}

.btn-call-hero .phone-number {
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 0.3px;
  line-height: 1;
}

.btn-call-hero:hover {
  background: white !important;
  color: var(--color-primary) !important;
  border-color: white !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.btn-call-hero:hover .phone-icon,
.btn-call-hero:hover .call-label,
.btn-call-hero:hover .phone-number {
  color: var(--color-primary) !important;
}

/* Process Section */
.process-section {
  padding: 5rem 0;
  background: #f5f7fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.process-section h2,
.requirements-section h2,
.claim-types-section h2 {
  text-align: center;
  color: var(--color-primary);
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.section-subtitle {
  text-align: center;
  color: #666;
  font-size: 1.2rem;
  margin-bottom: 3rem;
}

.process-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.step {
  background: white;
  padding: 2rem 1.5rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  position: relative;
  transition: all 0.3s;
}

.step:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 61, 165, 0.15);
}

.step-number {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--color-primary), #0052CC);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
  box-shadow: 0 2px 8px rgba(0, 61, 165, 0.3);
}

.step-icon {
  font-size: 3rem;
  margin: 1rem 0;
}

.step h3 {
  color: var(--color-primary);
  font-size: 1.3rem;
  margin-bottom: 0.75rem;
}

.step p {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Requirements Section */
.requirements-section {
  padding: 5rem 0;
  background: white;
}

.requirements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.requirement-card {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  border-left: 4px solid var(--color-primary);
  transition: all 0.3s;
}

.requirement-card:hover {
  transform: translateX(4px);
  box-shadow: -4px 4px 12px rgba(0, 61, 165, 0.1);
}

.requirement-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.requirement-card h3 {
  color: var(--color-primary);
  font-size: 1.3rem;
  margin-bottom: 0.75rem;
}

.requirement-card p {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Claim Types Section */
.claim-types-section {
  padding: 5rem 0;
  background: #f5f7fa;
}

.claim-types-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.claim-type-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.claim-type-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 61, 165, 0.12);
}

.type-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.claim-type-card h3 {
  color: var(--color-primary);
  font-size: 1.4rem;
  margin-bottom: 0.75rem;
}

.claim-type-card p {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .hero-actions {
    flex-direction: column;
  }

  .process-section h2,
  .requirements-section h2,
  .claim-types-section h2 {
    font-size: 2rem;
  }

  .process-steps {
    grid-template-columns: 1fr;
  }

  .requirements-grid {
    grid-template-columns: 1fr;
  }

  .claim-types-grid {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .process-steps {
    grid-template-columns: repeat(3, 1fr);
  }

  .requirements-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .claim-types-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
