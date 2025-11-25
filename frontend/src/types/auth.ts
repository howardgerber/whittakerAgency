export interface UserRegister {
  username: string
  email: string
  full_name: string
  phone?: string
  password: string
}

export interface UserLogin {
  username: string
  password: string
}

export interface Token {
  access_token: string
  token_type: string
}

export interface UserProfile {
  id: number
  username: string
  email: string
  full_name: string
  phone?: string
  is_active: boolean
  is_admin: boolean
  created_at: string
}
