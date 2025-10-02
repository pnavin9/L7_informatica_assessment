 
import { useParams, Link } from 'react-router-dom'
import MovieCard from '../components/MovieCard'
import { getActor, getMovies } from '../services/api'
import type { Actor, Movie } from '../types'
import Loading from '../components/Loading'
import PageContainer from '../components/PageContainer'
import Card from '../components/Card'
import BackLink from '../components/BackLink'
import SectionTitle from '../components/SectionTitle'
import { useAsync } from '../hooks/useAsync'

export default function ActorDetailPage() {
  const { id } = useParams()
  const { data: actor, loading: actorLoading, error: actorError } = useAsync<Actor>(
    () => (id ? getActor(id) : Promise.reject(new Error('Missing id'))),
    [id]
  )
  const { data: movies, loading: moviesLoading, error: moviesError } = useAsync<Movie[]>(
    () => (actor ? getMovies({ actor: actor.name }) : Promise.reject(new Error('No actor yet'))),
    [actor?.name]
  )
  const loading = actorLoading || moviesLoading
  const error = actorError || moviesError

  if (loading) return <Loading skeleton label="Loading actor..." />

  if (error || !actor) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-3xl font-bold text-red-400 mb-4">Actor Not Found</h1>
        <Link to="/actors" className="text-purple-400 hover:text-purple-300">
          ← Back to Actors
        </Link>
      </div>
    )
  }

  return (
    <PageContainer>
        <BackLink to="/actors">← Back to Actors</BackLink>

        <Card className="mb-8">
          <div className="md:flex">
            {actor.photo_url && (
              <div className="md:w-1/3">
                <img 
                  src={actor.photo_url} 
                  alt={actor.name}
                  className="w-full h-full object-cover"
                />
              </div>
            )}
            
            <div className="p-8 md:w-2/3">
              <SectionTitle as="h1" className="mb-4">{actor.name}</SectionTitle>
              
              {actor.bio && (
                <div className="mb-6">
                  <SectionTitle as="h3">Biography</SectionTitle>
                  <p className="text-gray-300 leading-relaxed">{actor.bio}</p>
                </div>
              )}
            </div>
          </div>
        </Card>

        {movies && movies.length > 0 && (
          <div>
            <SectionTitle as="h2">Movies ({movies.length})</SectionTitle>
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

