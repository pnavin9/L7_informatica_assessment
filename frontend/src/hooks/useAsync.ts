import { useCallback, useEffect, useRef, useState } from 'react'
import { logger } from '../services/logger'

type AsyncState<T> = {
  data: T | null
  error: string | null
  loading: boolean
}

export function useAsync<T>(asyncFn: (signal?: AbortSignal) => Promise<T>, deps: unknown[] = []) {
  const [state, setState] = useState<AsyncState<T>>({ data: null, error: null, loading: true })
  const fnRef = useRef(asyncFn)
  fnRef.current = asyncFn

  const run = useCallback(() => {
    const controller = new AbortController()
    setState(prev => ({ ...prev, loading: true, error: null }))
    fnRef.current(controller.signal)
      .then((result) => setState({ data: result, error: null, loading: false }))
      .catch((err: unknown) => {
        if ((err as any)?.name === 'AbortError') return
        const message = (err as Error)?.message || 'Request failed'
        logger.error('useAsync error', { message, err: err as object })
        setState({ data: null, error: message, loading: false })
      })
    return () => controller.abort()
  }, [])

  useEffect(run, deps)

  return { ...state, reload: run }
}

export type UseAsyncReturn<T> = ReturnType<typeof useAsync<T>>


