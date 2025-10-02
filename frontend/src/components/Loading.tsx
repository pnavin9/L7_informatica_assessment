type LoadingProps = {
  label?: string
  skeleton?: boolean
}

export default function Loading({ label = 'Loading...', skeleton = false }: LoadingProps) {
  if (skeleton) {
    return (
      <div className="container mx-auto px-4 py-8" aria-busy="true" aria-live="polite" role="status">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {Array.from({ length: 8 }).map((_, idx) => (
            <div
              key={idx}
              className="bg-white/10 backdrop-blur-sm rounded-lg overflow-hidden border border-white/10"
            >
              <div className="w-full h-64 bg-white/5 animate-pulse" />
              <div className="p-6 space-y-3">
                <div className="h-5 bg-white/10 rounded w-3/4 animate-pulse" />
                <div className="h-4 bg-white/10 rounded w-1/2 animate-pulse" />
                <div className="h-4 bg-white/10 rounded w-2/3 animate-pulse" />
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-20 text-center text-white text-xl" aria-live="polite" role="status">
      {label}
    </div>
  )
}


