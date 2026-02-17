import { Link } from 'react-router-dom'

export default function LandingPage() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-16">
      <h1 className="text-5xl font-bold mb-6">Build fitness consistency with automated plans</h1>
      <p className="text-slate-300 mb-8">Enterprise-ready subscription platform for ProGym with secure auth, payments, and analytics.</p>
      <Link to="/pricing" className="btn-primary">View Plans</Link>
    </div>
  )
}
