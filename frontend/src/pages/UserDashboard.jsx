import { useEffect, useState } from 'react'
import api from '../api/client'
import { useAuth } from '../contexts/AuthContext'

export default function UserDashboard() {
  const { user } = useAuth()
  const [subs, setSubs] = useState([])
  const [payments, setPayments] = useState([])

  const load = async () => {
    const [s, p] = await Promise.all([api.get('/subscriptions'), api.get('/payments/history')])
    setSubs(s.data)
    setPayments(p.data)
  }

  useEffect(() => { load() }, [])

  const createOrder = async (id) => {
    await api.post('/payments/create-order', { subscription_id: id })
    alert('Order created. Use Razorpay checkout integration client-side with returned order in production.')
  }

  return (
    <div className="max-w-6xl mx-auto p-4 grid md:grid-cols-2 gap-4">
      <div className="card">
        <h2 className="text-xl font-bold mb-2">Profile</h2>
        <p>{user?.name}</p><p>{user?.email}</p>
      </div>
      <div className="card">
        <h2 className="text-xl font-bold mb-2">Subscriptions</h2>
        {subs.map((s) => (
          <div key={s.id} className="border-b border-slate-800 py-2">
            {s.plan_name} - {s.status} - {s.payment_status}
            {s.payment_status !== 'paid' && <button className="btn-primary ml-2" onClick={() => createOrder(s.id)}>Pay</button>}
          </div>
        ))}
      </div>
      <div className="card md:col-span-2">
        <h2 className="text-xl font-bold mb-2">Payment History</h2>
        {payments.map((p) => <div key={p.id}>{p.payment_gateway_id} - ₹{p.amount} - {p.status}</div>)}
      </div>
    </div>
  )
}
