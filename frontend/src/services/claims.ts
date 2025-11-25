import api from './api'

export interface ClaimData {
  [key: string]: any
}

export interface ClaimRequest {
  category: string
  subcategory: string | null
  incident_date: string
  incident_summary: string
  claim_data: ClaimData
  appointment_requested?: string | null
  contact_preference: string
  preferred_contact_time?: string | null
  additional_notes?: string | null
}

export interface ClaimResponse {
  id: number
  user_id: number
  category: string
  subcategory: string | null
  incident_date: string
  incident_summary: string
  claim_data: ClaimData
  appointment_requested: string | null
  contact_preference: string
  preferred_contact_time: string | null
  additional_notes: string | null
  status: 'submitted' | 'contacted' | 'closed'
  contacted_at: string | null
  created_at: string
  updated_at: string
}

export default {
  // Create a new claim
  async createClaim(claimData: ClaimRequest): Promise<ClaimResponse> {
    const response = await api.post('/claims/', claimData)
    return response.data
  },

  // Get all claims for the current user
  async getMyClaims(category?: string, status?: string): Promise<ClaimResponse[]> {
    const params: Record<string, string> = {}
    if (category) params.category = category
    if (status) params.status = status

    const response = await api.get('/claims/my-claims', { params })
    return response.data
  },

  // Get a specific claim by ID
  async getClaim(claimId: number): Promise<ClaimResponse> {
    const response = await api.get(`/claims/${claimId}`)
    return response.data
  },

  // Cancel/delete a claim
  async cancelClaim(claimId: number): Promise<void> {
    await api.delete(`/claims/${claimId}`)
  }
}
