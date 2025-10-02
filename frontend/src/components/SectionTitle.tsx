import type { PropsWithChildren } from 'react'

interface SectionTitleProps {
  as?: 'h1' | 'h2' | 'h3'
  className?: string
}

export default function SectionTitle({ as = 'h2', className = '', children }: PropsWithChildren<SectionTitleProps>) {
  const Tag = as
  const base = as === 'h1' ? 'text-4xl font-bold text-white mb-8' : as === 'h2' ? 'text-3xl font-bold text-white mb-6' : 'text-xl font-semibold text-purple-400 mb-2'
  return <Tag className={`${base} ${className}`}>{children}</Tag>
}


