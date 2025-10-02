import { Component, type ReactNode } from 'react'
import { logger } from '../services/logger'

interface ErrorBoundaryProps {
  children: ReactNode
  fallback?: ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
}

export default class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  componentDidCatch(error: unknown) {
    logger.error('Uncaught error in UI', { error: error as object })
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div className="container mx-auto px-4 py-20 text-center">
          <h1 className="text-3xl font-bold text-red-400 mb-4">Something went wrong</h1>
          <p className="text-gray-300">Please refresh the page and try again.</p>
        </div>
      )
    }
    return this.props.children
  }
}


