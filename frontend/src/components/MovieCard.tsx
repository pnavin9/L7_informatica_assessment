import { Link } from 'react-router-dom'
import { Star } from './Icons'
import type { Movie } from '../types'

interface MovieCardProps {
  movie: Movie
}

export default function MovieCard({ movie }: MovieCardProps) {
  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-lg overflow-hidden border border-white/10 hover:border-purple-500/50 transition-all hover:scale-105">
      <Link to={`/movies/${movie.id}`}>
        {movie.poster_url && (
          <img 
            src={movie.poster_url} 
            alt={movie.title}
            className="w-full h-64 object-cover"
          />
        )}
      </Link>
      
      <div className="p-6">
        <Link to={`/movies/${movie.id}`}>
          <h3 className="text-xl font-bold text-white mb-2 hover:text-purple-300 transition-colors">{movie.title}</h3>
        </Link>
        <p className="text-gray-400 text-sm mb-3">{movie.release_year}</p>
        
        {movie.director && (
          <div className="mb-3">
            <p className="text-gray-300 text-sm">
              <span className="text-purple-400">Director:</span>{' '}
              <Link 
                to={`/directors/${movie.director.id}`}
                className="hover:text-white hover:underline transition-colors"
              >
                {movie.director.name}
              </Link>
            </p>
          </div>
        )}

        {movie.genres && movie.genres.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-3">
            {movie.genres.map((genre) => (
              <span key={genre.id} className="px-2 py-1 bg-purple-500/20 text-purple-300 text-xs rounded">
                {genre.name}
              </span>
            ))}
          </div>
        )}

        {movie.average_rating && (
          <div className="flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-400" />
            <span className="text-yellow-400 font-semibold">{movie.average_rating.toFixed(1)}</span>
          </div>
        )}
      </div>
    </div>
  )
}

