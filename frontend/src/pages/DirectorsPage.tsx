 
import IndividualCard from '../components/IndividualCard'
import { getDirectors } from '../services/api'
import type { Director } from '../types'
import Loading from '../components/Loading'
import PageContainer from '../components/PageContainer'
import SectionTitle from '../components/SectionTitle'
import { useAsync } from '../hooks/useAsync'

export default function DirectorsPage() {
  const { data: directors, loading, error } = useAsync<Director[]>(() => getDirectors(), [])

  if (loading) return <Loading skeleton label="Loading directors..." />
  if (error) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-3xl font-bold text-red-400 mb-4">Failed to load directors</h1>
        <p className="text-gray-300">{error}</p>
      </div>
    )
  }
  
  return (
    <PageContainer>
      <SectionTitle as="h1">Directors</SectionTitle>
      
      <p className="text-gray-300 mb-6">{(directors ?? []).length} directors found</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {(directors ?? []).map((director) => (
          <IndividualCard key={director.id} person={director} type="directors" />
        ))}
      </div>
    </PageContainer>
  )
}

