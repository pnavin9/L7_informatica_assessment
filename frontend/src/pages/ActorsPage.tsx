 
import IndividualCard from '../components/IndividualCard'
import { getActors } from '../services/api'
import type { Actor } from '../types'
import Loading from '../components/Loading'
import PageContainer from '../components/PageContainer'
import SectionTitle from '../components/SectionTitle'
import { useAsync } from '../hooks/useAsync'

export default function ActorsPage() {
  const { data: actors, loading, error } = useAsync<Actor[]>(() => getActors(), [])

  if (loading) return <Loading skeleton label="Loading actors..." />
  if (error) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-3xl font-bold text-red-400 mb-4">Failed to load actors</h1>
        <p className="text-gray-300">{error}</p>
      </div>
    )
  }
  
  return (
    <PageContainer>
      <SectionTitle as="h1">Actors</SectionTitle>
      
      <p className="text-gray-300 mb-6">{(actors ?? []).length} actors found</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {(actors ?? []).map((actor) => (
          <IndividualCard key={actor.id} person={actor} type="actors" />
        ))}
      </div>
    </PageContainer>
  )
}

