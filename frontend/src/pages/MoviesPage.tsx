 
import { useSearchParams } from 'react-router-dom'
import MovieCard from '../components/MovieCard'
import { getMovies, searchMoviesOR } from '../services/api'
import type { Movie } from '../types'
import Loading from '../components/Loading'
import PageContainer from '../components/PageContainer'
import SectionTitle from '../components/SectionTitle'
import { useAsync } from '../hooks/useAsync'

export default function MoviesPage() {
  const [searchParams] = useSearchParams()
  const query = searchParams.get('q')
  const { data, loading, error } = useAsync<Movie[]>(
    () => (query ? searchMoviesOR(query) : getMovies()),
    // Depend on the raw string so the effect runs when q changes
    [query]
  )

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
      
      {searchParams.get('q') && (
        <p className="text-purple-300 mb-4">
          Searching for: <span className="font-semibold">"{searchParams.get('q')}"</span>
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

