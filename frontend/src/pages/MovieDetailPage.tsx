 
import { useParams, Link } from 'react-router-dom'
import { getMovie } from '../services/api'
import type { MovieDetail } from '../types'
import Loading from '../components/Loading'
import PageContainer from '../components/PageContainer'
import { Star } from '../components/Icons'
import Card from '../components/Card'
import BackLink from '../components/BackLink'
import SectionTitle from '../components/SectionTitle'
import { useAsync } from '../hooks/useAsync'

export default function MovieDetailPage() {
  const { id } = useParams()
  const { data: movie, loading, error } = useAsync<MovieDetail>(
    () => id ? getMovie(id) : Promise.reject(new Error('Missing id')),
    [id]
  )

  if (loading) return <Loading skeleton label="Loading movie..." />

  if (error || !movie) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-3xl font-bold text-red-400 mb-4">Movie Not Found</h1>
        <Link to="/movies" className="text-purple-400 hover:text-purple-300">
          ← Back to Movies
        </Link>
      </div>
    )
  }

  return (
    <PageContainer>
        <BackLink to="/movies">← Back to Movies</BackLink>

        <Card className="mb-8">
          <div className="md:flex">
            {movie.poster_url && (
              <div className="md:w-1/3">
                <img 
                  src={movie.poster_url} 
                  alt={movie.title}
                  className="w-full h-full object-cover"
                />
              </div>
            )}
            
            <div className="p-8 md:w-2/3">
              <SectionTitle as="h1" className="mb-4">{movie.title}</SectionTitle>
              
              <div className="flex flex-wrap gap-4 mb-6">
                <div>
                  <span className="text-purple-400 font-semibold">Year:</span>
                  <span className="text-gray-300 ml-2">{movie.release_year}</span>
                </div>
                
                {movie.duration_minutes && (
                  <div>
                    <span className="text-purple-400 font-semibold">Duration:</span>
                    <span className="text-gray-300 ml-2">{movie.duration_minutes} min</span>
                  </div>
                )}
                
                {movie.status && (
                  <div>
                    <span className="text-purple-400 font-semibold">Status:</span>
                    <span className="text-gray-300 ml-2">{movie.status}</span>
                  </div>
                )}
              </div>

              {movie.average_rating && (
                <div className="mb-6">
                  <div className="flex items-center gap-2">
                    <Star className="w-6 h-6 text-yellow-400" />
                    <span className="text-yellow-400 font-bold text-2xl">{movie.average_rating.toFixed(1)}</span>
                    <span className="text-gray-400">({movie.rating_count} {movie.rating_count === 1 ? 'rating' : 'ratings'})</span>
                  </div>
                </div>
              )}

              {movie.director && (
                <div className="mb-6">
                  <SectionTitle as="h3">Director</SectionTitle>
                  <Link to={`/directors/${movie.director.id}`} className="text-gray-300 hover:text-white transition-colors">
                    {movie.director.name}
                  </Link>
                </div>
              )}

              {movie.genres && movie.genres.length > 0 && (
                <div className="mb-6">
                  <SectionTitle as="h3">Genres</SectionTitle>
                  <div className="flex flex-wrap gap-2">
                    {movie.genres.map((genre) => (
                      <span key={genre.id} className="px-3 py-1 bg-purple-500/20 text-purple-300 text-sm rounded">
                        {genre.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {movie.synopsis && (
                <div className="mb-6">
                  <SectionTitle as="h3">Synopsis</SectionTitle>
                  <p className="text-gray-300 leading-relaxed">{movie.synopsis}</p>
                </div>
              )}
            </div>
          </div>
        </Card>

              {movie.actors && movie.actors.length > 0 && (
          <div className="mb-8">
            <SectionTitle as="h2">Cast ({movie.actors.length})</SectionTitle>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
              {movie.actors.map((actor) => (
                <Link 
                  key={actor.id} 
                  to={`/actors/${actor.id}`}
                  className="bg-white/10 backdrop-blur-sm rounded-lg overflow-hidden border border-white/10 hover:border-purple-500/50 transition-all hover:scale-105"
                >
                  {actor.photo_url && (
                    <img 
                      src={actor.photo_url} 
                      alt={actor.name}
                      className="w-full h-48 object-cover"
                    />
                  )}
                  <div className="p-3">
                    <p className="text-white text-sm font-semibold text-center">{actor.name}</p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </PageContainer>
  )
}

