import { Link } from 'react-router-dom'
import type { Actor, Director } from '../types'

type Person = Actor | Director

interface IndividualCardProps {
  person: Person
  type: 'actors' | 'directors'
}

export default function IndividualCard({ person, type }: IndividualCardProps) {
  return (
    <Link to={`/${type}/${person.id}`} className="bg-white/10 backdrop-blur-sm rounded-lg overflow-hidden border border-white/10 hover:border-purple-500/50 transition-all hover:scale-105 block">
      {person.photo_url && (
        <img 
          src={person.photo_url} 
          alt={person.name}
          className="w-full h-64 object-cover"
        />
      )}
      
      <div className="p-6">
        <h3 className="text-xl font-bold text-white mb-2">{person.name}</h3>
        
        {person.bio && (
          <p className="text-gray-300 text-sm line-clamp-3 mb-3">
            {person.bio}
          </p>
        )}
      </div>
    </Link>
  )
}
