<template>
  <div class="about-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <h1>Proudly Serving Oregon Since 2010</h1>
        <p class="subtitle">Your neighbors, committed to protecting Oregon families and businesses</p>
      </div>
    </section>

    <!-- Our Story -->
    <section class="our-story">
      <div class="container">
        <h2>Our Story</h2>
        <div class="story-content">
          <p>
            At Whittaker Agency, we're more than just an insurance provider—we're your neighbors,
            committed to protecting Oregon families and businesses.
          </p>
          <p>
            Founded in Portland, Oregon, Whittaker Agency was built on a simple principle: insurance
            should be personal, transparent, and tailored to the unique needs of our community. With
            deep roots in the Pacific Northwest, we understand the challenges and opportunities that
            come with living in Oregon.
          </p>
        </div>
      </div>
    </section>

    <!-- Mission & Values -->
    <section class="mission-values">
      <div class="container">
        <div class="mission-box">
          <h2>Our Mission</h2>
          <p>
            To provide comprehensive, affordable insurance solutions with exceptional service that makes
            our clients feel valued, protected, and confident about their future.
          </p>
        </div>

        <div class="values-grid">
          <div class="value-card">
            <div class="value-icon">🎯</div>
            <h3>Integrity</h3>
            <p>We do the right thing, even when no one is watching</p>
          </div>

          <div class="value-card">
            <div class="value-icon">🤝</div>
            <h3>Community</h3>
            <p>We invest in and support Oregon communities</p>
          </div>

          <div class="value-card">
            <div class="value-icon">⭐</div>
            <h3>Excellence</h3>
            <p>We strive for the highest standards in everything we do</p>
          </div>

          <div class="value-card">
            <div class="value-icon">💎</div>
            <h3>Transparency</h3>
            <p>Clear communication, no hidden fees or surprises</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Why Choose Us -->
    <section class="why-choose-us">
      <div class="container">
        <h2>Why Choose Whittaker Agency</h2>

        <div class="benefits">
          <div class="benefit">
            <div class="benefit-icon">🌲</div>
            <h3>Local Expertise</h3>
            <p>
              We know Oregon inside and out—from coastal communities to mountain towns, we understand
              the specific risks and requirements of insuring in the Pacific Northwest.
            </p>
          </div>

          <div class="benefit">
            <div class="benefit-icon">🎯</div>
            <h3>Personalized Service</h3>
            <p>
              No two families or businesses are alike. We take the time to understand your unique
              situation and craft coverage that fits your needs and budget.
            </p>
          </div>

          <div class="benefit">
            <div class="benefit-icon">🏆</div>
            <h3>Trusted Advisors</h3>
            <p>
              With years of experience in the insurance industry, our team provides expert guidance
              you can trust.
            </p>
          </div>

          <div class="benefit">
            <div class="benefit-icon">📞</div>
            <h3>Always Available</h3>
            <p>
              When you need us, we're here. 24/7 claims support and responsive customer service.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Oregon Connection -->
    <section class="oregon-connection">
      <div class="container">
        <div class="oregon-content">
          <div class="oregon-text">
            <h2>The Oregon Connection</h2>
            <p>
              Living in Oregon means understanding rain, earthquakes, wildfires, and the unique beauty
              of the Pacific Northwest. Our policies are designed with Oregon in mind:
            </p>

            <ul class="oregon-features">
              <li>
                <span class="feature-icon">🏔️</span>
                <div>
                  <strong>Earthquake Coverage Recommendations</strong>
                  <p>Expert guidance on protecting your property from seismic activity</p>
                </div>
              </li>
              <li>
                <span class="feature-icon">🌊</span>
                <div>
                  <strong>Flood Insurance Expertise</strong>
                  <p>Specialized knowledge of flood zones and coverage requirements</p>
                </div>
              </li>
              <li>
                <span class="feature-icon">🔥</span>
                <div>
                  <strong>Wildfire Protection Strategies</strong>
                  <p>Comprehensive coverage for fire-prone areas</p>
                </div>
              </li>
              <li>
                <span class="feature-icon">📋</span>
                <div>
                  <strong>Oregon Insurance Regulations</strong>
                  <p>Deep understanding of state-specific requirements</p>
                </div>
              </li>
              <li>
                <span class="feature-icon">🏘️</span>
                <div>
                  <strong>Local Claims Adjusters</strong>
                  <p>Adjusters who know the Oregon landscape and communities</p>
                </div>
              </li>
            </ul>

            <p class="oregon-pride">
              We're proud to call Oregon home, and we're committed to protecting the people and places
              that make it special.
            </p>
          </div>

          <div class="oregon-image">
            <img src="/images/oregon-multnomah.jpg" alt="Multnomah Falls Oregon" class="falls-image">
            <p class="image-caption">Multnomah Falls - Oregon's natural beauty</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
      <div class="container">
        <h2>Our Track Record</h2>
        <div class="stats-grid">
          <div class="stat">
            <div class="stat-number">15+</div>
            <div class="stat-label">Years in Business</div>
          </div>

          <div class="stat">
            <div class="stat-number">5,000+</div>
            <div class="stat-label">Families Served</div>
          </div>

          <div class="stat">
            <div class="stat-number">98%</div>
            <div class="stat-label">Client Satisfaction</div>
          </div>

          <div class="stat">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Claims Support</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <h2>Ready to Get Started?</h2>
        <p>Experience the Whittaker Agency difference. Let's protect what matters most to you.</p>
        <div class="cta-buttons">
          <RouterLink v-if="!authStore.isAuthenticated" to="/register" class="btn btn-primary btn-lg">Get a Quote</RouterLink>
          <RouterLink to="/team" class="btn btn-outline btn-lg">Meet Our Team</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>
.about-page {
  width: 100%;
}

/* Hero Section */
.hero {
  background: linear-gradient(rgba(47, 79, 79, 0.3), rgba(26, 77, 46, 0.3)), url('/images/oregon-hero.jpg');
  background-size: cover;
  background-position: center;
  color: white;
  padding: var(--spacing-xl) 0;
  text-align: center;
  min-height: 400px;
  display: flex;
  align-items: center;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: var(--spacing-md);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
}

.subtitle {
  font-size: 1.3rem;
  opacity: 0.95;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
}

/* Our Story */
.our-story {
  padding: var(--spacing-xl) 0;
  background: white;
}

.our-story h2 {
  color: var(--color-primary);
  font-size: 2.2rem;
  margin-bottom: var(--spacing-lg);
  text-align: center;
}

.story-content p {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #666;
  margin-bottom: var(--spacing-md);
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

/* Mission & Values */
.mission-values {
  padding: var(--spacing-xl) 0;
  background: #f8f9fa;
}

.mission-box {
  text-align: center;
  max-width: 800px;
  margin: 0 auto var(--spacing-xl);
  padding: var(--spacing-xl);
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.mission-box h2 {
  color: var(--color-primary);
  font-size: 2rem;
  margin-bottom: var(--spacing-md);
}

.mission-box p {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #666;
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
}

.value-card {
  background: white;
  padding: var(--spacing-lg);
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.value-card:hover {
  transform: translateY(-5px);
}

.value-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
}

.value-card h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
  font-size: 1.3rem;
}

.value-card p {
  color: #666;
  line-height: 1.6;
}

/* Why Choose Us */
.why-choose-us {
  padding: var(--spacing-xl) 0;
}

.why-choose-us h2 {
  color: var(--color-primary);
  font-size: 2.2rem;
  margin-bottom: var(--spacing-xl);
  text-align: center;
}

.benefits {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-xl);
}

.benefit {
  display: flex;
  gap: var(--spacing-md);
}

.benefit-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.benefit h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
  font-size: 1.3rem;
}

.benefit p {
  color: #666;
  line-height: 1.7;
}

/* Oregon Connection */
.oregon-connection {
  padding: var(--spacing-xl) 0;
  background: #f8f9fa;
}

.oregon-content {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: var(--spacing-xl);
  align-items: start;
}

.oregon-text h2 {
  color: var(--color-primary);
  font-size: 2rem;
  margin-bottom: var(--spacing-md);
}

.oregon-text > p {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #666;
  margin-bottom: var(--spacing-lg);
}

.oregon-features {
  list-style: none;
  padding: 0;
  margin-bottom: var(--spacing-lg);
}

.oregon-features li {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  align-items: start;
}

.feature-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.oregon-features strong {
  color: var(--color-primary);
  display: block;
  margin-bottom: 0.25rem;
  font-size: 1.1rem;
}

.oregon-features p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.oregon-pride {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--color-primary);
  line-height: 1.7;
}

.oregon-image {
  position: sticky;
  top: 100px;
}

.falls-image {
  width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  margin-bottom: var(--spacing-sm);
}

.image-caption {
  text-align: center;
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}

/* Stats Section */
.stats-section {
  padding: var(--spacing-xl) 0;
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  color: white;
  text-align: center;
}

.stats-section h2 {
  color: white;
  font-size: 2rem;
  margin-bottom: var(--spacing-xl);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-xl);
  max-width: 1000px;
  margin: 0 auto;
}

.stat {
  padding: var(--spacing-lg);
}

.stat-number {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: var(--spacing-sm);
}

.stat-label {
  font-size: 1.1rem;
  opacity: 0.95;
}

/* CTA Section */
.cta-section {
  padding: var(--spacing-xl) 0;
  text-align: center;
  background: white;
}

.cta-section h2 {
  color: var(--color-primary);
  font-size: 2rem;
  margin-bottom: var(--spacing-md);
}

.cta-section p {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: var(--spacing-lg);
}

.cta-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

/* Buttons */
.btn {
  display: inline-block;
  padding: 0.75rem 2rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background: #1a4d2e;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-outline {
  background: transparent;
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.btn-outline:hover {
  background: var(--color-primary);
  color: white;
}

.btn-lg {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 1.8rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .our-story h2,
  .why-choose-us h2,
  .oregon-text h2 {
    font-size: 1.8rem;
  }

  .oregon-content {
    grid-template-columns: 1fr;
  }

  .oregon-image {
    position: static;
  }

  .benefits {
    grid-template-columns: 1fr;
  }

  .stat-number {
    font-size: 2.5rem;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }

  .btn-lg {
    width: 100%;
    max-width: 300px;
  }
}
</style>
