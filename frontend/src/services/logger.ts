type LogLevel = 'debug' | 'info' | 'warn' | 'error'

interface LogEvent {
  level: LogLevel
  message: string
  context?: Record<string, unknown>
  timestamp: string
}

function formatEvent(level: LogLevel, message: string, context?: Record<string, unknown>): LogEvent {
  return {
    level,
    message,
    context,
    timestamp: new Date().toISOString(),
  }
}

function writeToConsole(event: LogEvent) {
  // Allowed only here via eslint override
  const parts = [
    `[${event.timestamp}]`,
    event.level.toUpperCase(),
    event.message,
  ]
  const payload = event.context ? [...parts, event.context] : parts
  switch (event.level) {
    case 'debug':
      // eslint-disable-next-line no-console
      console.debug(...payload)
      break
    case 'info':
      // eslint-disable-next-line no-console
      console.info(...payload)
      break
    case 'warn':
      // eslint-disable-next-line no-console
      console.warn(...payload)
      break
    case 'error':
      // eslint-disable-next-line no-console
      console.error(...payload)
      break
  }
}

function emit(event: LogEvent) {
  if (import.meta.env.DEV) {
    writeToConsole(event)
    return
  }
  // In production: no-op for now. Hook here to send to a collector if needed.
}

export const logger = {
  debug(message: string, context?: Record<string, unknown>) {
    emit(formatEvent('debug', message, context))
  },
  info(message: string, context?: Record<string, unknown>) {
    emit(formatEvent('info', message, context))
  },
  warn(message: string, context?: Record<string, unknown>) {
    emit(formatEvent('warn', message, context))
  },
  error(message: string, context?: Record<string, unknown>) {
    emit(formatEvent('error', message, context))
  },
}

export type Logger = typeof logger


