/**
 * Input formatters for consistent data formatting across forms
 */

/**
 * Format phone number as XXX.XXX.XXXX
 * Auto-inserts dots, handles backspace intelligently
 */
export function formatPhoneNumber(value: string, _previousValue: string = ''): string {
  // Remove all non-digits
  const digitsOnly = value.replace(/\D/g, '')

  // Limit to 10 digits
  const limitedDigits = digitsOnly.substring(0, 10)

  // Build formatted string
  let formatted = ''

  for (let i = 0; i < limitedDigits.length; i++) {
    // Add dot after 3rd digit
    if (i === 3) {
      formatted += '.'
    }
    // Add dot after 6th digit
    if (i === 6) {
      formatted += '.'
    }
    formatted += limitedDigits[i]
  }

  return formatted
}

/**
 * Handle backspace for phone number
 * If cursor is right after a dot, delete the dot and the previous digit
 */
export function handlePhoneBackspace(event: KeyboardEvent, currentValue: string, cursorPosition: number): string {
  if (event.key !== 'Backspace') {
    return currentValue
  }

  // If we're right after a dot (positions 4 or 8), remove both the dot and the previous digit
  if (cursorPosition === 4 || cursorPosition === 8) {
    event.preventDefault()
    // Remove the digit before the dot
    return currentValue.substring(0, cursorPosition - 2) + currentValue.substring(cursorPosition)
  }

  return currentValue
}

/**
 * Sanitize input to only allow specific characters
 */
export function sanitizeInput(value: string, allowedPattern: RegExp): string {
  return value.replace(new RegExp(`[^${allowedPattern.source}]`, 'g'), '')
}

/**
 * Format email (trim, lowercase)
 */
export function formatEmail(value: string): string {
  return value.trim().toLowerCase()
}

/**
 * Format VIN (uppercase, remove invalid chars, limit to 17)
 * VINs don't use I, O, or Q to avoid confusion with 1, 0
 */
export function formatVIN(value: string): string {
  // Remove spaces and special characters, keep only valid VIN characters
  const cleaned = value.toUpperCase().replace(/[^A-HJ-NPR-Z0-9]/g, '')

  // Limit to 17 characters
  return cleaned.substring(0, 17)
}

/**
 * Format vehicle year (numbers only, limit to 4 digits)
 */
export function formatYear(value: string): string {
  // Remove all non-digits
  const digitsOnly = value.replace(/\D/g, '')

  // Limit to 4 digits
  return digitsOnly.substring(0, 4)
}

/**
 * Format vehicle text (make/model) - capitalize first letter of each word
 */
export function formatVehicleText(value: string): string {
  // Remove invalid characters (keep letters, numbers, spaces, dashes, parentheses)
  const cleaned = value.replace(/[^a-zA-Z0-9\s\-()]/g, '')

  // Limit to 50 characters
  return cleaned.substring(0, 50)
}

/**
 * Capitalize first letter of each word
 */
export function capitalizeWords(value: string): string {
  return value
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

/**
 * Universal text formatting function - capitalizes each word (splits by underscore or space)
 * Use this for statuses, categories, types, actions, and any text needing capitalization
 * Example: "pending_review" → "Pending Review"
 * Example: "submitted" → "Submitted"
 * Example: "pending review" → "Pending Review"
 * Example: "quote" → "Quote"
 */
export function formatText(text: string): string {
  if (!text) return ''
  return text
    .split(/[_\s]+/)  // Split by underscores OR spaces
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

/**
 * Trim and clean text input
 */
export function cleanText(value: string): string {
  return value.trim().replace(/\s+/g, ' ')
}

/**
 * Format number with thousands separator (commas)
 * Example: 2000 → 2,000
 */
export function formatNumberWithCommas(value: string): string {
  // Remove all non-digits
  const digitsOnly = value.replace(/\D/g, '')

  if (!digitsOnly) return ''

  // Convert to number and format with commas
  const number = parseInt(digitsOnly, 10)
  return number.toLocaleString('en-US')
}

/**
 * Parse formatted number back to raw number
 * Example: 2,000 → 2000
 */
export function parseFormattedNumber(value: string): number | null {
  const digitsOnly = value.replace(/\D/g, '')
  return digitsOnly ? parseInt(digitsOnly, 10) : null
}

/**
 * Format currency with dollar sign and commas
 * Example: 750000 → $750,000
 */
export function formatCurrency(value: string): string {
  // Remove all non-digits
  const digitsOnly = value.replace(/\D/g, '')

  if (!digitsOnly) return ''

  // Convert to number and format with commas
  const number = parseInt(digitsOnly, 10)
  return '$' + number.toLocaleString('en-US')
}

/**
 * Parse formatted currency back to raw number
 * Example: $750,000 → 750000
 */
export function parseFormattedCurrency(value: string): number | null {
  const digitsOnly = value.replace(/\D/g, '')
  return digitsOnly ? parseInt(digitsOnly, 10) : null
}

/**
 * Format datetime to user's local timezone with timezone abbreviation
 * Backend sends UTC timestamps (without Z indicator), this converts to user's local time
 * Example: "2025-11-20 17:31:00" (UTC) → "November 20, 2025 at 9:31 AM PST"
 */
export function formatDateTime(dateString: string | null | undefined): string {
  if (!dateString) return 'N/A'

  // Backend sends UTC time without 'Z' indicator, so we need to add it
  // This tells JavaScript to treat it as UTC, not local time
  let utcString = dateString
  if (!dateString.endsWith('Z') && !dateString.includes('+')) {
    // Replace space with 'T' and add 'Z' for UTC
    utcString = dateString.replace(' ', 'T') + 'Z'
  }

  const date = new Date(utcString)

  // Format date and time
  const formatted = date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })

  // Get timezone abbreviation (e.g., "PST", "PDT", "EST")
  const timeZone = date.toLocaleDateString('en-US', {
    day: '2-digit',
    timeZoneName: 'short'
  }).split(', ')[1]

  return `${formatted} ${timeZone}`
}

/**
 * Format date only (no time) to user's local timezone
 * Example: "2025-11-20" → "November 20, 2025"
 */
export function formatDate(dateString: string | null | undefined): string {
  if (!dateString) return 'N/A'

  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

/**
 * Format date to short format
 * Example: "2025-11-20" → "11/20/2025"
 */
export function formatDateShort(dateString: string | null | undefined): string {
  if (!dateString) return 'N/A'

  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

/**
 * Format relative time (e.g., "2 hours ago", "3 days ago")
 */
export function formatRelativeTime(dateString: string | null | undefined): string {
  if (!dateString) return 'N/A'

  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffSec = Math.floor(diffMs / 1000)
  const diffMin = Math.floor(diffSec / 60)
  const diffHour = Math.floor(diffMin / 60)
  const diffDay = Math.floor(diffHour / 24)

  if (diffSec < 60) return 'Just now'
  if (diffMin < 60) return `${diffMin} minute${diffMin !== 1 ? 's' : ''} ago`
  if (diffHour < 24) return `${diffHour} hour${diffHour !== 1 ? 's' : ''} ago`
  if (diffDay < 30) return `${diffDay} day${diffDay !== 1 ? 's' : ''} ago`

  return formatDate(dateString)
}
