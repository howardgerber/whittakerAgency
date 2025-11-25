<template>
  <div class="team-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <h1>Meet Our Expert Team</h1>
        <p class="subtitle">Experienced professionals dedicated to protecting what matters most to you</p>
      </div>
    </section>

    <!-- Team Introduction -->
    <section class="team-intro">
      <div class="container">
        <p class="intro-text">
          Our team of experienced insurance professionals is committed to providing personalized service
          and expert guidance. With deep roots in Oregon and years of industry experience, we're here
          to help you navigate your insurance needs with confidence.
        </p>
      </div>
    </section>

    <!-- Team Members Grid -->
    <section class="team-members">
      <div class="container">
        <div class="team-grid">
          <div
            v-for="member in teamMembers"
            :key="member.name"
            class="team-card"
          >
            <div class="member-photo">
              <div class="photo-placeholder">{{ member.initials }}</div>
            </div>

            <div class="member-info">
              <h3>{{ member.name }}</h3>
              <p class="member-role">{{ member.role }}</p>
              <p class="member-bio">{{ member.bio }}</p>

              <div v-if="member.specialties.length > 0" class="member-specialties">
                <h4>Specialties:</h4>
                <ul>
                  <li v-for="specialty in member.specialties" :key="specialty">
                    {{ specialty }}
                  </li>
                </ul>
              </div>

              <div v-if="member.email" class="member-contact">
                <a :href="`mailto:${member.email}`" class="contact-link">
                  📧 {{ member.email }}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <h2>Ready to Work With Our Team?</h2>
        <p>Contact us today to discuss your insurance needs with one of our expert advisors.</p>
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

const teamMembers = [
  {
    name: 'Kyle Whittaker',
    role: 'Founder & Lead Agent',
    initials: 'KW',
    bio: 'With over 15 years in the insurance industry, Kyle founded Whittaker Agency to bring personalized, transparent insurance solutions to Oregon families and businesses. His passion for protecting what matters most drives everything we do.',
    specialties: [
      'Business Insurance',
      'Commercial Property',
      'Risk Management',
      'Strategic Planning'
    ],
    email: 'kyle@whittakeragency.com'
  },
  {
    name: 'Michael Chen',
    role: 'Commercial Insurance Specialist',
    initials: 'MC',
    bio: 'Michael brings 12 years of experience in commercial insurance, helping Oregon businesses protect their operations with comprehensive coverage solutions. He specializes in creating custom packages for diverse industries.',
    specialties: [
      'Commercial Liability',
      'Workers Compensation',
      'Professional Liability',
      'Cyber Insurance'
    ],
    email: 'michael@whittakeragency.com'
  },
  {
    name: 'Jennifer Martinez',
    role: 'Personal Lines Agent',
    initials: 'JM',
    bio: 'Jennifer is passionate about finding the perfect coverage for auto, home, and life insurance needs. With 10 years of experience, she takes pride in building lasting relationships with clients and helping families secure their futures.',
    specialties: [
      'Auto Insurance',
      'Home Insurance',
      'Life Insurance',
      'Umbrella Policies'
    ],
    email: 'jennifer@whittakeragency.com'
  },
  {
    name: 'David Thompson',
    role: 'Claims Specialist',
    initials: 'DT',
    bio: 'With 10 years of experience in claims management, David ensures our clients receive fast, fair settlements when they need it most. His commitment to advocacy and attention to detail makes the claims process as smooth as possible.',
    specialties: [
      'Claims Processing',
      'Loss Assessment',
      'Claims Advocacy',
      'Settlement Negotiation'
    ],
    email: 'david@whittakeragency.com'
  },
  {
    name: 'Emily Rodriguez',
    role: 'Life Insurance Advisor',
    initials: 'ER',
    bio: 'Emily specializes in helping families plan for the future with comprehensive life insurance solutions tailored to their goals. Her empathetic approach and financial expertise help clients make informed decisions about protecting their loved ones.',
    specialties: [
      'Term Life Insurance',
      'Whole Life Insurance',
      'Estate Planning',
      'Financial Protection'
    ],
    email: 'emily@whittakeragency.com'
  },
  {
    name: 'James Anderson',
    role: 'Customer Service Manager',
    initials: 'JA',
    bio: 'James leads our customer service team with a focus on responsiveness, empathy, and going above and beyond for every client. With 8 years in the insurance industry, he ensures that every interaction reflects our commitment to exceptional service.',
    specialties: [
      'Client Relations',
      'Policy Management',
      'Customer Support',
      'Service Excellence'
    ],
    email: 'james@whittakeragency.com'
  }
]
</script>

<style scoped>
.team-page {
  width: 100%;
}

/* Hero Section */
.hero {
  background: linear-gradient(rgba(0, 61, 165, 0.85), rgba(26, 77, 46, 0.85)), url('/images/oregon-stag.jpg');
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
  font-size: 1.2rem;
  opacity: 0.95;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
}

/* Team Introduction */
.team-intro {
  padding: var(--spacing-xl) 0;
  background: white;
}

.intro-text {
  font-size: 1.2rem;
  line-height: 1.8;
  color: #666;
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
}

/* Team Members */
.team-members {
  padding: var(--spacing-xl) 0;
  background: #f8f9fa;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: var(--spacing-xl);
}

.team-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.member-photo {
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, var(--color-primary) 0%, #1a4d2e 100%);
  display: flex;
  justify-content: center;
  align-items: center;
}

.photo-placeholder {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: white;
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.member-info {
  padding: var(--spacing-lg);
}

.member-info h3 {
  color: var(--color-primary);
  font-size: 1.5rem;
  margin-bottom: var(--spacing-xs);
}

.member-role {
  color: #666;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: var(--spacing-md);
}

.member-bio {
  color: #666;
  line-height: 1.7;
  margin-bottom: var(--spacing-md);
}

.member-specialties {
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid #e9ecef;
}

.member-specialties h4 {
  color: var(--color-primary);
  font-size: 1rem;
  margin-bottom: var(--spacing-sm);
}

.member-specialties ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
}

.member-specialties li {
  background: #f8f9fa;
  color: #666;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-size: 0.9rem;
  border: 1px solid #e9ecef;
}

.member-contact {
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid #e9ecef;
}

.contact-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.3s ease;
}

.contact-link:hover {
  color: #1a4d2e;
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

  .intro-text {
    font-size: 1rem;
  }

  .team-grid {
    grid-template-columns: 1fr;
  }

  .photo-placeholder {
    width: 120px;
    height: 120px;
    font-size: 2.5rem;
  }

  .member-info h3 {
    font-size: 1.3rem;
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
