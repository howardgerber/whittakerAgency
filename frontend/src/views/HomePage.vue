<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <h1>Welcome to Whittaker Agency</h1>
        <p class="tagline">Your Family, Your Business, Our Priority</p>
        <p class="subtitle">Serving Families and Businesses Across Oregon</p>

        <div v-if="!authStore.isAuthenticated" class="cta">
          <RouterLink to="/register" class="btn btn-primary">Get Started</RouterLink>
          <RouterLink to="/services" class="btn btn-secondary">View Services</RouterLink>
        </div>
        <div v-else class="cta">
          <p class="welcome-message">Welcome back, {{ authStore.user?.full_name }}!</p>
          <RouterLink to="/services" class="btn btn-secondary">View Services</RouterLink>
        </div>
      </div>
    </section>

    <!-- Services Overview Section -->
    <section class="services">
      <div class="container">
        <h2>Our Insurance Services</h2>
        <p class="section-description">Comprehensive coverage for every stage of life</p>

        <div class="services-grid">
          <RouterLink
            v-for="service in services"
            :key="service.name"
            :to="`/services#${service.id}`"
            class="service-card"
          >
            <div class="service-icon">{{ service.icon }}</div>
            <h3>{{ service.name }}</h3>
            <p>{{ service.description }}</p>
          </RouterLink>
        </div>

        <div class="section-cta">
          <RouterLink to="/services" class="btn btn-primary">View All Services</RouterLink>
        </div>
      </div>
    </section>

    <!-- Why Choose Us Section -->
    <section class="why-choose-us">
      <div class="container">
        <h2>Why Choose Whittaker Agency?</h2>
        <div class="benefits-grid">
          <div v-for="benefit in benefits" :key="benefit.title" class="benefit-card">
            <div class="benefit-icon">{{ benefit.icon }}</div>
            <h3>{{ benefit.title }}</h3>
            <p>{{ benefit.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Oregon Connection Section -->
    <section class="oregon-connection">
      <div class="container">
        <div class="oregon-content">
          <div class="oregon-text">
            <h2>Proudly Serving Oregon</h2>
            <p>Born and raised in the Pacific Northwest, we understand the unique needs of Oregon families and businesses. From the coast to the mountains, we're here to protect what matters most to you.</p>
            <p>Our deep roots in Oregon mean we're not just your insurance agency—we're your neighbors, committed to the communities we serve.</p>
            <div class="section-cta">
              <RouterLink to="/about" class="btn btn-primary">Learn More About Us</RouterLink>
            </div>
          </div>
          <div class="oregon-image">
            <img src="/images/oregon-multnomah.jpg" alt="Multnomah Falls Oregon" class="falls-image">
          </div>
        </div>
      </div>
    </section>

    <!-- Visit Our Office Section -->
    <section class="visit-office">
      <div class="container">
        <h2>Visit Our Office Today</h2>
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
                Monday - Friday: 9:00 AM - 5:00 PM<br>
                Saturday - Sunday: Closed
              </p>
              <p class="contact">
                <strong>Phone:</strong> <a href="tel:+15035551234">(503) 555-1234</a><br>
                <strong>Email:</strong> <a href="mailto:info@whittakeragency.com">info@whittakeragency.com</a>
              </p>
              <a href="https://www.google.com/maps/dir/?api=1&destination=12520+SW+68th+Ave+A,+Tigard,+OR+97223" target="_blank" class="btn btn-primary">Get Directions</a>
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
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const services = [
  {
    id: 'auto',
    name: 'Auto Insurance',
    icon: '🚗',
    description: 'Comprehensive coverage for your vehicles with competitive rates.'
  },
  {
    id: 'home',
    name: 'Home Insurance',
    icon: '🏠',
    description: 'Protect your home and belongings from unexpected events.'
  },
  {
    id: 'life',
    name: 'Life Insurance',
    icon: '❤️',
    description: 'Secure your family\'s financial future with tailored life insurance.'
  },
  {
    id: 'business',
    name: 'Business Insurance',
    icon: '💼',
    description: 'Comprehensive coverage for your business operations and assets.'
  },
  {
    id: 'health',
    name: 'Health Insurance',
    icon: '🏥',
    description: 'Quality healthcare coverage for you and your family.'
  },
  {
    id: 'umbrella',
    name: 'Umbrella Insurance',
    icon: '☂️',
    description: 'Additional liability protection beyond standard policies.'
  },
  {
    id: 'motorcycle',
    name: 'Motorcycle Insurance',
    icon: '🏍️',
    description: 'Specialized coverage for motorcycle enthusiasts.'
  },
  {
    id: 'rv',
    name: 'RV Insurance',
    icon: '🚐',
    description: 'Protect your recreational vehicles and travel adventures.'
  }
]

const benefits = [
  {
    title: 'Local Expertise',
    icon: '🌲',
    description: 'Deep understanding of Oregon\'s unique insurance needs and regulations.'
  },
  {
    title: 'Personalized Service',
    icon: '🤝',
    description: 'Tailored insurance solutions that fit your specific situation.'
  },
  {
    title: 'Trusted Advisors',
    icon: '⭐',
    description: 'Years of experience helping families and businesses protect what matters.'
  },
  {
    title: '24/7 Support',
    icon: '📞',
    description: 'Always here when you need us, day or night.'
  }
]
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

/* Services Section */
.services {
  padding: var(--spacing-xl) 0;
  background-color: #f8f9fa;
}

.section-description {
  text-align: center;
  color: #666;
  margin-bottom: var(--spacing-lg);
  font-size: 1.1rem;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
  margin-top: var(--spacing-lg);
}

.service-card {
  background: white;
  padding: var(--spacing-lg);
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  color: inherit;
  display: block;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.service-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
}

.service-card h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.service-card p {
  color: #666;
  line-height: 1.6;
}

/* Why Choose Us Section */
.why-choose-us {
  padding: var(--spacing-xl) 0;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
  margin-top: var(--spacing-lg);
}

.benefit-card {
  text-align: center;
  padding: var(--spacing-lg);
}

.benefit-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
}

.benefit-card h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.benefit-card p {
  color: #666;
  line-height: 1.6;
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

/* Visit Our Office Section */
.visit-office {
  padding: var(--spacing-xl) 0;
  background: white;
}

.visit-office h2 {
  color: var(--color-primary);
  font-size: 2.2rem;
  margin-bottom: var(--spacing-xl);
  text-align: center;
}

.office-content {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: var(--spacing-xl);
  align-items: start;
}

.address-box {
  background: #f8f9fa;
  padding: var(--spacing-xl);
  border-radius: 12px;
  border-left: 5px solid var(--color-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.address-box h3 {
  color: var(--color-primary);
  font-size: 1.5rem;
  margin-bottom: var(--spacing-md);
}

.address-box p {
  margin-bottom: var(--spacing-md);
  line-height: 1.7;
  color: #666;
}

.address {
  font-size: 1.1rem;
  font-weight: 500;
  color: #444;
}

.hours,
.contact {
  font-size: 1rem;
}

.contact a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.3s ease;
}

.contact a:hover {
  color: #1a4d2e;
  text-decoration: underline;
}

.address-box .btn {
  margin-top: var(--spacing-md);
  width: 100%;
}

.office-map {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.office-map iframe {
  display: block;
  width: 100%;
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
  .hero h1 {
    font-size: 2rem;
  }

  .tagline {
    font-size: 1.2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .oregon-content {
    grid-template-columns: 1fr;
  }

  .office-content {
    grid-template-columns: 1fr;
  }

  .office-map iframe {
    height: 300px;
  }

  .services-grid,
  .benefits-grid,
  .team-grid {
    grid-template-columns: 1fr;
  }
}
</style>
