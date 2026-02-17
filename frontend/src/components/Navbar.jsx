import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()

  return (
    <nav className="p-4 border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-10">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <Link to="/" className="font-bold text-xl">ProGym SaaS</Link>
        <div className="space-x-4">
          <Link to="/pricing">Pricing</Link>
          {!user && <Link to="/login">Login</Link>}
          {!user && <Link to="/signup" className="btn-primary">Get Started</Link>}
          {user && <Link to={user.role === 'admin' ? '/admin' : '/dashboard'}>Dashboard</Link>}
          {user && <button onClick={logout} className="btn bg-slate-800">Logout</button>}
        </div>
      </div>
    </nav>
  )
}
