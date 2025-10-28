<template>
  <div class="vehicle-services">
    <div class="services-layout">
      <!-- Left Sidebar -->
      <aside class="services-sidebar">
        <div class="sidebar-sticky">
          <div class="sidebar-header">
            <h3>Vehicle Insurance</h3>
            <button class="mobile-toggle" @click="toggleMobileSidebar" aria-label="Toggle menu">
              {{ showMobileSidebar ? '✕' : '☰' }}
            </button>
          </div>

          <nav class="sidebar-nav" :class="{ 'mobile-open': showMobileSidebar }">
            <a
              v-for="service in services"
              :key="service.id"
              :href="`#${service.id}`"
              class="nav-item"
              :class="{ 'active': activeSection === service.id }"
              @click="scrollToSection(service.id)"
            >
              <span v-if="service.iconType === 'emoji'" class="nav-icon">{{ service.icon }}</span>
              <img v-else :src="service.icon" :alt="service.name" class="nav-icon-img">
              <span>{{ service.name }}</span>
            </a>
          </nav>

          <div class="sidebar-footer">
            <RouterLink to="/services" class="back-link">← All Services</RouterLink>
          </div>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="services-content">
        <!-- Auto Insurance -->
        <section v-show="activeSection === 'auto'" class="service-section style-option-1-2">
          <div class="section-header-colored">
            <h2>Auto Insurance</h2>
          </div>
          <p class="intro">Protect your vehicle with comprehensive auto insurance coverage tailored to Oregon drivers.</p>

          <div class="accent-card">
            <h3 class="colored-subheader">Coverage Options:</h3>
            <ul>
              <li><strong>Liability Coverage</strong> - Required in Oregon, protects you if you cause an accident</li>
              <li><strong>Collision Coverage</strong> - Pays for repairs to your vehicle after an accident</li>
              <li><strong>Comprehensive Coverage</strong> - Covers non-collision damage (theft, vandalism, weather)</li>
              <li><strong>Uninsured/Underinsured Motorist</strong> - Protection when the other driver lacks insurance</li>
              <li><strong>Medical Payments</strong> - Covers healthcare costs after an accident</li>
              <li><strong>Personal Injury Protection (PIP)</strong> - Medical expenses and lost wages</li>
            </ul>
          </div>

          <div class="accent-card">
            <h3 class="colored-subheader">Oregon Requirements:</h3>
            <ul>
              <li>Minimum liability: $25,000/$50,000/$20,000</li>
              <li>Proof of insurance required at all times</li>
              <li>SR-22 filing available for high-risk drivers</li>
            </ul>
          </div>

          <div class="cta-box gradient-cta">
            <p>Get competitive rates with personalized service from local Oregon experts.</p>
            <RouterLink v-if="!authStore.isAuthenticated" to="/register" class="btn btn-primary">Get a Quote</RouterLink>
          </div>
        </section>

        <!-- Motorcycle Insurance -->
        <section v-show="activeSection === 'motorcycle'" class="service-section style-option-1-2">
          <div class="section-header-colored">
            <h2>Motorcycle Insurance</h2>
          </div>
          <p class="intro">Hit the road with confidence - specialized coverage for motorcycle enthusiasts.</p>

          <div class="accent-card">
            <h3 class="colored-subheader">Coverage Options:</h3>
          <ul>
            <li><strong>Liability Coverage</strong> - Required in Oregon for motorcycles</li>
            <li><strong>Collision</strong> - Repairs after an accident</li>
            <li><strong>Comprehensive</strong> - Theft and non-collision damage</li>
            <li><strong>Accessory Coverage</strong> - Custom parts and equipment protection</li>
            <li><strong>Roadside Assistance</strong> - Towing and emergency service</li>
            <li><strong>Passenger Liability</strong> - Protection for riders</li>
          </ul>
          </div>

          <div class="accent-card">
            <h3 class="colored-subheader">Oregon Requirements:</h3>
          <ul>
            <li>Same minimum liability as auto insurance</li>
            <li>Proof of insurance required</li>
            <li>Seasonal storage discounts available</li>
          </ul>
          </div>

          <div class="cta-box gradient-cta">
            <p>Specialized coverage designed for riders by riders.</p>
            <RouterLink v-if="!authStore.isAuthenticated" to="/register" class="btn btn-primary">Get a Quote</RouterLink>
          </div>
        </section>

        <!-- ATV/Off-Road Insurance -->
        <section v-show="activeSection === 'atv'" class="service-section style-option-1-2">
          <div class="section-header-colored">
            <h2>ATV/Off-Road Insurance</h2>
          </div>
          <p class="intro">Adventure with peace of mind - coverage for your off-road vehicles.</p>

          <div class="accent-card">
            <h3 class="colored-subheader">Coverage Options:</h3>
            <ul>
              <li><strong>Liability Coverage</strong> - Protection for injuries to others</li>
              <li><strong>Physical Damage</strong> - Repairs or replacement of your ATV</li>
              <li><strong>Collision</strong> - Accident coverage on and off-road</li>
              <li><strong>Comprehensive</strong> - Theft, vandalism, and other perils</li>
              <li><strong>Medical Payments</strong> - Healthcare costs for you and passengers</li>
              <li><strong>Accessories Coverage</strong> - Custom equipment and gear</li>
            </ul>
          </div>

          <div class="accent-card">
            <h3 class="colored-subheader">What We Cover:</h3>
            <ul>
              <li>ATVs (All-Terrain Vehicles)</li>
              <li>UTVs (Utility Terrain Vehicles)</li>
              <li>Side-by-sides</li>
              <li>Dirt bikes and off-road motorcycles</li>
            </ul>
          </div>

          <div class="cta-box gradient-cta">
            <p>Explore Oregon's trails with confidence.</p>
            <RouterLink v-if="!authStore.isAuthenticated" to="/register" class="btn btn-primary">Get a Quote</RouterLink>
          </div>
        </section>

        <!-- Roadside Assistance -->
        <section v-show="activeSection === 'roadside'" class="service-section style-option-1-2">
          <div class="section-header-colored">
            <h2>Roadside Assistance</h2>
          </div>
          <p class="intro">24/7 help when you need it most - comprehensive roadside protection.</p>

          <div class="accent-card">
            <h3 class="colored-subheader">Services Included:</h3>
            <ul>
              <li><strong>Towing</strong> - Transport to nearest repair facility</li>
              <li><strong>Battery Jump-Start</strong> - Get back on the road quickly</li>
              <li><strong>Flat Tire Service</strong> - Tire change or repair</li>
              <li><strong>Fuel Delivery</strong> - Emergency gas delivery</li>
              <li><strong>Lockout Service</strong> - Key replacement or locksmith</li>
              <li><strong>Winching</strong> - Recovery from ditches or snow</li>
            </ul>
          </div>

          <div class="accent-card">
            <h3 class="colored-subheader">Benefits:</h3>
            <ul>
              <li>Available 24 hours a day, 7 days a week</li>
              <li>Coverage extends to you, not just your vehicle</li>
              <li>Works with rentals and borrowed vehicles</li>
              <li>Nationwide coverage for travel</li>
            </ul>
          </div>

          <div class="cta-box gradient-cta">
            <p>Never be stranded again with comprehensive roadside coverage.</p>
            <RouterLink v-if="!authStore.isAuthenticated" to="/register" class="btn btn-primary">Get a Quote</RouterLink>
          </div>
        </section>

        <!-- Snowmobile Insurance -->
        <section v-show="activeSection === 'snowmobile'" class="service-section style-option-1-2">
          <div class="section-header-colored">
            <h2>Snowmobile Insurance</h2>
          </div>
          <p class="intro">Protect your winter adventures with specialized snowmobile coverage.</p>

          <div class="accent-card">
            <h3 class="colored-subheader">Coverage Options:</h3>
            <ul>
              <li><strong>Liability Coverage</strong> - Injuries and property damage to others</li>
              <li><strong>Collision</strong> - Damage from accidents</li>
              <li><strong>Comprehensive</strong> - Theft, fire, and vandalism</li>
              <li><strong>Medical Payments</strong> - Healthcare costs for you and passengers</li>
              <li><strong>Accessories</strong> - Custom parts and equipment</li>
              <li><strong>Trailer Coverage</strong> - Protection for snowmobile trailers</li>
            </ul>
          </div>

          <div class="accent-card">
            <h3 class="colored-subheader">Oregon Winter Protection:</h3>
            <ul>
              <li>Coverage for Mt. Hood and Cascade Range riding</li>
              <li>Seasonal policies available</li>
              <li>Off-season storage discounts</li>
            </ul>
          </div>

          <div class="cta-box gradient-cta">
            <p>Enjoy Oregon's winter wonderland with complete protection.</p>
            <RouterLink v-if="!authStore.isAuthenticated" to="/register" class="btn btn-primary">Get a Quote</RouterLink>
          </div>
        </section>

        <!-- Boat Insurance -->
        <section v-show="activeSection === 'boat'" class="service-section style-option-1-2">
          <div class="section-header-colored">
            <h2>Boat Insurance</h2>
          </div>
          <p class="intro">Navigate Oregon's waters with confidence - comprehensive marine coverage.</p>

          <div class="accent-card">
            <h3 class="colored-subheader">Coverage Options:</h3>
          <ul>
            <li><strong>Hull Coverage</strong> - Physical damage to your boat</li>
            <li><strong>Liability</strong> - Injuries and property damage to others</li>
            <li><strong>Medical Payments</strong> - Healthcare costs for passengers</li>
            <li><strong>Uninsured Boater</strong> - Protection from uninsured watercraft</li>
            <li><strong>Personal Property</strong> - Fishing equipment, water skis, etc.</li>
            <li><strong>Towing & Assistance</strong> - On-water emergency service</li>
          </ul>
          </div>

          <div class="accent-card">
            <h3 class="colored-subheader">What We Cover:</h3>
          <ul>
            <li>Powerboats and speedboats</li>
            <li>Sailboats</li>
            <li>Fishing boats</li>
            <li>Personal watercraft (jet skis)</li>
            <li>Kayaks and canoes</li>
          </ul>
          </div>

          <div class="cta-box gradient-cta">
            <p>Perfect for Columbia River, Willamette River, and Oregon Coast adventures.</p>
            <RouterLink v-if="!authStore.isAuthenticated" to="/register" class="btn btn-primary">Get a Quote</RouterLink>
          </div>
        </section>

        <!-- RV Insurance -->
        <section v-show="activeSection === 'rv'" class="service-section style-option-1-2">
          <div class="section-header-colored">
            <h2>RV Insurance</h2>
          </div>
          <p class="intro">Protect your home on wheels with comprehensive RV coverage.</p>

          <div class="accent-card">
            <h3 class="colored-subheader">Coverage Types:</h3>
            <ul>
              <li><strong>Full-Time RV Coverage</strong> - If your RV is your primary residence</li>
              <li><strong>Vacation Use Coverage</strong> - For recreational travel only</li>
              <li><strong>Personal Belongings</strong> - Contents inside your RV</li>
              <li><strong>Attached Accessories</strong> - Awnings, satellite dishes, etc.</li>
              <li><strong>Emergency Expense Coverage</strong> - Lodging if RV is unusable</li>
              <li><strong>Roadside Assistance</strong> - Towing and emergency repairs</li>
            </ul>
          </div>

          <div class="accent-card">
            <h3 class="colored-subheader">RV Types Covered:</h3>
            <ul>
              <li>Class A, B, C motorhomes</li>
              <li>Travel trailers</li>
              <li>Fifth wheels</li>
              <li>Pop-up campers</li>
              <li>Toy haulers</li>
            </ul>
          </div>

          <div class="cta-box gradient-cta">
            <p>Hit the open road worry-free with comprehensive RV protection.</p>
            <RouterLink v-if="!authStore.isAuthenticated" to="/register" class="btn btn-primary">Get a Quote</RouterLink>
          </div>
        </section>

        <!-- Vehicle Protection -->
        <section v-show="activeSection === 'vehicle-protection'" class="service-section style-option-1-2">
          <div class="section-header-colored">
            <h2>Vehicle Protection Plans</h2>
          </div>
          <p class="intro">Extended coverage for mechanical breakdowns and repairs beyond manufacturer warranty.</p>

          <div class="accent-card">
            <h3 class="colored-subheader">What's Covered:</h3>
            <ul>
              <li><strong>Engine Components</strong> - Major engine repairs and replacements</li>
              <li><strong>Transmission</strong> - Transmission rebuilds and replacements</li>
              <li><strong>Drive System</strong> - Drivetrain and differential repairs</li>
              <li><strong>Electrical System</strong> - Computer modules and sensors</li>
              <li><strong>Air Conditioning</strong> - A/C compressor and components</li>
              <li><strong>Steering & Suspension</strong> - Power steering and suspension components</li>
            </ul>
          </div>

          <div class="accent-card">
            <h3 class="colored-subheader">Benefits:</h3>
            <ul>
              <li>Coverage after factory warranty expires</li>
              <li>Choice of repair facilities</li>
              <li>Transferable to new owner (increases resale value)</li>
              <li>24/7 roadside assistance included</li>
              <li>Rental car reimbursement</li>
            </ul>
          </div>

          <div class="cta-box gradient-cta">
            <p>Protect your investment with extended vehicle protection.</p>
            <RouterLink v-if="!authStore.isAuthenticated" to="/register" class="btn btn-primary">Get a Quote</RouterLink>
          </div>
        </section>

        <!-- Final CTA -->
        <section v-show="activeSection === 'auto'" class="final-cta">
          <h2>Ready to Protect Your Vehicles?</h2>
          <p>Our vehicle insurance experts are here to help you find the perfect coverage.</p>
          <div class="cta-buttons">
            <RouterLink v-if="!authStore.isAuthenticated" to="/register" class="btn btn-primary btn-lg">Get a Quote</RouterLink>
            <a href="tel:+15035551234" class="btn btn-outline btn-lg">Call (503) 555-1234</a>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const showMobileSidebar = ref(false)
const activeSection = ref('auto')

const services = [
  { id: 'auto', name: 'Auto', icon: '🚗', iconType: 'emoji' },
  { id: 'motorcycle', name: 'Motorcycle', icon: '🏍️', iconType: 'emoji' },
  { id: 'atv', name: 'ATV/Off-road', icon: '/images/icons/atv.png', iconType: 'image' },
  { id: 'roadside', name: 'Roadside', icon: '🛠️', iconType: 'emoji' },
  { id: 'snowmobile', name: 'Snowmobile', icon: '/images/icons/snowmobile.png', iconType: 'image' },
  { id: 'boat', name: 'Boat', icon: '⛵', iconType: 'emoji' },
  { id: 'rv', name: 'RV', icon: '🚐', iconType: 'emoji' },
  { id: 'vehicle-protection', name: 'Vehicle Protection', icon: '🛡️', iconType: 'emoji' }
]

const toggleMobileSidebar = () => {
  showMobileSidebar.value = !showMobileSidebar.value
}

const scrollToSection = (sectionId: string) => {
  // Simply change the active section - no scrolling
  activeSection.value = sectionId
  showMobileSidebar.value = false

  // Scroll content area to top
  const contentArea = document.querySelector('.services-content')
  if (contentArea) {
    contentArea.scrollTop = 0
  }
  // Also scroll window to top of content
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}
</script>

<style scoped>
.vehicle-services {
  width: 100%;
  background: #f8f9fa;
}

/* Layout */
.services-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: var(--spacing-xl);
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-lg);
  align-items: start;
}

/* Sidebar */
.services-sidebar {
  position: relative;
}

.sidebar-sticky {
  position: sticky;
  top: 100px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.sidebar-header {
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.25rem;
}

.sidebar-nav {
  padding: var(--spacing-md);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-sm) var(--spacing-sm) var(--spacing-xs);
  color: #666;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s ease;
  margin-bottom: var(--spacing-xs);
  font-weight: 500;
}

.nav-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.nav-icon-img {
  width: 24px;
  height: 24px;
  min-width: 24px;
  flex-shrink: 0;
  object-fit: contain;
  display: block;
}

.nav-item:hover {
  background: #f8f9fa;
  color: var(--color-primary);
}

.nav-item.active {
  background: var(--color-primary);
  color: white;
}

.sidebar-footer {
  padding: var(--spacing-md);
  border-top: 1px solid #e9ecef;
}

.back-link {
  display: block;
  text-align: center;
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
  padding: var(--spacing-sm);
  transition: color 0.2s ease;
}

.back-link:hover {
  color: #1a4d2e;
}

/* Main Content */
.services-content {
  background: white;
  border-radius: 12px;
  padding: var(--spacing-xl);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.service-section {
  /* No margins/padding needed since only one section visible at a time */
}

.section-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-sm);
}

.service-section h2 {
  color: var(--color-primary);
  font-size: 2rem;
  margin-bottom: var(--spacing-md);
}

.intro {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.5;
  margin-bottom: var(--spacing-md);
}

.service-section h3 {
  color: var(--color-primary);
  font-size: 1.3rem;
  margin-top: var(--spacing-md);
  margin-bottom: var(--spacing-sm);
}

.service-section ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: var(--spacing-md);
}

.service-section ul li {
  padding: 0.25rem 0;
  padding-left: 1.5rem;
  position: relative;
  color: #666;
  line-height: 1.5;
}

.service-section ul li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--color-primary);
  font-weight: bold;
}

.cta-box {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: var(--spacing-md);
  border-radius: 8px;
  margin-top: var(--spacing-md);
  text-align: center;
}

.cta-box p {
  color: #666;
  font-weight: 500;
  margin-bottom: var(--spacing-sm);
}

/* Final CTA */
.final-cta {
  text-align: center;
  padding: var(--spacing-xl) 0;
  border-top: 2px solid #e9ecef;
  margin-top: var(--spacing-xl);
}

.final-cta h2 {
  color: var(--color-primary);
  font-size: 2rem;
  margin-bottom: var(--spacing-md);
}

.final-cta p {
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

/* ========================================
   STYLE OPTIONS FOR DIFFERENT SECTIONS
======================================== */

/* Option 1: Colored Section Headers */
.style-option-1 .section-header-colored {
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  padding: var(--spacing-md);
  border-radius: 12px;
  margin-bottom: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  color: white;
}

.style-option-1 .section-header-colored .section-icon {
  font-size: 4rem;
  margin: 0;
}

.style-option-1 .section-header-colored h2 {
  color: white;
  margin: 0;
}

.style-option-1 .colored-subheader {
  background: linear-gradient(135deg, rgba(47, 79, 79, 0.1) 0%, rgba(26, 77, 46, 0.1) 100%);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 8px;
  border-left: 4px solid var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.style-option-1 .gradient-cta {
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  color: white;
}

.style-option-1 .gradient-cta p {
  color: white;
}

.style-option-1 .gradient-cta .btn-primary {
  background: white;
  color: var(--color-primary);
}

/* Option 2: Accent Cards */
.style-option-2 .accent-card {
  background: #f8f9fa;
  border-left: 5px solid var(--color-primary);
  padding: var(--spacing-md);
  border-radius: 8px;
  margin-bottom: var(--spacing-md);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.style-option-2 .accent-card h3 {
  color: var(--color-primary);
  margin-top: 0;
}

/* Option 3: Icon Enhancements */
.style-option-3 .icon-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--spacing-md);
  box-shadow: 0 8px 24px rgba(47, 79, 79, 0.2);
}

.style-option-3 .icon-circle .section-icon {
  font-size: 4rem;
  margin: 0;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.style-option-3 h2 {
  text-align: center;
}

/* Option 4: Simple/Clean (sidebar styling is global) */
.style-option-4 {
  /* Simple clean design - minimal styling */
}

/* Option 5: Combined Approach */
.style-option-5 .section-header-combined {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  padding: var(--spacing-md);
  background: linear-gradient(135deg, rgba(47, 79, 79, 0.05) 0%, rgba(26, 77, 46, 0.05) 100%);
  border-radius: 12px;
  border: 2px solid var(--color-primary);
}

.style-option-5 .icon-circle-large {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(47, 79, 79, 0.3);
}

.style-option-5 .icon-circle-large .section-icon {
  font-size: 3.5rem;
  margin: 0;
}

.style-option-5 .section-header-combined h2 {
  margin: 0 0 var(--spacing-xs) 0;
  color: var(--color-primary);
}

.style-option-5 .header-subtitle {
  font-size: 1.1rem;
  color: #666;
  font-weight: 500;
  margin: 0;
}

.style-option-5 .feature-box {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.style-option-5 .feature-box:hover {
  border-color: var(--color-primary);
  box-shadow: 0 4px 16px rgba(47, 79, 79, 0.1);
}

.style-option-5 .feature-box h3 {
  color: var(--color-primary);
  margin-top: 0;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.style-option-5 .gradient-cta {
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  color: white;
}

.style-option-5 .gradient-cta p {
  color: white;
}

.style-option-5 .gradient-cta .btn-primary {
  background: white;
  color: var(--color-primary);
}

/* Option 1+2: Combined Colored Headers and Accent Cards */
.style-option-1-2 .section-header-colored {
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 8px;
  margin-bottom: var(--spacing-md);
  color: white;
}

.style-option-1-2 .section-header-colored h2 {
  color: white;
  margin: 0;
  font-size: 1.5rem;
}

.style-option-1-2 .accent-card {
  background: #f8f9fa;
  border-left: 5px solid var(--color-primary);
  padding: var(--spacing-md);
  border-radius: 8px;
  margin-bottom: var(--spacing-md);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.style-option-1-2 .accent-card h3 {
  color: var(--color-primary);
  margin-top: 0;
}

.style-option-1-2 .colored-subheader {
  background: linear-gradient(135deg, rgba(47, 79, 79, 0.1) 0%, rgba(26, 77, 46, 0.1) 100%);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 6px;
}

.style-option-1-2 .gradient-cta {
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  color: white;
}

.style-option-1-2 .gradient-cta p {
  color: white;
}

.style-option-1-2 .gradient-cta .btn-primary {
  background: white;
  color: var(--color-primary);
}

/* Enhanced sidebar active state (applies globally) */
.nav-item.active {
  background: var(--color-primary);
  color: white;
  border-left: 4px solid #1a4d2e;
  font-weight: 600;
}

/* ======================================== */

/* Responsive */
@media (max-width: 1024px) {
  .services-layout {
    grid-template-columns: 240px 1fr;
    gap: var(--spacing-lg);
  }
}

@media (max-width: 768px) {
  .services-layout {
    grid-template-columns: 1fr;
    padding: var(--spacing-md);
  }

  .sidebar-sticky {
    position: static;
  }

  .mobile-toggle {
    display: block;
  }

  .sidebar-nav {
    display: none;
    padding: 0;
  }

  .sidebar-nav.mobile-open {
    display: block;
    padding: var(--spacing-md);
  }

  .services-content {
    padding: var(--spacing-lg);
  }

  .section-icon {
    font-size: 2.5rem;
  }

  .service-section h2 {
    font-size: 1.6rem;
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
