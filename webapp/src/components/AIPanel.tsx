import { useState, useCallback, useRef, useEffect } from 'react'
import { Sparkles, Check, X, ChevronDown, ChevronUp, RotateCcw } from 'lucide-react'
import type { AIProvider, Deck, ImproveRequest, ProviderInfo, Slide } from '../types'
import { streamImproveSlide, fetchModels } from '../api'

// ---------------------------------------------------------------------------
// Static model catalogue (matches server /api/models)
// ---------------------------------------------------------------------------

const STATIC_PROVIDERS: Record<AIProvider, { label: string; models: string[]; placeholder: string; storageKey: string }> = {
  anthropic: {
    label: 'Anthropic',
    models: ['claude-sonnet-4-5', 'claude-opus-4-7'],
    placeholder: 'sk-ant-…',
    storageKey: 'zp_anthropic_key',
  },
  openai: {
    label: 'OpenAI',
    models: ['gpt-4o', 'gpt-4o-mini', 'o1-mini'],
    placeholder: 'sk-…',
    storageKey: 'zp_openai_key',
  },
  gemini: {
    label: 'Google Gemini',
    models: ['gemini-2.0-flash', 'gemini-1.5-pro'],
    placeholder: 'AIza…',
    storageKey: 'zp_gemini_key',
  },
}

const QUICK_PROMPTS = [
  'Make bullets more concise',
  'Sharpen the title',
  'Executive-friendly tone',
  'Add more impact',
  'Simplify language',
  'Strengthen the narrative',
]

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function extractJson(raw: string): string {
  const match = raw.match(/```(?:json)?\s*([\s\S]*?)\s*```/)
  if (match) return match[1].trim()
  return raw.trim()
}

function ProviderDot({ configured }: { configured: boolean }) {
  return (
    <span
      className={`inline-block w-1.5 h-1.5 rounded-full ${configured ? 'bg-emerald-500' : 'bg-slate-300'}`}
      title={configured ? 'API key found in environment' : 'No server-side key (use your own)'}
    />
  )
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

interface Props {
  deck: Deck
  slideIndex: number
  onApply: (slide: Slide) => void
  onUndo: (() => void) | null
  canUndo: boolean
}

export default function AIPanel({ deck, slideIndex, onApply, onUndo, canUndo }: Props) {
  const [provider, setProvider] = useState<AIProvider>('anthropic')
  const [model, setModel] = useState(STATIC_PROVIDERS.anthropic.models[0])
  const [apiKey, setApiKey] = useState(
    () => localStorage.getItem(STATIC_PROVIDERS.anthropic.storageKey) ?? '',
  )
  const [showKey, setShowKey] = useState(false)
  const [instructions, setInstructions] = useState('')
  const [streaming, setStreaming] = useState(false)
  const [buffer, setBuffer] = useState('')
  const [error, setError] = useState('')
  const [done, setDone] = useState(false)
  const [configOpen, setConfigOpen] = useState(true)
  const [serverInfo, setServerInfo] = useState<Record<string, ProviderInfo>>({})
  const outputRef = useRef<HTMLPreElement>(null)

  // Fetch server-side key status (green dots)
  useEffect(() => {
    fetchModels()
      .then((r) => { if (r) setServerInfo(r.providers) })
      .catch(() => {})
  }, [])

  // Auto-scroll streaming output
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight
    }
  }, [buffer])

  const switchProvider = (p: AIProvider) => {
    setProvider(p)
    setModel(STATIC_PROVIDERS[p].models[0])
    setApiKey(localStorage.getItem(STATIC_PROVIDERS[p].storageKey) ?? '')
    setBuffer('')
    setError('')
    setDone(false)
  }

  const saveKey = () => {
    localStorage.setItem(STATIC_PROVIDERS[provider].storageKey, apiKey)
  }

  const handleImprove = useCallback(async () => {
    setStreaming(true)
    setBuffer('')
    setError('')
    setDone(false)

    const req: ImproveRequest = {
      deck,
      slideIndex,
      instructions,
      provider,
      model,
      apiKey,
    }

    try {
      for await (const event of streamImproveSlide(req)) {
        if (event.type === 'delta' && event.text) {
          setBuffer((prev) => prev + event.text)
        } else if (event.type === 'done') {
          setDone(true)
          setStreaming(false)
          break
        } else if (event.type === 'error') {
          setError(event.message ?? 'Unknown error')
          setStreaming(false)
          break
        }
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err))
      setStreaming(false)
    }
  }, [deck, slideIndex, instructions, provider, model, apiKey])

  const handleAccept = () => {
    try {
      const cleaned = extractJson(buffer)
      const obj = JSON.parse(cleaned) as Slide
      if (!obj.layout) throw new Error('AI response missing "layout" field.')
      onApply(obj)
      setBuffer('')
      setDone(false)
      setError('')
    } catch (err: unknown) {
      setError(
        `Could not parse AI response: ${err instanceof Error ? err.message : String(err)}\n\nRaw output preserved above — copy manually if needed.`,
      )
    }
  }

  const handleDiscard = () => {
    setBuffer('')
    setDone(false)
    setError('')
  }

  const { models, placeholder } = STATIC_PROVIDERS[provider]
  const serverProviderInfo = serverInfo[provider]

  return (
    <div className="w-full max-w-4xl bg-white border border-violet-200 rounded-2xl shadow-lg overflow-hidden animate-slide-up">
      {/* ── Header ─────────────────────────────────────────────────── */}
      <div className="flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-violet-600 to-blue-600">
        <Sparkles size={15} className="text-white/90" />
        <span className="text-sm font-semibold text-white">AI Slide Improver</span>
        <span className="text-xs text-white/50 ml-1">· slide {slideIndex + 1}</span>
        <div className="flex-1" />
        {canUndo && onUndo && (
          <button
            onClick={onUndo}
            className="flex items-center gap-1 text-xs text-white/70 hover:text-white px-2 py-1 rounded-lg hover:bg-white/10 transition-colors"
            title="Undo last AI change"
          >
            <RotateCcw size={12} />
            Undo
          </button>
        )}
        <button
          onClick={() => setConfigOpen((v) => !v)}
          className="p-1.5 rounded-lg hover:bg-white/10 text-white/70 hover:text-white transition-colors"
          title="Toggle config"
        >
          {configOpen ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </button>
      </div>

      <div className="p-4 space-y-3">
        {/* ── Config (collapsible) ────────────────────────────────── */}
        {configOpen && (
          <div className="flex gap-3 flex-wrap items-end pb-3 border-b border-slate-100">
            {/* Provider */}
            <div>
              <label className="block text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                Provider
              </label>
              <select
                value={provider}
                onChange={(e) => switchProvider(e.target.value as AIProvider)}
                className="text-xs border border-slate-200 rounded-lg px-2 py-1.5 bg-white focus:outline-none focus:ring-1 focus:ring-violet-300"
              >
                {(Object.keys(STATIC_PROVIDERS) as AIProvider[]).map((p) => (
                  <option key={p} value={p}>
                    {STATIC_PROVIDERS[p].label}
                  </option>
                ))}
              </select>
            </div>

            {/* Model */}
            <div>
              <label className="block text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                Model
              </label>
              <select
                value={model}
                onChange={(e) => setModel(e.target.value)}
                className="text-xs border border-slate-200 rounded-lg px-2 py-1.5 bg-white focus:outline-none focus:ring-1 focus:ring-violet-300"
              >
                {models.map((m) => (
                  <option key={m} value={m}>{m}</option>
                ))}
              </select>
            </div>

            {/* API Key */}
            <div className="flex-1 min-w-52">
              <label className="flex items-center gap-1.5 text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                API Key
                {serverProviderInfo && (
                  <ProviderDot configured={serverProviderInfo.configured} />
                )}
                {serverProviderInfo?.configured && (
                  <span className="text-emerald-600 font-normal normal-case tracking-normal">
                    server key active
                  </span>
                )}
              </label>
              <div className="flex gap-1.5">
                <input
                  type={showKey ? 'text' : 'password'}
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder={serverProviderInfo?.configured ? '(using server key)' : placeholder}
                  className="flex-1 text-xs border border-slate-200 rounded-lg px-2 py-1.5 font-mono focus:outline-none focus:ring-1 focus:ring-violet-300 min-w-0"
                />
                <button
                  onClick={() => setShowKey((v) => !v)}
                  className="text-[10px] px-2 py-1.5 rounded-lg border border-slate-200 text-slate-400 hover:text-slate-600 transition-colors shrink-0"
                >
                  {showKey ? 'hide' : 'show'}
                </button>
                <button
                  onClick={saveKey}
                  className="text-[10px] px-2 py-1.5 rounded-lg border border-slate-200 text-slate-500 hover:bg-slate-50 transition-colors shrink-0"
                  title="Save to browser localStorage"
                >
                  save
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ── Instructions + Improve button ───────────────────────── */}
        <div>
          <div className="flex gap-2">
            <div className="flex-1">
              <textarea
                value={instructions}
                onChange={(e) => setInstructions(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
                    e.preventDefault()
                    if (!streaming) handleImprove()
                  }
                }}
                placeholder="Instructions (optional) — e.g. make bullets more concise, punchier title…  ⌘↵ to run"
                rows={2}
                className="w-full text-xs border border-slate-200 rounded-xl px-3 py-2 resize-none focus:outline-none focus:ring-1 focus:ring-violet-300 text-slate-700 placeholder:text-slate-300 leading-relaxed"
              />
              {/* Quick prompts */}
              <div className="flex gap-1.5 mt-1.5 flex-wrap">
                {QUICK_PROMPTS.map((p) => (
                  <button
                    key={p}
                    onClick={() => setInstructions(p)}
                    className="text-[10px] px-2 py-0.5 rounded-full bg-violet-50 text-violet-600 hover:bg-violet-100 transition-colors border border-violet-100 whitespace-nowrap"
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            {/* Improve / Stop button */}
            <button
              onClick={streaming ? () => { setStreaming(false) } : handleImprove}
              disabled={!apiKey.trim() && !serverInfo[provider]?.configured}
              className={`self-start px-4 py-2 rounded-xl text-sm font-semibold transition-all shrink-0 ${
                streaming
                  ? 'bg-red-500 hover:bg-red-400 text-white'
                  : 'bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed text-white'
              }`}
              title={!apiKey.trim() && !serverInfo[provider]?.configured ? 'Enter an API key to use AI' : 'Improve slide (⌘↵)'}
            >
              {streaming ? (
                <span className="flex items-center gap-1.5">
                  <span className="w-2 h-2 bg-white rounded-full animate-pulse" />
                  Stop
                </span>
              ) : (
                <span className="flex items-center gap-1.5">
                  <Sparkles size={13} />
                  Improve
                </span>
              )}
            </button>
          </div>
        </div>

        {/* ── Streaming output ────────────────────────────────────── */}
        {(buffer || error) && (
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
                {error ? 'Error' : streaming ? 'Streaming' : 'Result'}
              </span>
              {streaming && (
                <span className="text-[10px] text-violet-500 animate-pulse font-medium">● live</span>
              )}
              {done && !streaming && (
                <span className="text-[10px] text-emerald-600 font-medium">✓ ready to apply</span>
              )}
            </div>

            {error ? (
              <div className="text-xs text-red-600 bg-red-50 border border-red-200 rounded-xl px-3 py-2 font-mono whitespace-pre-wrap break-all">
                {error}
              </div>
            ) : (
              <pre
                ref={outputRef}
                className="text-[11px] font-mono bg-slate-950 text-emerald-300 rounded-xl px-4 py-3 overflow-auto max-h-52 whitespace-pre-wrap leading-relaxed"
              >
                {buffer}
                {streaming && <span className="animate-pulse text-violet-400">▍</span>}
              </pre>
            )}

            {/* Accept / Discard */}
            {done && !error && (
              <div className="flex items-center gap-2 mt-3">
                <button
                  onClick={handleAccept}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold transition-colors"
                >
                  <Check size={14} />
                  Apply to slide
                </button>
                <button
                  onClick={handleDiscard}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 text-sm font-semibold transition-colors"
                >
                  <X size={14} />
                  Discard
                </button>
                <p className="text-[10px] text-slate-400 ml-1 leading-relaxed">
                  Applied slides can be improved further. Export PPTX at any time.
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
