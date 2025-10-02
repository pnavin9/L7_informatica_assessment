import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Header from './components/Header';
import ErrorBoundary from './components/ErrorBoundary';
import Hero from './components/Hero';
import FeatureCard from './components/FeatureCard';
import Footer from './components/Footer';
import MoviesPage from './pages/MoviesPage';
import MovieDetailPage from './pages/MovieDetailPage';
import ActorsPage from './pages/ActorsPage';
import ActorDetailPage from './pages/ActorDetailPage';
import DirectorsPage from './pages/DirectorsPage';
import DirectorDetailPage from './pages/DirectorDetailPage';

interface Feature {
  icon: string;
  title: string;
  description: string;
}

const features: Feature[] = [
  {
    icon: '📚',
    title: 'Vast Library',
    description: 'Explore thousands of movies, from classics to the latest blockbusters.'
  },
  {
    icon: '🔍',
    title: 'Smart Filters',
    description: 'Find exactly what you want with advanced filtering by genre, director, and actors.'
  },
  {
    icon: '⚡',
    title: 'Blazing Fast',
    description: 'Powered by FastAPI and Vite, enjoy a seamless and responsive experience.'
  },
];

function HomePage() {
  return (
    <main className="container mx-auto px-4 py-8 text-white font-sans">
      <Hero />
      <section id="features" className="grid md:grid-cols-3 gap-8 mt-16">
        {features.map((feature, index) => (
          <FeatureCard key={index} icon={feature.icon} title={feature.title} description={feature.description} />
        ))}
      </section>
    </main>
  );
}

function App() {
  return (
    <BrowserRouter>
      <ErrorBoundary>
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
          <Header />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/movies" element={<MoviesPage />} />
            <Route path="/movies/:id" element={<MovieDetailPage />} />
            <Route path="/actors" element={<ActorsPage />} />
            <Route path="/actors/:id" element={<ActorDetailPage />} />
            <Route path="/directors" element={<DirectorsPage />} />
            <Route path="/directors/:id" element={<DirectorDetailPage />} />
          </Routes>
          <Footer />
        </div>
      </ErrorBoundary>
    </BrowserRouter>
  );
}

export default App;
