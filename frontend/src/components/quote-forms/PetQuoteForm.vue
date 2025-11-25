<template>
  <div class="pet-quote-form">
    <h3>Pet Insurance Details</h3>

    <div class="form-row">
      <div class="form-group">
        <label for="pet-name">Pet's Name *</label>
        <input
          type="text"
          id="pet-name"
          v-model="formData.pet_name"
          required
          class="form-control"
          placeholder="e.g., Max"
        />
      </div>

      <div class="form-group">
        <label for="pet-breed">Pet's Breed *</label>
        <input
          type="text"
          id="pet-breed"
          v-model="formData.pet_breed"
          required
          class="form-control"
          placeholder="e.g., Golden Retriever"
        />
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="pet-age">Pet's Age *</label>
        <select id="pet-age" v-model="formData.pet_age" required class="form-control">
          <option value="">Select Age</option>
          <option value="0-1">Less than 1 year</option>
          <option value="1-2">1-2 years</option>
          <option value="3-5">3-5 years</option>
          <option value="6-8">6-8 years</option>
          <option value="9-12">9-12 years</option>
          <option value="13+">13+ years</option>
        </select>
      </div>

      <div class="form-group">
        <label class="section-label">Pet Type *</label>
        <div class="toggle-group">
          <button
            type="button"
            :class="['toggle-button', { active: formData.pet_type === 'dog' }]"
            @click="formData.pet_type = 'dog'"
          >
            <span class="checkmark" v-if="formData.pet_type === 'dog'">✓</span>
            Dog
          </button>
          <button
            type="button"
            :class="['toggle-button', { active: formData.pet_type === 'cat' }]"
            @click="formData.pet_type = 'cat'"
          >
            <span class="checkmark" v-if="formData.pet_type === 'cat'">✓</span>
            Cat
          </button>
        </div>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label class="section-label">Pet's Gender *</label>
        <div class="toggle-group">
          <button
            type="button"
            :class="['toggle-button', { active: formData.pet_gender === 'male' }]"
            @click="formData.pet_gender = 'male'"
          >
            <span class="checkmark" v-if="formData.pet_gender === 'male'">✓</span>
            Male
          </button>
          <button
            type="button"
            :class="['toggle-button', { active: formData.pet_gender === 'female' }]"
            @click="formData.pet_gender = 'female'"
          >
            <span class="checkmark" v-if="formData.pet_gender === 'female'">✓</span>
            Female
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="pet-spayed">Spayed/Neutered</label>
        <select id="pet-spayed" v-model="formData.spayed_neutered" class="form-control">
          <option value="">Select</option>
          <option value="yes">Yes</option>
          <option value="no">No</option>
          <option value="unknown">Unknown</option>
        </select>
      </div>
    </div>

    <div class="form-group">
      <label for="pet-preexisting">Pre-existing Conditions (if any)</label>
      <textarea
        id="pet-preexisting"
        v-model="formData.preexisting_conditions"
        rows="3"
        maxlength="250"
        class="form-control"
        placeholder="List any known health conditions or concerns..."
      ></textarea>
      <small class="help-text">{{ formData.preexisting_conditions.length }}/250 characters</small>
    </div>

    <div class="form-group">
      <label for="pet-coverage">Desired Coverage Type</label>
      <select id="pet-coverage" v-model="formData.coverage_type" class="form-control">
        <option value="">Select Coverage Type</option>
        <option value="accident_only">Accident Only</option>
        <option value="accident_illness">Accident & Illness</option>
        <option value="comprehensive">Comprehensive (includes wellness)</option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'

const emit = defineEmits<{
  (e: 'update', data: any): void
  (e: 'valid', isValid: boolean): void
  (e: 'blur', fieldName: string): void
}>()

const formData = reactive({
  pet_name: '',
  pet_breed: '',
  pet_age: '',
  pet_type: '',
  pet_gender: '',
  spayed_neutered: '',
  preexisting_conditions: '',
  coverage_type: ''
})

// Watch for form changes
watch(formData, () => {
  emit('update', { ...formData })

  // Validate form
  const isValid = !!(
    formData.pet_name.trim() &&
    formData.pet_breed.trim() &&
    formData.pet_age &&
    formData.pet_type &&
    formData.pet_gender
  )

  emit('valid', isValid)
}, { deep: true })
</script>

<style scoped>
.pet-quote-form {
  width: 100%;
}

h3 {
  color: var(--color-primary);
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.section-label {
  font-size: 1rem;
  margin-bottom: 0.75rem;
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

textarea.form-control {
  resize: vertical;
  font-family: inherit;
}

.help-text {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #666;
  font-weight: normal;
}

select.form-control {
  cursor: pointer;
}

.toggle-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.toggle-button {
  padding: 0.75rem 1rem;
  border: none;
  background: white;
  color: #333;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  border-right: 1px solid #ddd;
}

.toggle-button:last-child {
  border-right: none;
}

.toggle-button:hover {
  background: #f5f5f5;
}

.toggle-button.active {
  background: var(--color-primary);
  color: white;
  font-weight: 600;
}

.toggle-button .checkmark {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  color: var(--color-primary);
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 700;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
