import type { Movie, MovieDetail, Actor, Director, Genre } from '../types'
import { logger } from './logger'

// Resolve API base URL from environment for production; empty string keeps relative paths for dev proxy
const API_BASE_URL = ((import.meta as any)?.env?.VITE_API_BASE_URL ?? '').replace(/\/$/, '')

type QueryParams = Record<string, string | number | boolean | undefined | null>

function buildQuery(params?: QueryParams): string {
  if (!params) return ''
  const search = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && String(value).length > 0) {
      search.set(key, String(value))
    }
  })
  const query = search.toString()
  return query ? `?${query}` : ''
}

type RequestInterceptor = (input: RequestInfo, init?: RequestInit) => Promise<[RequestInfo, RequestInit?]> | [RequestInfo, RequestInit?]
type ResponseInterceptor = (response: Response) => Promise<Response> | Response

const requestInterceptors: RequestInterceptor[] = []
const responseInterceptors: ResponseInterceptor[] = []

export function addRequestInterceptor(interceptor: RequestInterceptor) {
  requestInterceptors.push(interceptor)
}

export function addResponseInterceptor(interceptor: ResponseInterceptor) {
  responseInterceptors.push(interceptor)
}

type CacheOptions = { cacheTtlMs?: number; cacheKey?: string; cacheByUrl?: boolean }
const responseCache = new Map<string, { expiry: number; data: unknown }>()
const inflight = new Map<string, Promise<unknown>>()

function isGET(init?: RequestInit) {
  return (!init?.method || init.method.toUpperCase() === 'GET')
}

function buildCacheKey(url: string, init?: RequestInit, opts?: CacheOptions) {
  if (opts?.cacheKey) return opts.cacheKey
  if (opts?.cacheByUrl === false) return ''
  const method = (init?.method || 'GET').toUpperCase()
  const body = init?.body ? String(init.body) : ''
  return `${method}:${url}:${body}`
}

async function fetchJSON<T>(url: string, init?: RequestInit & { timeoutMs?: number; signal?: AbortSignal } & CacheOptions): Promise<T> {
  const isAbsolute = /^https?:\/\//i.test(url)
  const finalUrl = isAbsolute ? url : `${API_BASE_URL}${url}`
  let input: RequestInfo = finalUrl
  let options: RequestInit = { ...init }

  for (const interceptor of requestInterceptors) {
    const result = await interceptor(input, options)
    input = result[0]
    options = result[1] ?? options
  }

  const controller = new AbortController()
  const timeout = init?.timeoutMs ?? 15000
  const timer = setTimeout(() => controller.abort(), timeout)

  if (options.signal) {
    const upstream = options.signal
    if (upstream.aborted) controller.abort(upstream.reason)
    else upstream.addEventListener('abort', () => controller.abort(upstream.reason))
  }

  const isGetRequest = isGET(options)
  const defaultTtl = 30_000
  const ttl = (isGetRequest ? (init?.cacheTtlMs ?? defaultTtl) : 0) as number
  const cacheKey = isGetRequest ? buildCacheKey(String(input), options, init) : ''

  if (ttl > 0 && cacheKey) {
    const cached = responseCache.get(cacheKey)
    if (cached && cached.expiry > Date.now()) {
      logger.debug('cache hit', { cacheKey })
      return cached.data as T
    }
    const existing = inflight.get(cacheKey)
    if (existing) {
      logger.debug('inflight dedupe', { cacheKey })
      return existing as Promise<T>
    }
  }

  const doFetch = (async () => {
    let res = await fetch(input, { ...options, signal: controller.signal }).finally(() => clearTimeout(timer))
    for (const interceptor of responseInterceptors) {
      res = await interceptor(res)
    }
    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(text || `Request failed: ${res.status}`)
    }
    const json = (await res.json()) as T
    if (ttl > 0 && cacheKey) {
      responseCache.set(cacheKey, { expiry: Date.now() + ttl, data: json as unknown })
    }
    return json
  })()

  // TODO: Implement a minimal retry/backoff for transient network errors (GET only):
  // - Consider 1-2 retries with exponential backoff (e.g., 250ms, 750ms)
  // - Only retry on network failures/5xx; avoid retrying 4xx
  // - Respect AbortSignal and do not retry if aborted

  if (ttl > 0 && cacheKey) {
    inflight.set(cacheKey, doFetch as Promise<unknown>)
    try {
      const result = await doFetch
      return result
    } finally {
      inflight.delete(cacheKey)
    }
  }

  let response = await doFetch as T
  return response
}

// Movies
export async function getMovies(params?: QueryParams) {
  return fetchJSON<Movie[]>(`/api/movies${buildQuery(params)}`)
}

export async function getMovie(id: string | number) {
  return fetchJSON<MovieDetail>(`/api/movies/${id}`)
}

// Unified OR search via backend
export async function searchMoviesOR(q: string) {
  return fetchJSON<Movie[]>(`/api/movies/search${buildQuery({ q })}`)
}

// Actors
export async function getActors() {
  return fetchJSON<Actor[]>(`/api/actors`)
}

export async function getActor(id: string | number) {
  return fetchJSON<Actor>(`/api/actors/${id}`)
}

// Directors
export async function getDirectors() {
  return fetchJSON<Director[]>(`/api/directors`)
}

export async function getDirector(id: string | number) {
  return fetchJSON<Director>(`/api/directors/${id}`)
}

// Genres
export async function getGenres() {
  return fetchJSON<Genre[]>(`/api/genres`)
}

export const api = {
  fetchJSON,
  getMovies,
  getMovie,
  searchMoviesOR,
  getActors,
  getActor,
  getDirectors,
  getDirector,
  getGenres,
}


