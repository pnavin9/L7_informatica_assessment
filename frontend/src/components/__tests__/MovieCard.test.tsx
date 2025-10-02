import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import MovieCard from '../MovieCard'
import { describe, it, expect } from 'vitest'
const renderWithRouter = (ui: React.ReactElement) => {
  return render(<MemoryRouter>{ui}</MemoryRouter>)
}

describe('MovieCard', () => {
  it('renders title, year, genres and rating', () => {
    const movie = {
      id: 1,
      title: 'Inception',
      release_year: 2010,
      synopsis: null,
      poster_url: 'https://example.com/poster.jpg',
      duration_minutes: null,
      status: null,
      director: { id: 10, name: 'Christopher Nolan', bio: null, photo_url: null },
      genres: [
        { id: 100, name: 'Sci-Fi' },
        { id: 101, name: 'Thriller' },
      ],
      average_rating: 4.6,
      rating_count: 1000,
    }

    renderWithRouter(<MovieCard movie={movie} />)

    expect(screen.getByRole('heading', { name: 'Inception' })).toBeInTheDocument()
    expect(screen.getByText('2010')).toBeInTheDocument()
    expect(screen.getByText('Sci-Fi')).toBeInTheDocument()
    expect(screen.getByText('Thriller')).toBeInTheDocument()
    expect(screen.getByText('4.6')).toBeInTheDocument()
  })

  it('omits rating when average_rating is null/undefined', () => {
    const movie = {
      id: 2,
      title: 'Untitled',
      release_year: 2024,
      synopsis: null,
      poster_url: null,
      duration_minutes: null,
      status: null,
      director: { id: 20, name: 'Someone', bio: null, photo_url: null },
      genres: [],
      average_rating: null,
      rating_count: 0,
    }

    renderWithRouter(<MovieCard movie={movie} />)

    expect(screen.getByRole('heading', { name: 'Untitled' })).toBeInTheDocument()
    expect(screen.queryByText('NaN')).not.toBeInTheDocument()
  })

  it('links to the director detail page', () => {
    const movie = {
      id: 3,
      title: 'Interstellar',
      release_year: 2014,
      synopsis: null,
      poster_url: null,
      duration_minutes: null,
      status: null,
      director: { id: 11, name: 'Christopher Nolan', bio: null, photo_url: null },
      genres: [{ id: 200, name: 'Sci-Fi' }],
      average_rating: 4.8,
      rating_count: 2000,
    }

    renderWithRouter(<MovieCard movie={movie} />)

    const directorLink = screen.getByRole('link', { name: 'Christopher Nolan' })
    expect(directorLink).toBeInTheDocument()
    expect(directorLink).toHaveAttribute('href', `/directors/${movie.director.id}`)
  })

  it('shows poster image only when poster_url exists', () => {
    const withPoster = {
      id: 4,
      title: 'Tenet',
      release_year: 2020,
      synopsis: null,
      poster_url: 'https://example.com/tenet.jpg',
      duration_minutes: null,
      status: null,
      director: { id: 12, name: 'Christopher Nolan', bio: null, photo_url: null },
      genres: [],
      average_rating: 4.0,
      rating_count: 500,
    }

    renderWithRouter(<MovieCard movie={withPoster} />)
    expect(screen.getByRole('img', { name: 'Tenet' })).toBeInTheDocument()

    const withoutPoster = { ...withPoster, id: 5, title: 'Dunkirk', poster_url: null }
    renderWithRouter(<MovieCard movie={withoutPoster} />)
    expect(screen.queryByRole('img', { name: 'Dunkirk' })).not.toBeInTheDocument()
  })
})


