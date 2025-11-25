<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <!-- Company Info -->
        <div class="footer-section">
          <h3>Whittaker Agency</h3>
          <p class="tagline">Your Family, Your Business, Our Priority</p>
          <p class="description">Serving Oregon families and businesses with comprehensive insurance solutions since 2010.</p>
        </div>

        <!-- Contact Info -->
        <div class="footer-section">
          <h4>Contact Us</h4>
          <p><a href="mailto:info@whittakeragency.com">info@whittakeragency.com</a></p>
          <p><a href="tel:+15036205999">(503) 620-5999</a></p>
          <p>Hours: Mon-Fri 8AM-5PM</p>
          <p>Sat-Sun: By appointment</p>
        </div>

        <!-- Quick Links -->
        <div class="footer-section">
          <h4>Quick Links</h4>
          <ul>
            <li><RouterLink to="/services">Our Services</RouterLink></li>
            <li><RouterLink to="/about">About Us</RouterLink></li>
            <li><RouterLink to="/team">Our Team</RouterLink></li>
            <li v-if="authStore.isAuthenticated">
              <RouterLink to="/dashboard">Dashboard</RouterLink>
            </li>
            <li v-else>
              <RouterLink to="/register">Get a Quote</RouterLink>
            </li>
          </ul>
        </div>

        <!-- Location -->
        <div class="footer-section">
          <h4>Location</h4>
          <p>Serving all of Oregon</p>
          <p>Portland, OR</p>
          <p class="mt-sm">
            <RouterLink to="/about">Learn about our Oregon connection</RouterLink>
          </p>
        </div>
      </div>

      <!-- Footer Bottom -->
      <div class="footer-bottom">
        <p>&copy; 2025 Whittaker Agency. All rights reserved.</p>
        <div class="footer-links">
          <a href="/privacy">Privacy Policy</a>
          <span class="separator">•</span>
          <a href="/terms">Terms of Service</a>
          <span class="separator">•</span>
          <a href="/accessibility">Accessibility</a>
          <span class="separator">•</span>
          <RouterLink to="/attributions">Attributions</RouterLink>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>
.footer {
  background-color: #2c3e50;
  background-image: url('/images/oregon-stag.jpg');
  background-size: cover;
  background-position: center;
  background-blend-mode: overlay;
  color: white;
  padding: var(--spacing-xl) 0 var(--spacing-md);
  margin-top: var(--spacing-xl);
  position: relative;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(44, 62, 80, 0.92);
  pointer-events: none;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-lg);
  position: relative;
  z-index: 1;
}

.footer-section h3 {
  color: white;
  margin-bottom: var(--spacing-sm);
  font-size: 1.5rem;
}

.footer-section h4 {
  color: white;
  margin-bottom: var(--spacing-md);
  font-size: 1.1rem;
}

.tagline {
  color: #ecf0f1;
  font-style: italic;
  margin-bottom: var(--spacing-sm);
  font-size: 0.95rem;
}

.description {
  color: #bdc3c7;
  line-height: 1.6;
  font-size: 0.9rem;
}

.footer-section p {
  color: #ecf0f1;
  margin-bottom: var(--spacing-sm);
  line-height: 1.6;
}

.footer-section a {
  color: #ecf0f1;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-section a:hover {
  color: var(--color-accent, #4a90e2);
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: var(--spacing-sm);
}

.mt-sm {
  margin-top: var(--spacing-sm);
}

/* Footer Bottom */
.footer-bottom {
  border-top: 1px solid #34495e;
  padding-top: var(--spacing-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  position: relative;
  z-index: 1;
}

.footer-bottom p {
  color: #95a5a6;
  margin: 0;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.footer-links a {
  color: #95a5a6;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #ecf0f1;
}

.separator {
  color: #7f8c8d;
  font-size: 0.8rem;
}

/* Responsive */
@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }

  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }

  .footer-links {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
