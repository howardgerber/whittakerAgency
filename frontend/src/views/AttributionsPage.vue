<template>
  <div class="attributions-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <h1>Attributions & Credits</h1>
        <p class="subtitle">Acknowledging the creators and resources that make our site possible</p>
      </div>
    </section>

    <!-- Attributions Content -->
    <section class="attributions-content">
      <div class="container">
        <div class="intro">
          <p>
            We believe in supporting the creative community. Below are the icons, images, and resources
            we use on our website, along with credit to their talented creators.
          </p>
        </div>

        <div class="attribution-section">
          <h2>Icons</h2>
          <div class="attribution-card">
            <div class="attribution-item">
              <h3>Snowmobile Icon</h3>
              <p class="creator">Created by Smashicons</p>
              <p class="source">Source: <a href="https://www.flaticon.com/free-icons/snowmobile" target="_blank" rel="noopener noreferrer">Flaticon</a></p>
              <p class="license">License: Flaticon Free License</p>
            </div>

            <div class="attribution-item">
              <h3>ATV Icon</h3>
              <p class="creator">Created by Andy Horvath</p>
              <p class="source">Source: <a href="https://www.flaticon.com/free-icons/atv" target="_blank" rel="noopener noreferrer">Flaticon</a></p>
              <p class="license">License: Flaticon Free License</p>
            </div>

            <div class="attribution-item">
              <h3>Earthquake Icon</h3>
              <p class="creator">Created by kerismaker</p>
              <p class="source">Source: <a href="https://www.flaticon.com/free-icons/earthquake" target="_blank" rel="noopener noreferrer">Flaticon</a></p>
              <p class="license">License: Flaticon Free License</p>
            </div>

            <div class="attribution-item">
              <h3>Oregon Icon</h3>
              <p class="creator">Created by JunGSa</p>
              <p class="source">Source: <a href="https://www.flaticon.com/free-icons/oregon" target="_blank" rel="noopener noreferrer">Flaticon</a></p>
              <p class="license">License: Flaticon Free License</p>
            </div>

            <div class="attribution-item">
              <h3>Contact Icon</h3>
              <p class="creator">Created by Prashanth Rapolu 15</p>
              <p class="source">Source: <a href="https://www.flaticon.com/free-icons/contact" target="_blank" rel="noopener noreferrer">Flaticon</a></p>
              <p class="license">License: Flaticon Free License</p>
            </div>

            <div class="attribution-item">
              <h3>Claim Icon</h3>
              <p class="creator">Created by kmg design</p>
              <p class="source">Source: <a href="https://www.flaticon.com/free-icons/claim" target="_blank" rel="noopener noreferrer">Flaticon</a></p>
              <p class="license">License: Flaticon Free License</p>
            </div>

            <div class="attribution-item">
              <h3>Quote Icon</h3>
              <p class="creator">Created by Awicon</p>
              <p class="source">Source: <a href="https://www.flaticon.com/free-icons/price-list" target="_blank" rel="noopener noreferrer">Flaticon</a></p>
              <p class="license">License: Flaticon Free License</p>
            </div>

            <div class="attribution-item">
              <h3>User Icon</h3>
              <p class="creator">Created by Nuricon</p>
              <p class="source">Source: <a href="https://www.flaticon.com/free-icons/my-profile" target="_blank" rel="noopener noreferrer">Flaticon</a></p>
              <p class="license">License: Flaticon Free License</p>
            </div>

          </div>
        </div>

        <div class="attribution-section">
          <h2>Images</h2>
          <div class="attribution-card">
            <div class="attribution-item">
              <h3>Portland Stag Sign</h3>
              <p class="creator">Credit: George Fox Evangelical Seminary</p>
              <p class="source">Source: <a href="https://commons.wikimedia.org/wiki/File:White_Stag_sign,_Portland,_Oregon.jpg" target="_blank" rel="noopener noreferrer">Wikimedia Commons</a></p>
              <p class="license">License: <a href="https://creativecommons.org/licenses/by-sa/2.0/" target="_blank" rel="noopener noreferrer">CC BY-SA 2.0</a> • No changes made</p>
            </div>
          </div>
        </div>

        <div class="attribution-section">
          <h2>Open Source Software</h2>
          <div class="attribution-card">
            <div class="attribution-item">
              <h3>Vue.js</h3>
              <p class="description">The Progressive JavaScript Framework</p>
              <p class="source">Source: <a href="https://vuejs.org" target="_blank" rel="noopener noreferrer">vuejs.org</a></p>
              <p class="license">License: MIT License</p>
            </div>

            <div class="attribution-item">
              <h3>Vite</h3>
              <p class="description">Next Generation Frontend Tooling</p>
              <p class="source">Source: <a href="https://vitejs.dev" target="_blank" rel="noopener noreferrer">vitejs.dev</a></p>
              <p class="license">License: MIT License</p>
            </div>
          </div>
        </div>

        <div class="note">
          <p>
            If you believe any content on this site infringes on your copyright or requires additional
            attribution, please <RouterLink to="/about">contact us</RouterLink> and we'll address it promptly.
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.attributions-page {
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

/* Content Section */
.attributions-content {
  padding: var(--spacing-xl) 0;
  background: #f8f9fa;
}

.intro {
  background: white;
  padding: var(--spacing-lg);
  border-radius: 8px;
  margin-bottom: var(--spacing-xl);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.intro p {
  font-size: 1.1rem;
  line-height: 1.7;
  color: #666;
  margin: 0;
}

/* Attribution Sections */
.attribution-section {
  margin-bottom: var(--spacing-xl);
}

.attribution-section h2 {
  color: var(--color-primary);
  font-size: 1.8rem;
  margin-bottom: var(--spacing-md);
}

.attribution-card {
  background: white;
  padding: var(--spacing-lg);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.attribution-item {
  padding: var(--spacing-md);
  border-left: 4px solid var(--color-primary);
  background: #f8f9fa;
  border-radius: 4px;
  margin-bottom: var(--spacing-md);
}

.attribution-item:last-child {
  margin-bottom: 0;
}

.attribution-item h3 {
  color: var(--color-primary);
  font-size: 1.3rem;
  margin-bottom: var(--spacing-sm);
}

.attribution-item p {
  color: #666;
  margin-bottom: var(--spacing-xs);
  line-height: 1.6;
}

.attribution-item p:last-child {
  margin-bottom: 0;
}

.creator {
  font-weight: 600;
  color: #444;
}

.source a,
.description {
  color: #666;
}

.source a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.3s ease;
}

.source a:hover {
  color: #1a4d2e;
  text-decoration: underline;
}

.license {
  font-size: 0.95rem;
  font-style: italic;
  color: #888;
}

/* Note Section */
.note {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: var(--spacing-md);
  border-radius: 4px;
  margin-top: var(--spacing-xl);
}

.note p {
  color: #856404;
  margin: 0;
  line-height: 1.6;
}

.note a {
  color: #856404;
  font-weight: 600;
  text-decoration: underline;
}

.note a:hover {
  color: #533f03;
}

/* Responsive */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 1.8rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .attribution-section h2 {
    font-size: 1.5rem;
  }

  .attribution-item h3 {
    font-size: 1.1rem;
  }
}
</style>
