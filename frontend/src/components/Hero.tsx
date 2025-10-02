import Button from './Button.js'

export default function Hero() {
  return (
    <div className="max-w-4xl mx-auto text-center">
      <h2 className="text-5xl md:text-6xl font-bold text-white mb-6">
        Discover Your Next
        <span className="block bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
          Favorite Movie
        </span>
      </h2>
      <p className="text-xl text-gray-300 mb-8">
        Explore thousands of movies, discover talented actors and acclaimed directors.
        Filter, search, and find exactly what you're looking for.
      </p>
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <Button variant="primary" to="/movies">Browse Movies</Button>
        <Button variant="secondary">Learn More</Button>
      </div>
    </div>
  )
}

