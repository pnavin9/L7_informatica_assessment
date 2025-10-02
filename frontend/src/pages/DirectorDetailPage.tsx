 
import { useParams, Link } from 'react-router-dom'
import MovieCard from '../components/MovieCard'
import { getDirector, getMovies } from '../services/api'
import type { Director, Movie } from '../types'
import Loading from '../components/Loading'
import PageContainer from '../components/PageContainer'
import Card from '../components/Card'
import BackLink from '../components/BackLink'
import SectionTitle from '../components/SectionTitle'
import { useAsync } from '../hooks/useAsync'

export default function DirectorDetailPage() {
  const { id } = useParams()
  const { data: director, loading: directorLoading, error: directorError } = useAsync<Director>(
    () => (id ? getDirector(id) : Promise.reject(new Error('Missing id'))),
    [id]
  )
  const { data: movies, loading: moviesLoading, error: moviesError } = useAsync<Movie[]>(
    () => (director ? getMovies({ director: director.name }) : Promise.reject(new Error('No director yet'))),
    [director?.name]
  )
  const loading = directorLoading || moviesLoading
  const error = directorError || moviesError

  if (loading) return <Loading skeleton label="Loading director..." />

  if (error || !director) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-3xl font-bold text-red-400 mb-4">Director Not Found</h1>
        <Link to="/directors" className="text-purple-400 hover:text-purple-300">
          ← Back to Directors
        </Link>
      </div>
    )
  }

  return (
    <PageContainer>
        <BackLink to="/directors">← Back to Directors</BackLink>

        <Card className="mb-8">
          <div className="md:flex">
            {director.photo_url && (
              <div className="md:w-1/3">
                <img 
                  src={director.photo_url} 
                  alt={director.name}
                  className="w-full h-full object-cover"
                />
              </div>
            )}
            
            <div className="p-8 md:w-2/3">
              <SectionTitle as="h1" className="mb-4">{director.name}</SectionTitle>
              
              {director.bio && (
                <div className="mb-6">
                  <SectionTitle as="h3">Biography</SectionTitle>
                  <p className="text-gray-300 leading-relaxed">{director.bio}</p>
                </div>
              )}
            </div>
          </div>
        </Card>

        {movies && movies.length > 0 && (
          <div>
            <SectionTitle as="h2">Filmography ({movies.length})</SectionTitle>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {movies.map((movie: any) => (
                <MovieCard key={movie.id} movie={movie} />
              ))}
            </div>
          </div>
        )}
      </PageContainer>
  )
}

