import { Link } from 'react-router-dom'

interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary'
  onClick?: () => void
  to?: string
}

export default function Button({ children, variant = 'primary', onClick, to }: ButtonProps) {
  const baseClasses = "px-8 py-4 font-semibold rounded-lg transition duration-200"
  
  const variants = {
    primary: "bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg hover:shadow-purple-500/50 transform hover:scale-105",
    secondary: "bg-white/10 backdrop-blur-sm text-white border border-white/20 hover:bg-white/20"
  }

  const className = `${baseClasses} ${variants[variant]}`

  if (to) {
    return (
      <Link to={to} className={className}>
        {children}
      </Link>
    )
  }

  return (
    <button 
      onClick={onClick}
      className={className}
    >
      {children}
    </button>
  )
}

