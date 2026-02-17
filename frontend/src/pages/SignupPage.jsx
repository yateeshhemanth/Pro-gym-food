import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function SignupPage() {
  const { signup } = useAuth()
  const nav = useNavigate()
  const [form, setForm] = useState({ name: '', email: '', password: '' })

  const submit = async (e) => {
    e.preventDefault()
    await signup(form.name, form.email, form.password)
    nav('/dashboard')
  }

  return (
    <form onSubmit={submit} className="card max-w-md mx-auto mt-10 space-y-3">
      <h2 className="text-2xl font-bold">Sign Up</h2>
      {['name', 'email', 'password'].map((k) => (
        <input
          key={k}
          className="w-full p-2 rounded bg-slate-800"
          type={k === 'password' ? 'password' : 'text'}
          placeholder={k}
          value={form[k]}
          onChange={(e) => setForm({ ...form, [k]: e.target.value })}
        />
      ))}
      <button className="btn-primary w-full">Create Account</button>
    </form>
  )
}
