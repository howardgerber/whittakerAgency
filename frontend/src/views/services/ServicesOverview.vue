<template>
  <div class="services-overview">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <h1>Insurance Services</h1>
        <p class="subtitle">Comprehensive coverage for every aspect of your life</p>
      </div>
    </section>

    <!-- Category Cards Grid -->
    <section class="categories">
      <div class="container">
        <div class="category-grid">
          <RouterLink
            v-for="category in categories"
            :key="category.id"
            :to="category.path"
            class="category-card"
          >
            <div class="card-icon">{{ category.icon }}</div>
            <h3>{{ category.name }}</h3>
            <p>{{ category.description }}</p>
            <span class="card-arrow">→</span>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <h2>Need Help Choosing?</h2>
        <p>Our expert advisors are here to help you find the perfect coverage for your needs.</p>
        <div class="cta-buttons">
          <RouterLink v-if="!authStore.isAuthenticated" to="/register" class="btn btn-primary btn-lg">Get a Quote</RouterLink>
          <a href="tel:+15035551234" class="btn btn-outline btn-lg">Call (503) 555-1234</a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const categories = [
  {
    id: 'vehicle',
    name: 'Vehicle',
    icon: '🚗',
    path: '/services/vehicle',
    description: 'Auto, Motorcycle, RV, Boat, ATV, and more vehicle coverage options'
  },
  {
    id: 'property',
    name: 'Property',
    icon: '🏠',
    path: '/services/property',
    description: 'Homeowners, Renters, Condo, Landlord, and Mobile Home insurance'
  },
  {
    id: 'life',
    name: 'Life',
    icon: '❤️',
    path: '/services/life',
    description: 'Term, Whole, and Universal life insurance to protect your family\'s future'
  },
  {
    id: 'business',
    name: 'Business',
    icon: '💼',
    path: '/services/business',
    description: 'Comprehensive coverage for businesses of all sizes and industries'
  },
  {
    id: 'identity',
    name: 'Identity Protection',
    icon: '🔒',
    path: '/services/identity',
    description: 'Protect yourself from identity theft and fraud'
  },
  {
    id: 'phone',
    name: 'Phone Protection',
    icon: '📱',
    path: '/services/phone',
    description: 'Coverage for loss, theft, and damage to your mobile devices'
  },
  {
    id: 'other',
    name: 'Other Services',
    icon: '☂️',
    path: '/services/other',
    description: 'Umbrella, Health, Pet, Travel, Jewelry, and specialized coverage options'
  }
]
</script>

<style scoped>
.services-overview {
  width: 100%;
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  color: white;
  padding: var(--spacing-xl) 0;
  text-align: center;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: var(--spacing-md);
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.95;
}

/* Categories Section */
.categories {
  padding: var(--spacing-xl) 0;
  background: #f8f9fa;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.category-card {
  background: white;
  padding: var(--spacing-xl);
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  text-decoration: none;
  color: inherit;
  position: relative;
  overflow: hidden;
}

.category-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.category-card:hover::before {
  transform: scaleX(1);
}

.card-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-md);
}

.category-card h3 {
  color: var(--color-primary);
  font-size: 1.5rem;
  margin-bottom: var(--spacing-sm);
}

.category-card p {
  color: #666;
  line-height: 1.7;
  margin-bottom: var(--spacing-md);
}

.card-arrow {
  display: inline-block;
  color: var(--color-primary);
  font-size: 1.5rem;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.category-card:hover .card-arrow {
  transform: translateX(5px);
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

  .category-grid {
    grid-template-columns: 1fr;
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
