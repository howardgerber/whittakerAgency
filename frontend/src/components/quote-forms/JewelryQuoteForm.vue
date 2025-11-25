<template>
  <div class="jewelry-quote-form">
    <h3>Jewelry Insurance Details</h3>

    <!-- Zip Code Section -->
    <div class="form-group">
      <label for="wearer-zipcode">Enter the Zip/Postal Code of the Jewelry Wearer *</label>
      <input
        type="text"
        id="wearer-zipcode"
        v-model="wearerZipCode"
        required
        maxlength="10"
        class="form-control zipcode-input"
        placeholder="e.g., 97330"
        @input="updateFormData"
      />
    </div>

    <p class="form-instructions">Add each jewelry item you'd like to insure with its estimated replacement value.</p>

    <!-- Jewelry Items Grid -->
    <div class="jewelry-items-grid">
      <div class="grid-header">
        <div class="header-type">Type *</div>
        <div class="header-value">Value *</div>
        <div class="header-description">Description (Optional)</div>
        <div class="header-actions"></div>
      </div>

      <div v-for="(item, index) in jewelryItems" :key="item.id" class="jewelry-item-row">
        <div class="item-type">
          <select
            v-model="item.type"
            required
            class="form-control"
            @change="updateFormData"
          >
            <option value="">Select Type</option>
            <option value="ring">Ring</option>
            <option value="earrings">Earrings</option>
            <option value="bracelet">Bracelet</option>
            <option value="necklace">Necklace</option>
            <option value="watch">Watch</option>
            <option value="pendant">Pendant</option>
            <option value="chain">Chain</option>
            <option value="loose_stone">Loose Stone</option>
            <option value="brooch">Brooch</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div class="item-value">
          <input
            type="text"
            :value="item.displayValue"
            @input="handleValueInput($event, index)"
            required
            class="form-control"
            placeholder="$5,000"
          />
        </div>

        <div class="item-description">
          <input
            type="text"
            v-model="item.description"
            class="form-control"
            placeholder="e.g., 14K gold with diamond"
            @input="updateFormData"
          />
        </div>

        <div class="item-actions">
          <button
            type="button"
            @click="removeItem(index)"
            class="btn-remove"
            :disabled="jewelryItems.length === 1"
            title="Remove item"
          >
            ✕
          </button>
        </div>
      </div>
    </div>

    <button type="button" @click="addItem" class="btn-add-item">
      + Add Another Item
    </button>

    <div class="total-coverage">
      <strong>Total Coverage Amount:</strong>
      <span class="total-amount">{{ formatCurrency(totalCoverageAmount) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { formatCurrency } from '@/utils/formatters'

const emit = defineEmits<{
  (e: 'update', data: any): void
  (e: 'valid', isValid: boolean): void
  (e: 'blur', fieldName: string): void
}>()

interface JewelryItem {
  id: number
  type: string
  value: string  // stored as string number (e.g., "5000")
  displayValue: string  // formatted display (e.g., "$5,000")
  description: string
}

const wearerZipCode = ref('')
let nextId = 1

// Initialize with one empty item
const jewelryItems = ref<JewelryItem[]>([
  {
    id: nextId++,
    type: '',
    value: '',
    displayValue: '',
    description: ''
  }
])

// Calculate total coverage amount
const totalCoverageAmount = computed(() => {
  return jewelryItems.value.reduce((total, item) => {
    const value = item.value ? parseInt(item.value, 10) : 0
    return total + value
  }, 0).toString()
})

// Add a new jewelry item
const addItem = () => {
  jewelryItems.value.push({
    id: nextId++,
    type: '',
    value: '',
    displayValue: '',
    description: ''
  })
}

// Remove a jewelry item
const removeItem = (index: number) => {
  if (jewelryItems.value.length > 1) {
    jewelryItems.value.splice(index, 1)
    updateFormData()
  }
}

// Handle value input with currency formatting
const handleValueInput = (event: Event, index: number) => {
  const input = event.target as HTMLInputElement
  const rawValue = input.value.replace(/[^0-9]/g, '')

  if (rawValue === '') {
    jewelryItems.value[index].value = ''
    jewelryItems.value[index].displayValue = ''
  } else {
    jewelryItems.value[index].value = rawValue
    jewelryItems.value[index].displayValue = formatCurrency(rawValue)
  }
  updateFormData()
}

// Update form data and emit
const updateFormData = () => {
  const formData = {
    wearer_zipcode: wearerZipCode.value,
    jewelry_items: jewelryItems.value.map(item => ({
      type: item.type,
      value: item.value,
      description: item.description
    })),
    total_coverage: totalCoverageAmount.value
  }

  emit('update', formData)

  // Validate: zip code required and at least one item with type and value
  const hasValidItem = jewelryItems.value.some(item => item.type && item.value)
  const isValid = !!(wearerZipCode.value.trim() && hasValidItem)

  emit('valid', isValid)
}

// Watch for changes
watch([wearerZipCode, jewelryItems], () => {
  updateFormData()
}, { deep: true })
</script>

<style scoped>
.jewelry-quote-form {
  width: 100%;
}

h3 {
  color: var(--color-primary);
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
}

.form-instructions {
  color: #666;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: var(--color-primary);
}

.zipcode-input {
  max-width: 200px;
}

textarea.form-control {
  resize: vertical;
  font-family: inherit;
}

select.form-control {
  cursor: pointer;
}

/* Grid Layout */
.jewelry-items-grid {
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.grid-header {
  display: grid;
  grid-template-columns: 200px 150px 1fr 50px;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border-bottom: 2px solid #ddd;
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.jewelry-item-row {
  display: grid;
  grid-template-columns: 200px 150px 1fr 50px;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  align-items: center;
}

.jewelry-item-row:last-child {
  border-bottom: none;
}

.item-type,
.item-value,
.item-description {
  display: flex;
  align-items: center;
}

.item-actions {
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-remove {
  width: 32px;
  height: 32px;
  border: 1px solid #dc3545;
  background: white;
  color: #dc3545;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-remove:hover:not(:disabled) {
  background: #dc3545;
  color: white;
}

.btn-remove:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.btn-add-item {
  padding: 0.75rem 1.5rem;
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.btn-add-item:hover {
  background: var(--color-primary);
  color: white;
}

.total-coverage {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ddd;
}

.total-coverage strong {
  color: #333;
  font-size: 1.1rem;
}

.total-amount {
  color: var(--color-primary);
  font-size: 1.5rem;
  font-weight: 700;
}

@media (max-width: 968px) {
  .grid-header,
  .jewelry-item-row {
    grid-template-columns: 150px 120px 1fr 50px;
    gap: 0.5rem;
    padding: 0.75rem;
  }

  .grid-header {
    font-size: 0.85rem;
  }

  .form-control {
    font-size: 0.9rem;
    padding: 0.5rem;
  }
}

@media (max-width: 768px) {
  .grid-header {
    display: none;
  }

  .jewelry-item-row {
    grid-template-columns: 1fr;
    gap: 0.75rem;
    padding: 1rem;
    position: relative;
  }

  .item-actions {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
  }

  .total-coverage {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }

  .zipcode-input {
    max-width: 100%;
  }
}
</style>
