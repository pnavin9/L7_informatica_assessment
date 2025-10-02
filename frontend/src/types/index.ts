export interface Genre {
  id: number
  name: string
}

export interface PersonBase {
  id: number
  name: string
  bio?: string | null
  photo_url?: string | null
}

export type Actor = PersonBase
export type Director = PersonBase

export interface Movie {
  id: number
  title: string
  release_year: number
  synopsis?: string | null
  poster_url?: string | null
  duration_minutes?: number | null
  status?: string | null
  director: Director
  genres: Genre[]
  average_rating?: number | null
  rating_count?: number
}

export interface MovieDetail extends Movie {
  actors: Actor[]
}


