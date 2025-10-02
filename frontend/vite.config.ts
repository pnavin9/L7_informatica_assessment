import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ command, mode }) => {
  const isDev = command === 'serve' && mode !== 'production'
  return {
    plugins: [react(), tailwindcss()],
    server: {
      port: 5173,
      proxy: isDev
        ? {
            '/api': {
              target: 'https://l7informaticaassessment-production.up.railway.app',
              changeOrigin: true,
              secure: true,
              configure(proxy) {
                const write = (line: string) => console.log(line)
                const p = proxy as any
                p.on('proxyReq', (_proxyReq: any, req: any) => {
                  ;(req as any)._startTime = Date.now()
                  const method = (req.method || 'GET').toUpperCase()
                  const url = req.url || ''
                  write(`[proxy] → ${method} ${url}`)
                })
                p.on('proxyRes', (proxyRes: any, req: any) => {
                  const method = (req.method || 'GET').toUpperCase()
                  const url = req.url || ''
                  const status = proxyRes.statusCode || 0
                  const start = (req as any)._startTime as number | undefined
                  const ms = typeof start === 'number' ? (Date.now() - start) : 0
                  write(`[proxy] ← ${method} ${url} -> ${status} ${ms}ms`)
                })
                p.on('error', (err: any, req: any) => {
                  const method = (req?.method || 'GET').toUpperCase()
                  const url = req?.url || ''
                  write(`[proxy] ✖ ${method} ${url} -> ERROR ${String(err?.message || err)}`)
                })
              }
            }
          }
        : undefined,
    },
    preview: {
      // Ensure preview never proxies; it should hit the real API via VITE_API_BASE_URL
      proxy: undefined,
    },
    build: {
      // optional: keep source maps hidden for prod debugging tools
      // sourcemap: 'hidden',
    },
  }
})
