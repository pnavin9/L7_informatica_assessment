import type { PropsWithChildren } from 'react'

interface CardProps {
  className?: string
}

export default function Card({ children, className = '' }: PropsWithChildren<CardProps>) {
  return (
    <div className={`bg-white/10 backdrop-blur-sm rounded-lg border border-white/10 overflow-hidden ${className}`}>
      {children}
    </div>
  )
}


