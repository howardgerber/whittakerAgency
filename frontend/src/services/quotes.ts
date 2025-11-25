import api from './api'

export interface QuoteData {
  [key: string]: any
}

export interface QuoteRequest {
  category: string
  subcategory: string | null
  quote_data: QuoteData
  customer_notes?: string
}

export interface QuoteResponse {
  id: number
  user_id: number
  category: string
  subcategory: string | null
  status: string
  quote_data: QuoteData
  agent_notes?: string
  customer_notes?: string
  quote_amount?: number
  quoted_at?: string
  created_at: string
  updated_at: string
}

export default {
  // Create a new quote request
  async createQuote(quoteData: QuoteRequest): Promise<QuoteResponse> {
    const response = await api.post('/quotes/', quoteData)
    return response.data
  },

  // Get all quotes for the current user
  async getMyQuotes(): Promise<QuoteResponse[]> {
    const response = await api.get('/quotes/')
    return response.data
  },

  // Get a specific quote by ID
  async getQuote(quoteId: number): Promise<QuoteResponse> {
    const response = await api.get(`/quotes/${quoteId}`)
    return response.data
  }
}
