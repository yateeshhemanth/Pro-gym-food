import { createContext, useContext, useState } from 'react'
import api from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user') || 'null'))

  const login = async (email, password) => {
    const { data } = await api.post('/auth/login', { email, password })
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    const me = await api.get('/users/me')
    localStorage.setItem('user', JSON.stringify(me.data))
    setUser(me.data)
  }

  const signup = async (name, email, password) => {
    await api.post('/auth/register', { name, email, password })
    await login(email, password)
  }

  const logout = async () => {
    try { await api.post('/auth/logout') } catch (_) {}
    localStorage.clear()
    setUser(null)
  }

  return <AuthContext.Provider value={{ user, login, signup, logout }}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
