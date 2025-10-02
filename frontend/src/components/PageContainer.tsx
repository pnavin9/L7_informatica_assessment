import type { PropsWithChildren } from 'react'

interface PageContainerProps {
  className?: string
}

export default function PageContainer({ children, className = '' }: PropsWithChildren<PageContainerProps>) {
  return (
    <main className={`container mx-auto px-4 py-8 ${className}`}>
      {children}
    </main>
  )
}


