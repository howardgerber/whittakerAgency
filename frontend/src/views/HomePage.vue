<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container hero-container">
        <div class="hero-content">
          <h1>Welcome to Whittaker Agency</h1>
          <p class="tagline">Your Family, Your Business, Our Priority</p>
          <p class="subtitle">Serving Families and Businesses Across Oregon</p>

          <div v-if="!authStore.isAuthenticated" class="cta">
            <RouterLink to="/register" class="btn btn-primary">Get Started</RouterLink>
            <RouterLink to="/contact" class="btn btn-secondary">Contact Us</RouterLink>
          </div>
          <div v-else class="cta">
            <p class="welcome-message">Welcome back, {{ authStore.user?.full_name }}!</p>
          </div>
        </div>

        <!-- Thought Bubble for Claims -->
        <RouterLink v-if="isBubbleVisible" to="/claims" class="thought-bubble">
          <button @click.prevent="dismissBubble" class="dismiss-btn" aria-label="Dismiss" title="Dismiss">×</button>
          <div class="bubble-text">
            <span class="bubble-content">⚠️ Need to file a claim?</span>
            <span class="bubble-link">Learn what to do →</span>
          </div>
        </RouterLink>
      </div>
    </section>

    <!-- About + Services Combo Section -->
    <section class="about-services-combo">
      <div class="container">
        <div class="about-text">
          <h2>Oregon's Trusted Insurance Partner Since 1998</h2>
          <p>
            Family-owned and operated, Whittaker Agency serves families and businesses across Oregon
            with personalized insurance solutions. We're not a call center - we're your neighbors,
            committed to protecting what matters most to you.
          </p>
        </div>

        <div class="services-and-advantages">
          <div class="services-simple">
            <h3>Coverage Options</h3>
            <ul class="coverage-list">
              <li><span class="icon">🚗</span> Vehicle</li>
              <li><span class="icon">🏠</span> Property</li>
              <li><span class="icon">❤️</span> Life</li>
              <li><span class="icon">💼</span> Business</li>
              <li><span class="icon">🔒</span> Identity Protection</li>
              <li><span class="icon">☂️</span> Other Services</li>
            </ul>
            <RouterLink to="/services" class="details-link">
              View all services →
            </RouterLink>
          </div>

          <div class="advantage-card">
            <div class="icon-image">
              <img src="/images/icons/Oregon.png" alt="Oregon" class="oregon-icon">
            </div>
            <h3>Proudly Serving Oregon</h3>
            <p>Born and raised in the Pacific Northwest, we understand the unique needs of Oregon families and businesses. From the coast to the mountains, we're here to protect what matters most to you.</p>
            <p>Our deep roots in Oregon mean we're not just your insurance agency—we're your neighbors, committed to the communities we serve.</p>
          </div>

          <div class="advantage-card">
            <div class="icon-large">🤝</div>
            <h3>Personalized Touch with Trusted Advisors</h3>
            <p>Real people, real relationships, real service - not automated systems or call centers.</p>
            <p>With years of experience in the insurance industry, our team provides expert guidance you can trust.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Serving Oregon Communities Section -->
    <section class="serving-oregon">
      <div class="container">
        <h2>Serving Oregon Communities</h2>
        <div class="two-column">
          <div class="communities-text">
            <p>
              From the coast to the Cascades, from Portland to Medford, Whittaker Agency is proud
              to serve communities throughout Oregon. We're licensed statewide and ready to help
              wherever you call home.
            </p>
            <div class="areas">
              <strong>Service Areas Include:</strong><br>
              Portland Metro • Salem • Eugene • Bend • Medford • Corvallis • Ashland •
              Crater Lake • Hood River • Pendleton • and all surrounding communities
            </div>
          </div>
          <div class="oregon-pride">
            <div class="pride-box">
              <p class="big-stat">25+</p>
              <p class="stat-label">Years Serving Oregon</p>
            </div>
            <div class="pride-box">
              <p class="big-stat">5,000+</p>
              <p class="stat-label">Happy Customers</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Get Started / Already Protected Section -->
    <section class="dual-cta-section">
      <div class="container">
        <div class="dual-cta-grid">
          <!-- Ready to Get Protected -->
          <div class="cta-card cta-primary">
            <div class="card-icon">🛡️</div>
            <h2>Ready to Get Protected?</h2>
            <p class="card-description">Get a free quote in just 3 minutes and discover how affordable comprehensive coverage can be.</p>

            <div class="cta-actions">
              <RouterLink v-if="authStore.isAuthenticated" to="/quote" class="btn btn-primary btn-lg">Get a Quote</RouterLink>
              <RouterLink v-else to="/register" class="btn btn-primary btn-lg">Get a Quote</RouterLink>
              <RouterLink to="/services" class="btn-link">Browse Services →</RouterLink>
            </div>
          </div>

          <!-- Already Protected -->
          <div class="cta-card cta-secondary">
            <div class="card-icon warning">⚠️</div>
            <h2>Already Protected?</h2>
            <p class="card-description">Need to file a claim? Learn what information you'll need and how the process works.</p>

            <div class="cta-actions">
              <RouterLink to="/claims" class="btn btn-outline-primary btn-lg">Learn About Claims</RouterLink>
              <a href="tel:+15036205999" class="btn-link">Contact Us: (503) 620-5999</a>
            </div>
          </div>
        </div>

        <p class="guarantee">
          ✓ No obligation  ✓ Free consultation  ✓ Fast, friendly service
        </p>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isBubbleVisible = ref(true)

interface BubbleState {
  dismissCount: number
  lastDismissed: number | null
}

const THIRTY_DAYS_MS = 30 * 24 * 60 * 60 * 1000 // 30 days in milliseconds
const MAX_DISMISSALS = 6 // After 6 dismissals, hide permanently

onMounted(() => {
  const stateStr = localStorage.getItem('claims-bubble-state')

  if (!stateStr) {
    // First time - show the bubble
    isBubbleVisible.value = true
    return
  }

  try {
    const state: BubbleState = JSON.parse(stateStr)

    // If dismissed 6 or more times, hide permanently
    if (state.dismissCount >= MAX_DISMISSALS) {
      isBubbleVisible.value = false
      return
    }

    // If never dismissed or no lastDismissed timestamp, show it
    if (!state.lastDismissed) {
      isBubbleVisible.value = true
      return
    }

    // Check if 30 days have passed since last dismissal
    const now = Date.now()
    const daysSinceLastDismiss = now - state.lastDismissed

    if (daysSinceLastDismiss >= THIRTY_DAYS_MS) {
      // 30 days have passed - show the bubble again
      isBubbleVisible.value = true
    } else {
      // Still within 30-day hiding period
      isBubbleVisible.value = false
    }
  } catch (error) {
    // If parsing fails, reset and show the bubble
    console.error('Error parsing bubble state:', error)
    isBubbleVisible.value = true
  }
})

const dismissBubble = () => {
  const stateStr = localStorage.getItem('claims-bubble-state')
  let state: BubbleState = { dismissCount: 0, lastDismissed: null }

  if (stateStr) {
    try {
      state = JSON.parse(stateStr)
    } catch (error) {
      console.error('Error parsing bubble state:', error)
    }
  }

  // Increment dismiss count and update timestamp
  state.dismissCount += 1
  state.lastDismissed = Date.now()

  localStorage.setItem('claims-bubble-state', JSON.stringify(state))
  isBubbleVisible.value = false
}
</script>

<style scoped>
.home-page {
  width: 100%;
}

/* Hero Section */
.hero {
  background: linear-gradient(rgba(47, 79, 79, 0.2), rgba(26, 77, 46, 0.2)), url('/images/oregon-hero.jpg');
  background-size: 100% auto;
  background-position: top center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  color: white;
  padding: var(--spacing-xl) 0;
  text-align: center;
  min-height: 500px;
  display: flex;
  align-items: center;
}

.hero-container {
  position: relative;
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
}

.tagline {
  font-size: 1.5rem;
  margin-bottom: var(--spacing-sm);
  font-weight: 300;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: var(--spacing-lg);
  opacity: 0.95;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
}

.cta {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.welcome-message {
  font-size: 1.2rem;
  font-weight: 500;
}

/* Thought Bubble - Soft Rounded Shape */
.thought-bubble {
  position: fixed;
  top: 150px;
  right: 60px;
  background: white;
  border-radius: 38px;
  padding: 0.85rem 1.35rem;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
  max-width: 220px;
  text-decoration: none;
  color: #333;
  transition: all 0.3s ease;
  z-index: 100;
  border: 3px solid #ffc107;
}

.thought-bubble:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
  border-color: #f39c12;
}

.bubble-text {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  text-align: center;
}

.bubble-content {
  color: #333;
  font-size: 0.85rem;
  font-weight: 600;
  line-height: 1.3;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
}

.bubble-link {
  color: var(--color-primary);
  font-weight: 600;
  font-size: 0.75rem;
  transition: color 0.2s ease;
}

.thought-bubble:hover .bubble-link {
  color: #1a4d2e;
}

/* Dismiss Button */
.dismiss-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  background: white;
  border: 2px solid #ffc107;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.2rem;
  line-height: 1;
  color: #666;
  padding: 0;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.dismiss-btn:hover {
  background: #f39c12;
  color: white;
  border-color: #f39c12;
  transform: scale(1.1);
}

/* About + Services Combo Section */
.about-services-combo {
  padding: var(--spacing-lg) 0;
  background: white;
}

.about-text {
  max-width: 900px;
  margin: 0 auto var(--spacing-lg);
  text-align: center;
}

.about-text h2 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
  font-size: 1.8rem;
}

.about-text p {
  font-size: 1.05rem;
  line-height: 1.6;
  color: #666;
}

.services-and-advantages {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--spacing-lg);
  align-items: stretch;
}

.services-simple {
  text-align: center;
  padding: var(--spacing-lg);
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.services-simple h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
  font-size: 1.1rem;
}

.coverage-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
  text-align: left;
}

.coverage-list li {
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.coverage-list .icon {
  font-size: 1.3rem;
}

.details-link {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.details-link:hover {
  color: var(--color-dark-blue);
  text-decoration: underline;
}

.advantage-card {
  background: #f8f9fa;
  padding: var(--spacing-lg);
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #e0e0e0;
}

.advantage-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.icon-large {
  font-size: 2.5rem;
  margin-bottom: var(--spacing-sm);
}

.icon-image {
  margin-bottom: var(--spacing-sm);
  display: flex;
  justify-content: center;
  align-items: center;
}

.oregon-icon {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

.advantage-card h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
  font-size: 1.1rem;
}

.advantage-card p {
  color: #666;
  line-height: 1.5;
  font-size: 0.95rem;
}

.advantage-card p + p {
  margin-top: var(--spacing-sm);
}

/* Team Preview Section */
.team-preview {
  padding: var(--spacing-xl) 0;
  background-color: #f8f9fa;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-lg);
  margin-top: var(--spacing-lg);
}

.team-card {
  background: white;
  padding: var(--spacing-lg);
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.team-photo {
  margin-bottom: var(--spacing-md);
}

.photo-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  margin: 0 auto;
}

.team-card h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-xs);
}

.team-role {
  color: #666;
  font-weight: 500;
  margin-bottom: var(--spacing-sm);
}

.team-bio {
  color: #666;
  line-height: 1.6;
  font-size: 0.95rem;
}

/* Oregon Connection Section */
.oregon-connection {
  padding: var(--spacing-xl) 0;
}

.oregon-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-xl);
  align-items: center;
}

.oregon-text h2 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
}

.oregon-text p {
  color: #666;
  line-height: 1.8;
  margin-bottom: var(--spacing-md);
}

.falls-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Serving Oregon Communities Section */
.serving-oregon {
  padding: var(--spacing-xl) 0;
  background: #f8f9fa;
}

.serving-oregon h2 {
  color: var(--color-primary);
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.two-column {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-xl);
  align-items: center;
  margin-top: var(--spacing-lg);
}

.communities-text p {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #666;
  margin-bottom: var(--spacing-lg);
}

.areas {
  background: white;
  padding: var(--spacing-lg);
  border-radius: 8px;
  border-left: 4px solid var(--color-primary);
  line-height: 1.8;
  color: #666;
}

.areas strong {
  color: var(--color-primary);
}

.oregon-pride {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.pride-box {
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  color: white;
  padding: var(--spacing-xl);
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.big-stat {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.stat-label {
  font-size: 1.1rem;
  margin: 0;
  opacity: 0.95;
}

/* Dual CTA Section */
.dual-cta-section {
  padding: var(--spacing-xl) 0;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}

.dual-cta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.cta-card {
  background: white;
  padding: var(--spacing-xl);
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  text-align: center;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  border-top: 4px solid transparent;
}

.cta-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.cta-primary {
  border-top-color: var(--color-primary);
}

.cta-secondary {
  border-top-color: #ffc107;
}

.cta-card .card-icon {
  font-size: 3.5rem;
  margin-bottom: var(--spacing-md);
}

.cta-card .card-icon.warning {
  filter: drop-shadow(0 2px 4px rgba(255, 193, 7, 0.3));
}

.cta-card h2 {
  color: var(--color-primary);
  font-size: 1.8rem;
  margin-bottom: var(--spacing-sm);
}

.card-description {
  color: #666;
  font-size: 1.05rem;
  line-height: 1.6;
  margin-bottom: var(--spacing-lg);
  flex: 1;
}

.cta-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  align-items: center;
}

.btn-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.btn-link:hover {
  color: #1a4d2e;
  background: rgba(47, 79, 79, 0.05);
  text-decoration: none;
}

.guarantee {
  text-align: center;
  font-size: 1rem;
  color: #666;
  margin-top: var(--spacing-lg);
}

.btn-outline-primary {
  background: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

.btn-outline-primary:hover {
  background: var(--color-primary);
  color: white;
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  width: 100%;
  max-width: 280px;
}

/* Hero CTA Buttons */
.cta .btn-primary,
.cta .btn-secondary {
  padding: 1rem 2.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  display: inline-block;
  transition: all 0.3s;
}

.cta .btn-primary {
  background: var(--color-primary);
  color: white;
}

.cta .btn-primary:hover {
  background: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.cta .btn-secondary {
  background: white;
  color: var(--color-primary);
  border: 2px solid white;
}

.cta .btn-secondary:hover {
  background: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}


/* Footer */
.footer {
  background-color: #2c3e50;
  color: white;
  padding: var(--spacing-xl) 0 var(--spacing-md);
  margin-top: var(--spacing-xl);
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.footer-section h3,
.footer-section h4 {
  color: white;
  margin-bottom: var(--spacing-md);
}

.footer-section p {
  color: #ecf0f1;
  margin-bottom: var(--spacing-sm);
  line-height: 1.6;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: var(--spacing-sm);
}

.footer-section a {
  color: #ecf0f1;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-section a:hover {
  color: var(--color-primary);
}

.section-cta {
  text-align: center;
  margin-top: var(--spacing-xl);
}

.footer-bottom {
  border-top: 1px solid #34495e;
  padding-top: var(--spacing-md);
  text-align: center;
  color: #95a5a6;
}

/* Responsive Design */
@media (max-width: 768px) {
  /* Hide thought bubble on mobile to avoid clutter */
  .thought-bubble {
    display: none;
  }

  .hero h1 {
    font-size: 2rem;
  }

  .tagline {
    font-size: 1.2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .services-and-advantages {
    grid-template-columns: 1fr;
  }

  .oregon-content {
    grid-template-columns: 1fr;
  }

  .two-column {
    grid-template-columns: 1fr;
  }

  .dual-cta-grid {
    grid-template-columns: 1fr;
  }

  .cta-secondary {
    order: -1;
  }

  .office-content {
    grid-template-columns: 1fr;
  }

  .office-map iframe {
    height: 300px;
  }

  .team-grid {
    grid-template-columns: 1fr;
  }

  .cta-card h2 {
    font-size: 1.5rem;
  }
}
</style>
