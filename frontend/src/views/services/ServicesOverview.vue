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
            <div class="card-content">
              <h3>{{ category.name }}</h3>
              <p>{{ category.description }}</p>
            </div>
            <span class="card-arrow">→</span>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Claims Info Callout -->
    <section class="claims-callout">
      <div class="container">
        <div class="callout-content">
          <span class="callout-icon">📋</span>
          <div class="callout-text">
            <h3>Already have coverage with us?</h3>
            <p>If you need to file a claim, learn what information to gather and how our claims process works.</p>
          </div>
          <RouterLink to="/claims" class="callout-link">Learn About Filing Claims →</RouterLink>
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
          <a href="tel:+15036205999" class="btn btn-outline btn-lg">Call (503) 620-5999</a>
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
  background: var(--color-primary);
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
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 1rem;
}

.category-card {
  background: white;
  padding: 1.25rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  text-decoration: none;
  color: inherit;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  border-left: 4px solid transparent;
}

.category-card:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  border-left-color: var(--color-primary);
}

.card-icon {
  font-size: 3rem;
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(47, 79, 79, 0.1);
  border-radius: 12px;
}

.card-content {
  flex: 1;
}

.category-card h3 {
  color: var(--color-primary);
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.card-content p {
  color: #666;
  line-height: 1.5;
  font-size: 0.95rem;
}

.card-arrow {
  color: var(--color-primary);
  font-size: 1.5rem;
  font-weight: bold;
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.category-card:hover .card-arrow {
  transform: translateX(5px);
}

/* Claims Callout Section */
.claims-callout {
  padding: var(--spacing-lg) 0;
  background: #f8f9fa;
}

.callout-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: white;
  padding: 1.5rem 2rem;
  border-radius: 8px;
  border-left: 4px solid #ffc107;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.callout-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.callout-text {
  flex: 1;
}

.callout-text h3 {
  color: #333;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.callout-text p {
  color: #666;
  font-size: 0.95rem;
  margin: 0;
  line-height: 1.5;
}

.callout-link {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
  white-space: nowrap;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.callout-link:hover {
  background: rgba(0, 61, 165, 0.05);
  color: var(--color-primary-dark);
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
  background: var(--color-primary-dark);
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

  .card-icon {
    width: 60px;
    height: 60px;
    font-size: 2rem;
  }

  .category-card {
    gap: 1rem;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }

  .btn-lg {
    width: 100%;
    max-width: 300px;
  }

  .callout-content {
    flex-direction: column;
    text-align: center;
    padding: 1.25rem 1rem;
  }

  .callout-link {
    white-space: normal;
  }
}
</style>
