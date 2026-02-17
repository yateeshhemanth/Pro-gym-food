import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function LoginPage() {
  const { login } = useAuth()
  const nav = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    await login(email, password)
    nav('/dashboard')
  }

  return (
    <form onSubmit={submit} className="card max-w-md mx-auto mt-10 space-y-3">
      <h2 className="text-2xl font-bold">Login</h2>
      <input className="w-full p-2 rounded bg-slate-800" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input className="w-full p-2 rounded bg-slate-800" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button className="btn-primary w-full">Login</button>
    </form>
  )
}
