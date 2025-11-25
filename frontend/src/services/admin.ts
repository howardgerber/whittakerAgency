/**
 * Admin API Service
 * Handles all admin dashboard API calls
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance with auth interceptor
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to all requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Dashboard Stats Types (matches backend DashboardStatsResponse)
export interface DashboardStats {
  quotes: {
    pending: number
    in_review: number
    quoted: number
    total: number
  }
  claims: {
    submitted: number
    contacted: number
    closed: number
    total: number
  }
  messages: {
    new: number
    read: number
    responded: number
    closed: number
    total: number
  }
  users: {
    active: number
    inactive: number
    total: number
  }
  recent_activity: RecentActivityItem[]
}

export interface RecentActivityItem {
  type: 'quote' | 'claim' | 'message'
  customer: string
  action: string
  date: string
}

export interface AttentionItem {
  type: 'quote' | 'claim' | 'message' | 'multiple_quotes' | 'multiple_claims'
  id: number | null
  user_id: number | null
  customer_name: string
  title: string
  category: string
  detail: string
  age: string
  priority: 'high' | 'medium' | 'low'
  icon: string
  link: string
}

// Quote Types (reuse from quotes service)
export interface AdminQuote {
  id: number
  user_id: number
  category: string
  subcategory: string | null
  status: string
  quote_data: Record<string, any>
  customer_notes: string | null
  quote_amount: number | null
  appointment_date: string | null
  agent_notes: string | null
  quoted_at: string | null
  created_at: string
  updated_at: string
  customer_name: string
  customer_email: string
  customer_phone: string | null
}

export interface UpdateQuoteRequest {
  status?: string
  quote_amount?: number
  appointment_date?: string
  agent_notes?: string
}

// Claim Types
export interface AdminClaim {
  id: number
  user_id: number
  category: string
  subcategory: string | null
  status: string
  incident_date: string
  claim_data: Record<string, any>
  appointment_requested: string | null
  admin_notes: string | null
  contacted_at: string | null
  created_at: string
  updated_at: string
  customer_name: string
  customer_email: string
  customer_phone: string | null
}

export interface UpdateClaimRequest {
  status?: string
  appointment_requested?: string
  admin_notes?: string
}

// Message Types
export interface AdminMessage {
  id: number
  user_id: number | null
  subject: string
  message: string
  status: string
  admin_response: string | null
  appointment_date: string | null
  responded_at: string | null
  created_at: string
  updated_at: string
  sender_name: string
  sender_email: string
  sender_phone: string | null
  is_guest: boolean
}

export interface UpdateMessageRequest {
  status?: string
  appointment_date?: string
  admin_response?: string
}

// User Types
export interface AdminUser {
  id: number
  username: string
  full_name: string
  email: string
  phone: string | null
  is_active: boolean
  is_admin: boolean
  created_at: string
  last_login_at: string | null
  quotes_count: number
  claims_count: number
  messages_count: number
}

export interface UserActivity {
  quotes: Array<{id: number, category: string, status: string, created_at: string}>
  claims: Array<{id: number, category: string, status: string, created_at: string}>
  messages: Array<{id: number, subject: string, status: string, created_at: string}>
  recent_activity: Array<{type: string, action: string, date: string}>
}

export interface AdminUserDetail extends AdminUser {
  updated_at: string
  activity: UserActivity
}

export interface UpdateUserRequest {
  is_active?: boolean
  is_admin?: boolean
}

// Admin Service
class AdminService {
  /**
   * Get dashboard stats
   */
  async getDashboardStats(): Promise<DashboardStats> {
    try {
      const response = await apiClient.get('/admin/dashboard/stats')
      return response.data
    } catch (error: any) {
      console.error('Error fetching dashboard stats:', error)
      throw error
    }
  }

  /**
   * Get attention items for dashboard
   */
  async getAttentionItems(): Promise<AttentionItem[]> {
    try {
      const response = await apiClient.get('/admin/dashboard/attention-items')
      return response.data.items
    } catch (error: any) {
      console.error('Error fetching attention items:', error)
      throw error
    }
  }

  /**
   * Get all quotes with optional filters
   */
  async getQuotes(params?: {
    category?: string
    subcategory?: string
    status?: string
    start_date?: string
    end_date?: string
    search?: string
    page?: number
    limit?: number
  }): Promise<{ items: AdminQuote[]; total: number; page: number; limit: number; pages: number }> {
    try {
      const response = await apiClient.get('/admin/quotes', { params })
      return response.data
    } catch (error: any) {
      console.error('Error fetching quotes:', error)
      throw error
    }
  }

  /**
   * Get single quote by ID
   */
  async getQuote(id: number): Promise<AdminQuote> {
    try {
      const response = await apiClient.get(`/admin/quotes/${id}`)
      return response.data
    } catch (error: any) {
      console.error(`Error fetching quote ${id}:`, error)
      throw error
    }
  }

  /**
   * Update quote (amount, notes, status)
   */
  async updateQuote(id: number, data: UpdateQuoteRequest): Promise<AdminQuote> {
    try {
      const response = await apiClient.put(`/admin/quotes/${id}`, data)
      return response.data
    } catch (error: any) {
      console.error(`Error updating quote ${id}:`, error)
      throw error
    }
  }

  /**
   * Get all claims with optional filters
   */
  async getClaims(params?: {
    category?: string
    subcategory?: string
    status?: string
    start_date?: string
    end_date?: string
    search?: string
    page?: number
    limit?: number
  }): Promise<{ items: AdminClaim[]; total: number; page: number; limit: number; pages: number }> {
    try {
      const response = await apiClient.get('/admin/claims', { params })
      return response.data
    } catch (error: any) {
      console.error('Error fetching claims:', error)
      throw error
    }
  }

  /**
   * Get single claim by ID
   */
  async getClaim(id: number): Promise<AdminClaim> {
    try {
      const response = await apiClient.get(`/admin/claims/${id}`)
      return response.data
    } catch (error: any) {
      console.error(`Error fetching claim ${id}:`, error)
      throw error
    }
  }

  /**
   * Update claim (notes, status, appointment)
   */
  async updateClaim(id: number, data: UpdateClaimRequest): Promise<AdminClaim> {
    try {
      const response = await apiClient.put(`/admin/claims/${id}`, data)
      return response.data
    } catch (error: any) {
      console.error(`Error updating claim ${id}:`, error)
      throw error
    }
  }

  /**
   * Get all messages with optional filters
   */
  async getMessages(params?: {
    subject?: string
    status?: string
    start_date?: string
    end_date?: string
    search?: string
    include_guest?: boolean
    page?: number
    limit?: number
  }): Promise<{ items: AdminMessage[]; total: number; page: number; limit: number; pages: number }> {
    try {
      const response = await apiClient.get('/admin/messages', { params })
      return response.data
    } catch (error: any) {
      console.error('Error fetching messages:', error)
      throw error
    }
  }

  /**
   * Get single message by ID
   */
  async getMessage(id: number): Promise<AdminMessage> {
    try {
      const response = await apiClient.get(`/admin/messages/${id}`)
      return response.data
    } catch (error: any) {
      console.error(`Error fetching message ${id}:`, error)
      throw error
    }
  }

  /**
   * Update message (response, status)
   */
  async updateMessage(id: number, data: UpdateMessageRequest): Promise<AdminMessage> {
    try {
      const response = await apiClient.put(`/admin/messages/${id}`, data)
      return response.data
    } catch (error: any) {
      console.error(`Error updating message ${id}:`, error)
      throw error
    }
  }

  /**
   * Get all users with optional filters
   */
  async getUsers(params?: {
    status?: string
    search?: string
    start_date?: string
    end_date?: string
    sort_by?: string
    sort_order?: string
    page?: number
    limit?: number
  }): Promise<{ items: AdminUser[]; total: number; page: number; limit: number; pages: number }> {
    try {
      const response = await apiClient.get('/admin/users', { params })
      return response.data
    } catch (error: any) {
      console.error('Error fetching users:', error)
      throw error
    }
  }

  /**
   * Get single user by ID with activity details
   */
  async getUserDetail(id: number, dateRange?: string): Promise<AdminUserDetail> {
    try {
      const params = dateRange ? { date_range: dateRange } : {}
      const response = await apiClient.get(`/admin/users/${id}`, { params })
      return response.data
    } catch (error: any) {
      console.error(`Error fetching user ${id}:`, error)
      throw error
    }
  }

  /**
   * Update user (active status, admin status)
   */
  async updateUser(id: number, data: UpdateUserRequest): Promise<AdminUserDetail> {
    try {
      const response = await apiClient.put(`/admin/users/${id}`, data)
      return response.data
    } catch (error: any) {
      console.error(`Error updating user ${id}:`, error)
      throw error
    }
  }
}

export default new AdminService()
