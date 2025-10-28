export interface UserRegister {
  email: string
  full_name: string
  phone?: string
  password: string
}

export interface UserLogin {
  email: string
  password: string
}

export interface Token {
  access_token: string
  token_type: string
}

export interface UserProfile {
  id: number
  email: string
  full_name: string
  phone?: string
  is_active: boolean
  created_at: string
}
