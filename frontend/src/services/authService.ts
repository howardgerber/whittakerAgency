import api from './api'
import type { UserRegister, UserLogin, Token, UserProfile } from '@/types/auth'

export const authService = {
  async register(userData: UserRegister): Promise<UserProfile> {
    const response = await api.post<UserProfile>('/auth/register', userData)
    return response.data
  },

  async login(credentials: UserLogin): Promise<Token> {
    const response = await api.post<Token>('/auth/login', credentials)
    return response.data
  },

  async getCurrentUser(): Promise<UserProfile> {
    const response = await api.get<UserProfile>('/auth/me')
    return response.data
  }
}
