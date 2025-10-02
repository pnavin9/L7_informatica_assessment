import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useState, useEffect, useRef } from 'react'

export default function Header() {
  const navigate = useNavigate()
  const location = useLocation()
  const [searchQuery, setSearchQuery] = useState('')
  const debounceTimer = useRef<number | null>(null)

  // Extract search query from URL on mount and location change
  useEffect(() => {
    const params = new URLSearchParams(location.search)
    const query = params.get('q') || ''
    setSearchQuery(query)
  }, [location.search])

  // Update URL as user types (with debouncing)
  useEffect(() => {
    // Clear existing timer
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current)
    }

    // Set new timer
    debounceTimer.current = setTimeout(() => {
      const params = new URLSearchParams(location.search)
      const currentQuery = params.get('q') || ''
      
      // Navigate to /movies if query has changed
      if (currentQuery !== searchQuery) {
        if (searchQuery.trim()) {
          navigate(`/movies?q=${encodeURIComponent(searchQuery.trim())}`, { replace: true })
        } else if (location.pathname === '/movies') {
          // Only clear query if already on /movies page
          navigate('/movies', { replace: true })
        }
      }
    }, 300) // 300ms debounce

    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current)
      }
    }
  }, [searchQuery, navigate, location.pathname, location.search])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setSearchQuery(value)
  }

  return (
    <header className="bg-black/30 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Navigation */}
          <div className="flex items-center gap-8">
            <Link to="/" className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
              MovieExplorer
            </Link>
            
            <nav className="hidden md:flex gap-6">
              <Link to="/movies" className="text-gray-300 hover:text-white transition-colors">
                Movies
              </Link>
              <Link to="/actors" className="text-gray-300 hover:text-white transition-colors">
                Actors
              </Link>
              <Link to="/directors" className="text-gray-300 hover:text-white transition-colors">
                Directors
              </Link>
            </nav>
          </div>

          {/* Search Input */}
          <div className="flex items-center">
            <input
              type="text"
              value={searchQuery}
              onChange={handleInputChange}
              placeholder="Search movies, actors, directors..."
              className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-purple-500 transition-colors w-64"
            />
          </div>
        </div>
      </div>
    </header>
  )
}

