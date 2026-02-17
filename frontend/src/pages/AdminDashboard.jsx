import { useEffect, useState } from 'react'
import api from '../api/client'

export default function AdminDashboard() {
  const [analytics, setAnalytics] = useState({})
  const [users, setUsers] = useState([])

  const load = async () => {
    const [a, u] = await Promise.all([api.get('/admin/analytics'), api.get('/admin/users')])
    setAnalytics(a.data)
    setUsers(u.data)
  }

  useEffect(() => { load() }, [])

  return (
    <div className="max-w-6xl mx-auto p-4 space-y-4">
      <div className="grid md:grid-cols-5 gap-3">
        {Object.entries(analytics).map(([k, v]) => <div key={k} className="card"><p className="text-xs uppercase">{k}</p><p className="text-xl">{v}</p></div>)}
      </div>
      <div className="card">
        <h2 className="text-xl font-bold mb-2">User Management</h2>
        {users.map((u) => <div key={u.id}>{u.email} - {u.role} - {u.is_active ? 'active' : 'inactive'}</div>)}
      </div>
    </div>
  )
}
