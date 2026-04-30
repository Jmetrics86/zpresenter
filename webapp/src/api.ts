import type { ValidateResult } from './types'

async function handleResponse(res: Response) {
  if (!res.ok) {
    let detail: unknown
    try {
      detail = await res.json()
    } catch {
      detail = await res.text()
    }
    throw new Error(
      typeof detail === 'object' ? JSON.stringify(detail, null, 2) : String(detail),
    )
  }
  return res
}

export async function validateDeck(raw: unknown): Promise<ValidateResult> {
  const res = await handleResponse(
    await fetch('/api/decks/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(raw),
    }),
  )
  return res.json()
}

export async function exportPptx(deck: unknown): Promise<void> {
  const res = await handleResponse(
    await fetch('/api/decks/export-pptx', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(deck),
    }),
  )
  const blob = await res.blob()
  const disposition = res.headers.get('Content-Disposition') ?? ''
  const match = disposition.match(/filename="?([^";]+)"?/)
  const filename = match ? match[1] : 'deck.pptx'
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

export async function listExamples(): Promise<string[]> {
  const res = await fetch('/api/examples')
  if (!res.ok) return []
  return res.json()
}

export async function loadExample(name: string): Promise<unknown> {
  const res = await handleResponse(await fetch(`/api/examples/${name}`))
  return res.json()
}

export async function fetchIcons(): Promise<{ id: string; char: string }[]> {
  const res = await fetch('/api/icons')
  if (!res.ok) return []
  return res.json()
}

export async function fetchModels(): Promise<import('./types').ModelsResponse | null> {
  const res = await fetch('/api/models')
  if (!res.ok) return null
  return res.json()
}

/**
 * Stream LLM-improved slide JSON from the server.
 *
 * Yields ``ImproveEvent`` objects:
 * - ``{type: "delta", text: "..."}`` — incremental token
 * - ``{type: "done", buffer: "..."}`` — streaming complete
 * - ``{type: "error", message: "..."}`` — server-side error
 *
 * Use ``for await (const event of streamImproveSlide(req)) { ... }``
 */
export async function* streamImproveSlide(
  req: import('./types').ImproveRequest,
): AsyncGenerator<import('./types').ImproveEvent> {
  const body = {
    deck: req.deck,
    slide_index: req.slideIndex,
    instructions: req.instructions,
    provider: req.provider,
    model: req.model,
    api_key: req.apiKey,
  }

  const res = await fetch('/api/slides/improve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => null)
    const detail = err?.detail ?? `HTTP ${res.status}`
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail))
  }

  const reader = res.body!.getReader()
  const decoder = new TextDecoder()
  let lineBuf = ''

  try {
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      lineBuf += decoder.decode(value, { stream: true })
      const lines = lineBuf.split('\n')
      lineBuf = lines.pop() ?? ''
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            yield JSON.parse(line.slice(6)) as import('./types').ImproveEvent
          } catch {
            // skip malformed SSE frame
          }
        }
      }
    }
  } finally {
    reader.releaseLock()
  }
}

/**
 * Stream LLM-generated Deck JSON (SSE). Events match ``ImproveEvent``.
 */
export async function* streamGenerateDeck(
  req: import('./types').GenerateDeckRequest,
): AsyncGenerator<import('./types').ImproveEvent> {
  const body = {
    brief: req.brief,
    slide_count: req.slideCount,
    technical_level: req.technicalLevel ?? null,
    attention_span: req.attentionSpan ?? null,
    provider: req.provider,
    model: req.model,
    api_key: req.apiKey,
  }

  const res = await fetch('/api/decks/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => null)
    const detail = err?.detail ?? `HTTP ${res.status}`
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail))
  }

  const reader = res.body!.getReader()
  const decoder = new TextDecoder()
  let lineBuf = ''

  try {
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      lineBuf += decoder.decode(value, { stream: true })
      const lines = lineBuf.split('\n')
      lineBuf = lines.pop() ?? ''
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            yield JSON.parse(line.slice(6)) as import('./types').ImproveEvent
          } catch {
            // skip malformed SSE frame
          }
        }
      }
    }
  } finally {
    reader.releaseLock()
  }
}
