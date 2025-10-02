 
import { useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import MovieCard from '../components/MovieCard'
import { getMovies, searchMoviesOR, getGenres } from '../services/api'
import type { Movie, Genre } from '../types'
import Loading from '../components/Loading'
import PageContainer from '../components/PageContainer'
import SectionTitle from '../components/SectionTitle'
import { useAsync } from '../hooks/useAsync'

export default function MoviesPage() {
  const [searchParams, setSearchParams] = useSearchParams()

  // Extract current query and filters from URL
  const query = searchParams.get('q') || ''
  const genre = searchParams.get('genre') || ''
  const actor = searchParams.get('actor') || ''
  const director = searchParams.get('director') || ''
  const yearParam = searchParams.get('year') || ''
  const minYearParam = searchParams.get('min_year') || ''
  const maxYearParam = searchParams.get('max_year') || ''

  // Local input state (only applied when clicking Apply)
  const [genreInput, setGenreInput] = useState<string>(genre)
  const [actorInput, setActorInput] = useState<string>(actor)
  const [directorInput, setDirectorInput] = useState<string>(director)
  const [yearInput, setYearInput] = useState<string>(yearParam)
  const [minYearInput, setMinYearInput] = useState<string>(minYearParam)
  const [maxYearInput, setMaxYearInput] = useState<string>(maxYearParam)

  const year = yearParam ? Number(yearParam) : undefined
  const min_year = minYearParam ? Number(minYearParam) : undefined
  const max_year = maxYearParam ? Number(maxYearParam) : undefined

  const hasFilters = Boolean(genre || actor || director || year || min_year || max_year)

  // Fetch movies depending on whether filters are set; prefer filters over q search
  const { data, loading, error } = useAsync<Movie[]>(
    () =>
      hasFilters
        ? getMovies({ genre, actor, director, year, min_year, max_year })
        : (query ? searchMoviesOR(query) : getMovies()),
    [query, genre, actor, director, year, min_year, max_year]
  )

  // Fetch genres for the genre select
  const { data: genresData } = useAsync<Genre[]>(() => getGenres(), [])
  const genres = useMemo(() => genresData ?? [], [genresData])

  // Apply button: write local inputs to URL params (which triggers fetch)
  const applyFilters = () => {
    const next = new URLSearchParams(searchParams)

    const setOrDelete = (key: string, value: string) => {
      if (value && value.trim().length > 0) next.set(key, value.trim())
      else next.delete(key)
    }

    setOrDelete('genre', genreInput)
    setOrDelete('actor', actorInput)
    setOrDelete('director', directorInput)
    setOrDelete('year', yearInput)
    setOrDelete('min_year', minYearInput)
    setOrDelete('max_year', maxYearInput)

    const anyFilter = [genreInput, actorInput, directorInput, yearInput, minYearInput, maxYearInput]
      .some(v => v && v.trim().length > 0)
    if (anyFilter) next.delete('q')

    setSearchParams(next, { replace: true })
  }

  // Clear inputs only (does not fetch until Apply is clicked)
  const clearFilterInputs = () => {
    setGenreInput('')
    setActorInput('')
    setDirectorInput('')
    setYearInput('')
    setMinYearInput('')
    setMaxYearInput('')
  }

  if (loading) return <Loading skeleton label="Loading movies..." />
  if (error) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-3xl font-bold text-red-400 mb-4">Failed to load movies</h1>
        <p className="text-gray-300">{error}</p>
      </div>
    )
  }
  
  return (
    <PageContainer>
      <SectionTitle as="h1">Browse Movies</SectionTitle>
      
      {/* Filters */}
      <div className="mb-6 p-4 bg-white/5 border border-white/10 rounded-lg">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          {/* Genre */}
          <div>
            <label className="block text-sm text-gray-400 mb-1">Genre</label>
            <select
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded text-white"
              value={genreInput}
              onChange={(e) => setGenreInput(e.target.value)}
            >
              <option value="">All</option>
              {genres.map((g) => (
                <option key={g.id} value={g.name}>{g.name}</option>
              ))}
            </select>
          </div>

          {/* Actor */}
          <div>
            <label className="block text-sm text-gray-400 mb-1">Actor</label>
            <input
              type="text"
              placeholder="e.g., Leonardo DiCaprio"
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded text-white placeholder-gray-400"
              value={actorInput}
              onChange={(e) => setActorInput(e.target.value)}
            />
          </div>

          {/* Director */}
          <div>
            <label className="block text-sm text-gray-400 mb-1">Director</label>
            <input
              type="text"
              placeholder="e.g., Christopher Nolan"
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded text-white placeholder-gray-400"
              value={directorInput}
              onChange={(e) => setDirectorInput(e.target.value)}
            />
          </div>

          {/* Year (exact) */}
          <div>
            <label className="block text-sm text-gray-400 mb-1">Year</label>
            <input
              type="number"
              min={1888}
              max={2100}
              placeholder="e.g., 2010"
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded text-white placeholder-gray-400"
              value={yearInput}
              onChange={(e) => setYearInput(e.target.value)}
            />
          </div>

          {/* Min Year */}
          <div>
            <label className="block text-sm text-gray-400 mb-1">Min Year</label>
            <input
              type="number"
              min={1888}
              max={2100}
              placeholder="From"
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded text-white placeholder-gray-400"
              value={minYearInput}
              onChange={(e) => setMinYearInput(e.target.value)}
            />
          </div>

          {/* Max Year */}
          <div>
            <label className="block text-sm text-gray-400 mb-1">Max Year</label>
            <input
              type="number"
              min={1888}
              max={2100}
              placeholder="To"
              className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded text-white placeholder-gray-400"
              value={maxYearInput}
              onChange={(e) => setMaxYearInput(e.target.value)}
            />
          </div>
        </div>

        <div className="mt-4 flex items-center gap-3">
          <button
            onClick={applyFilters}
            className="px-4 py-2 text-sm bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded font-semibold hover:opacity-90"
          >
            Apply filters
          </button>

          <button
            onClick={clearFilterInputs}
            className="px-4 py-2 text-sm bg-white/10 border border-white/20 rounded text-white hover:bg-white/20"
          >
            Clear inputs
          </button>

          {hasFilters && (
            <span className="text-xs text-purple-300">Filters applied</span>
          )}
        </div>
      </div>
      
      {(!hasFilters && query) && (
        <p className="text-purple-300 mb-4">
          Searching for: <span className="font-semibold">"{query}"</span>
        </p>
      )}
      
      <p className="text-gray-300 mb-6">{(data ?? []).length} movies found</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {(data ?? []).map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    </PageContainer>
  )
}

