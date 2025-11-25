import api from './api'

export interface ContactMessageCreate {
  full_name: string
  email: string
  phone?: string
  subject: string
  message: string
}

export interface ContactMessageResponse {
  id: number
  subject: string
  status: string
  created_at: string
  has_response: boolean
}

export interface ContactMessageDetail {
  id: number
  full_name: string
  email: string
  phone: string | null
  subject: string
  message: string
  status: string
  admin_response: string | null
  responded_at: string | null
  created_at: string
}

export interface SubmitContactResponse {
  id: number
  status: string
  created_at: string
  message: string
}

export interface ContactMessagesListResponse {
  messages: ContactMessageResponse[]
  total: number
  page: number
  per_page: number
}

const contactService = {
  /**
   * Submit a contact message (public endpoint - no auth required)
   */
  async submitContactMessage(data: ContactMessageCreate): Promise<SubmitContactResponse> {
    const response = await api.post<SubmitContactResponse>('/contact/submit', data)
    return response.data
  },

  /**
   * Get user's contact messages (requires authentication)
   */
  async getUserMessages(): Promise<ContactMessageResponse[]> {
    const response = await api.get<ContactMessageResponse[]>('/contact/messages')
    return response.data
  },

  /**
   * Get specific message detail (requires authentication)
   */
  async getMessageDetail(id: number | string): Promise<ContactMessageDetail> {
    const response = await api.get<ContactMessageDetail>(`/contact/${id}`)
    return response.data
  }
}

export default contactService
