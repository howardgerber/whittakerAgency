/**
 * Centralized validation rules for all forms
 */

export interface ValidationRule {
  validate: (value: string) => boolean
  message: string
}

export interface ValidationResult {
  isValid: boolean
  errors: string[]
}

/**
 * Validation Rules
 */
export const ValidationRules = {
  // Username: 3-50 chars, lowercase, alphanumeric + underscore/dash, must start with letter
  username: {
    required: true,
    minLength: 3,
    maxLength: 50,
    validate(value: string): ValidationResult {
      const errors: string[] = []

      if (!value || value.trim().length === 0) {
        errors.push('Username is required')
        return { isValid: false, errors }
      }

      // Force lowercase
      const lowerValue = value.toLowerCase()
      if (value !== lowerValue) {
        errors.push('Username must be lowercase')
      }

      if (value.length < this.minLength) {
        errors.push(`Username must be at least ${this.minLength} characters`)
      }

      if (value.length > this.maxLength) {
        errors.push(`Username must be ${this.maxLength} characters or less`)
      }

      // Must start with a letter
      if (!/^[a-z]/.test(lowerValue)) {
        errors.push('Username must start with a letter')
      }

      // Can only contain lowercase letters, numbers, underscores, and dashes
      if (!/^[a-z][a-z0-9_-]*$/.test(lowerValue)) {
        errors.push('Username can only contain lowercase letters, numbers, underscores, and dashes')
      }

      return { isValid: errors.length === 0, errors }
    }
  },

  // Full Name: At least 2 words (first + last), max 200 chars
  fullName: {
    required: true,
    minLength: 3,
    maxLength: 200,
    validate(value: string): ValidationResult {
      const errors: string[] = []

      if (!value || value.trim().length === 0) {
        errors.push('Full name is required')
        return { isValid: false, errors }
      }

      if (value.length > this.maxLength) {
        errors.push(`Full name must be ${this.maxLength} characters or less`)
      }

      // Must have at least 2 words (first and last name)
      const words = value.trim().split(/\s+/)
      if (words.length < 2) {
        errors.push('Please enter both first and last name')
      }

      // Each word should have at least 1 letter
      const allWordsValid = words.every(word => /[a-zA-Z]/.test(word))
      if (!allWordsValid) {
        errors.push('Name must contain letters')
      }

      return { isValid: errors.length === 0, errors }
    }
  },

  // Email: Standard email format, max 254 chars (RFC 5321 standard)
  email: {
    required: true,
    maxLength: 254,
    validate(value: string): ValidationResult {
      const errors: string[] = []

      if (!value || value.trim().length === 0) {
        errors.push('Email is required')
        return { isValid: false, errors }
      }

      if (value.length > this.maxLength) {
        errors.push(`Email must be ${this.maxLength} characters or less`)
      }

      // Email regex pattern
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailPattern.test(value)) {
        errors.push('Please enter a valid email address')
      }

      return { isValid: errors.length === 0, errors }
    }
  },

  // Phone: Optional, but if provided must be XXX.XXX.XXXX format
  phone: {
    required: false,
    validate(value: string): ValidationResult {
      const errors: string[] = []

      // If empty and optional, it's valid
      if (!value || value.trim().length === 0) {
        return { isValid: true, errors: [] }
      }

      // Must match XXX.XXX.XXXX format (12 chars including dots)
      const phonePattern = /^\d{3}\.\d{3}\.\d{4}$/
      if (!phonePattern.test(value)) {
        errors.push('Phone must be in format XXX.XXX.XXXX')
      }

      return { isValid: errors.length === 0, errors }
    }
  },

  // Password: 8-100 chars, require complexity
  password: {
    required: true,
    minLength: 8,
    maxLength: 100,
    validate(value: string): ValidationResult {
      const errors: string[] = []

      if (!value || value.length === 0) {
        errors.push('Password is required')
        return { isValid: false, errors }
      }

      if (value.length < this.minLength) {
        errors.push(`Password must be at least ${this.minLength} characters`)
      }

      if (value.length > this.maxLength) {
        errors.push(`Password must be ${this.maxLength} characters or less`)
      }

      // Require at least one uppercase, one lowercase, one number
      if (!/[A-Z]/.test(value)) {
        errors.push('Password must contain at least one uppercase letter')
      }

      if (!/[a-z]/.test(value)) {
        errors.push('Password must contain at least one lowercase letter')
      }

      if (!/[0-9]/.test(value)) {
        errors.push('Password must contain at least one number')
      }

      return { isValid: errors.length === 0, errors }
    }
  },

  // VIN: Optional, but if provided must be exactly 17 alphanumeric characters
  vin: {
    required: false,
    length: 17,
    validate(value: string): ValidationResult {
      const errors: string[] = []

      // If empty and optional, it's valid
      if (!value || value.trim().length === 0) {
        return { isValid: true, errors: [] }
      }

      // Must be exactly 17 characters
      if (value.length !== this.length) {
        errors.push(`VIN must be exactly ${this.length} characters`)
      }

      // Must be alphanumeric only (no spaces, special chars)
      if (!/^[A-HJ-NPR-Z0-9]{17}$/i.test(value)) {
        errors.push('VIN must contain only letters and numbers (no I, O, or Q)')
      }

      return { isValid: errors.length === 0, errors }
    }
  },

  // Vehicle Year: 1900 to current year + 1
  vehicleYear: {
    required: true,
    minYear: 1900,
    maxYear: new Date().getFullYear() + 1,
    validate(value: string | number): ValidationResult {
      const errors: string[] = []
      const year = typeof value === 'string' ? parseInt(value, 10) : value

      if (!value || isNaN(year)) {
        errors.push('Year is required')
        return { isValid: false, errors }
      }

      if (year < this.minYear) {
        errors.push(`Year must be ${this.minYear} or later`)
      }

      if (year > this.maxYear) {
        errors.push(`Year cannot be later than ${this.maxYear}`)
      }

      return { isValid: errors.length === 0, errors }
    }
  },

  // Vehicle Make/Model: 1-50 chars, letters/numbers/spaces/dashes
  vehicleText: {
    required: true,
    minLength: 1,
    maxLength: 50,
    validate(value: string): ValidationResult {
      const errors: string[] = []

      if (!value || value.trim().length === 0) {
        errors.push('This field is required')
        return { isValid: false, errors }
      }

      if (value.length > this.maxLength) {
        errors.push(`Must be ${this.maxLength} characters or less`)
      }

      // Allow letters, numbers, spaces, dashes, parentheses
      if (!/^[a-zA-Z0-9\s\-()]+$/.test(value)) {
        errors.push('Only letters, numbers, spaces, dashes, and parentheses allowed')
      }

      return { isValid: errors.length === 0, errors }
    }
  },

  // Text Area: Optional, max length
  textArea: {
    required: false,
    maxLength: 1000,
    validate(value: string): ValidationResult {
      const errors: string[] = []

      // If empty and optional, it's valid
      if (!value || value.trim().length === 0) {
        return { isValid: true, errors: [] }
      }

      if (value.length > this.maxLength) {
        errors.push(`Must be ${this.maxLength} characters or less`)
      }

      return { isValid: errors.length === 0, errors }
    }
  },

  // Generic required text field
  requiredText: {
    required: true,
    minLength: 1,
    maxLength: 200,
    validate(value: string): ValidationResult {
      const errors: string[] = []

      if (!value || value.trim().length === 0) {
        errors.push('This field is required')
        return { isValid: false, errors }
      }

      if (value.length > this.maxLength) {
        errors.push(`Must be ${this.maxLength} characters or less`)
      }

      return { isValid: errors.length === 0, errors }
    }
  },

  // Incident date: Required, cannot be future, cannot be more than 2 years in past
  incidentDate: {
    required: true,
    maxYearsInPast: 2,
    validate(value: string): ValidationResult {
      const errors: string[] = []

      if (!value || value.trim().length === 0) {
        errors.push('Incident date is required')
        return { isValid: false, errors }
      }

      const inputDate = new Date(value)
      const today = new Date()
      today.setHours(0, 0, 0, 0)

      // Check if date is in the future
      if (inputDate > today) {
        errors.push('Incident date cannot be in the future')
      }

      // Check if date is more than 2 years in the past
      const twoYearsAgo = new Date(today.getFullYear() - this.maxYearsInPast, today.getMonth(), today.getDate())
      if (inputDate < twoYearsAgo) {
        errors.push(`Incident date cannot be more than ${this.maxYearsInPast} years ago`)
      }

      return { isValid: errors.length === 0, errors }
    }
  }
}

/**
 * Helper function to validate a field
 */
export function validateField(fieldName: keyof typeof ValidationRules, value: string): ValidationResult {
  const rule = ValidationRules[fieldName]
  if (!rule) {
    return { isValid: true, errors: [] }
  }

  return rule.validate(value)
}

/**
 * Check if all required fields in a form are valid
 */
export function isFormValid(fields: Record<string, string>, requiredFields: string[]): boolean {
  for (const fieldName of requiredFields) {
    const value = fields[fieldName] || ''
    const result = validateField(fieldName as keyof typeof ValidationRules, value)

    if (!result.isValid) {
      return false
    }
  }

  return true
}

/**
 * Get character count status for display
 * Returns class name for styling based on how close to limit
 */
export function getCharacterCountClass(currentLength: number, maxLength: number): string {
  const percentage = (currentLength / maxLength) * 100

  if (currentLength >= maxLength) {
    return 'at-limit' // Red
  } else if (percentage >= 90) {
    return 'near-limit' // Orange
  } else {
    return 'normal' // Gray
  }
}
