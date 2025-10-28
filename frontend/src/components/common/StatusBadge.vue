<template>
  <span :class="['status-badge', `status-${status}`]">
    {{ formatText(status) }}
  </span>
</template>

<script setup lang="ts">
import { formatText } from '@/utils/formatters'

defineProps<{
  status: string
}>()
</script>

<style scoped>
/* Unified status color scheme:
   - Red/Pink: Initial submission (new, pending, submitted)
   - Tan/Yellow: Agency working on it (read, in_review)
   - Green: Agency completed, ball in customer's court (responded, contacted, quoted)
   - Blue: Customer took action (accepted)
   - Gray: Closed/Final states (closed, declined)
*/

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  display: inline-block;
}

/* Message statuses */
.status-new {
  background: #F8D7DA;
  color: #721C24;
}

.status-read {
  background: #FFF3CD;
  color: #856404;
}

.status-responded {
  background: #D4EDDA;
  color: #155724;
}

/* Claim statuses */
.status-submitted {
  background: #F8D7DA;
  color: #721C24;
}

.status-contacted {
  background: #D4EDDA;
  color: #155724;
}

/* Quote statuses */
.status-pending {
  background: #F8D7DA;
  color: #721C24;
}

.status-in_review {
  background: #FFF3CD;
  color: #856404;
}

.status-quoted {
  background: #D4EDDA;
  color: #155724;
}

.status-accepted {
  background: #CCE5FF;
  color: #004085;
}

.status-declined {
  background: #E2E3E5;
  color: #383D41;
}

/* Universal closed status */
.status-closed {
  background: #E2E3E5;
  color: #383D41;
}
</style>
