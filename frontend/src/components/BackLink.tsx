import { Link } from 'react-router-dom'

interface BackLinkProps {
  to: string
  children?: string
  className?: string
}

export default function BackLink({ to, children = '← Back', className = '' }: BackLinkProps) {
  return (
    <Link to={to} className={`text-purple-400 hover:text-purple-300 mb-6 inline-block ${className}`}>
      {children}
    </Link>
  )
}


