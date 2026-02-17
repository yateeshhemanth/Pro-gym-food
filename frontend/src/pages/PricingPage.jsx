import api from '../api/client'

const plans = [
  { plan_id: 'daily', name: 'Daily', price: 5, duration: 1 },
  { plan_id: 'monthly', name: 'Monthly', price: 99, duration: 30 },
  { plan_id: 'quarterly', name: '3-Month', price: 249, duration: 90 }
]

export default function PricingPage() {
  const subscribe = async (plan_id) => {
    const { data } = await api.post('/subscriptions/create', { plan_id })
    alert(`Subscription created with ID ${data.id}. Complete payment from dashboard.`)
  }

  return (
    <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-4 py-10 px-4">
      {plans.map((p) => (
        <div key={p.plan_id} className="card">
          <h3 className="text-2xl font-semibold">{p.name}</h3>
          <p className="text-3xl mt-3">₹{p.price}</p>
          <p className="text-slate-400">{p.duration} day access</p>
          <button onClick={() => subscribe(p.plan_id)} className="btn-primary mt-4 w-full">Choose Plan</button>
        </div>
      ))}
    </div>
  )
}
