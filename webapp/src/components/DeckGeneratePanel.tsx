import { useState, useCallback, useRef, useEffect } from 'react'
import { Wand2, Check, X, ChevronDown, ChevronUp } from 'lucide-react'
import type { AIProvider, Deck, Finding, ProviderInfo } from '../types'
import { streamGenerateDeck, validateDeck, fetchModels } from '../api'

const STATIC_PROVIDERS: Record<
  AIProvider,
  { label: string; models: string[]; placeholder: string; storageKey: string }
> = {
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

function extractJson(raw: string): string {
  const match = raw.match(/```(?:json)?\s*([\s\S]*?)\s*```/)
  if (match) return match[1].trim()
  const start = raw.indexOf('{')
  const end = raw.lastIndexOf('}')
  if (start >= 0 && end > start) return raw.slice(start, end + 1).trim()
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

interface Props {
  onDeckReady: (deck: Deck, findings: Finding[], formattedJson: string) => void
}

export default function DeckGeneratePanel({ onDeckReady }: Props) {
  const [open, setOpen] = useState(false)
  const [provider, setProvider] = useState<AIProvider>('anthropic')
  const [model, setModel] = useState(STATIC_PROVIDERS.anthropic.models[0])
  const [apiKey, setApiKey] = useState(
    () => localStorage.getItem(STATIC_PROVIDERS.anthropic.storageKey) ?? '',
  )
  const [showKey, setShowKey] = useState(false)
  const [brief, setBrief] = useState('')
  const [slideCount, setSlideCount] = useState(12)
  const [technicalLevel, setTechnicalLevel] = useState<'executive' | 'general' | 'technical' | ''>(
    '',
  )
  const [attentionSpan, setAttentionSpan] = useState<'short' | 'medium' | 'long' | ''>('')
  const [streaming, setStreaming] = useState(false)
  const [buffer, setBuffer] = useState('')
  const [error, setError] = useState('')
  const [done, setDone] = useState(false)
  const [serverInfo, setServerInfo] = useState<Record<string, ProviderInfo>>({})
  const outputRef = useRef<HTMLPreElement>(null)

  useEffect(() => {
    fetchModels()
      .then((r) => {
        if (r) setServerInfo(r.providers)
      })
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (outputRef.current) outputRef.current.scrollTop = outputRef.current.scrollHeight
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

  const handleGenerate = useCallback(async () => {
    setStreaming(true)
    setBuffer('')
    setError('')
    setDone(false)

    try {
      for await (const event of streamGenerateDeck({
        brief: brief.trim(),
        slideCount,
        technicalLevel: technicalLevel || undefined,
        attentionSpan: attentionSpan || undefined,
        provider,
        model,
        apiKey,
      })) {
        if (event.type === 'delta' && event.text) {
          setBuffer((prev) => prev + event.text)
        } else if (event.type === 'done') {
          setDone(true)
          break
        } else if (event.type === 'error') {
          setError(event.message ?? 'Unknown error')
          break
        }
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err))
    } finally {
      setStreaming(false)
    }
  }, [brief, slideCount, technicalLevel, attentionSpan, provider, model, apiKey])

  const handleApply = async () => {
    try {
      const cleaned = extractJson(buffer)
      const raw: unknown = JSON.parse(cleaned)
      const result = await validateDeck(raw)
      onDeckReady(result.deck, result.findings, JSON.stringify(result.deck, null, 2))
      setBuffer('')
      setDone(false)
      setError('')
    } catch (err: unknown) {
      setError(
        `Could not validate generated deck: ${err instanceof Error ? err.message : String(err)}`,
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
  const keyOk = Boolean(apiKey.trim() || serverProviderInfo?.configured)

  return (
    <div className="rounded-xl border border-teal-200 bg-teal-50/40 overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-teal-600 to-cyan-600 text-white text-left"
      >
        <Wand2 size={14} className="shrink-0 text-white/90" />
        <span className="text-xs font-semibold">AI deck generation</span>
        <span className="text-[10px] text-white/70 ml-auto">outline → full JSON</span>
        {open ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
      </button>

      {open && (
        <div className="p-3 space-y-3 border-t border-teal-100">
          <p className="text-[10px] text-slate-600 leading-relaxed">
            Paste notes or an outline. The model returns zpresenter Deck JSON (streaming). Validate
            applies it like <strong>Load Deck</strong>.
          </p>

          <textarea
            value={brief}
            onChange={(e) => setBrief(e.target.value)}
            placeholder="Topic, bullets, pasted brief… (min ~12 characters)"
            rows={4}
            className="w-full text-[11px] border border-teal-200 rounded-lg px-2.5 py-2 resize-none focus:outline-none focus:ring-1 focus:ring-teal-400 text-slate-700 placeholder:text-slate-400"
          />

          <div className="flex flex-wrap gap-2 items-end">
            <div>
              <label className="block text-[10px] font-semibold text-slate-400 uppercase mb-1">
                Slides
              </label>
              <input
                type="number"
                min={3}
                max={35}
                value={slideCount}
                onChange={(e) => {
                  const n = Number(e.target.value)
                  setSlideCount(
                    Number.isFinite(n) ? Math.min(35, Math.max(3, Math.round(n))) : 12,
                  )
                }}
                className="w-16 text-xs border border-slate-200 rounded-lg px-2 py-1"
              />
            </div>
            <div>
              <label className="block text-[10px] font-semibold text-slate-400 uppercase mb-1">
                Audience
              </label>
              <select
                value={technicalLevel}
                onChange={(e) =>
                  setTechnicalLevel(e.target.value as 'executive' | 'general' | 'technical' | '')
                }
                className="text-xs border border-slate-200 rounded-lg px-2 py-1 bg-white max-w-[110px]"
              >
                <option value="">Level — infer</option>
                <option value="executive">Executive</option>
                <option value="general">General</option>
                <option value="technical">Technical</option>
              </select>
            </div>
            <div>
              <label className="block text-[10px] font-semibold text-slate-400 uppercase mb-1">
                &nbsp;
              </label>
              <select
                value={attentionSpan}
                onChange={(e) => setAttentionSpan(e.target.value as typeof attentionSpan)}
                className="text-xs border border-slate-200 rounded-lg px-2 py-1 bg-white max-w-[120px]"
              >
                <option value="">Span — infer</option>
                <option value="short">Short</option>
                <option value="medium">Medium</option>
                <option value="long">Long</option>
              </select>
            </div>
          </div>

          <div className="flex flex-wrap gap-2 items-end pb-2 border-b border-teal-100/80">
            <select
              value={provider}
              onChange={(e) => switchProvider(e.target.value as AIProvider)}
              className="text-xs border border-slate-200 rounded-lg px-2 py-1 bg-white"
            >
              {(Object.keys(STATIC_PROVIDERS) as AIProvider[]).map((p) => (
                <option key={p} value={p}>
                  {STATIC_PROVIDERS[p].label}
                </option>
              ))}
            </select>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="text-xs border border-slate-200 rounded-lg px-2 py-1 bg-white min-w-[140px]"
            >
              {models.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
            <div className="flex-1 min-w-[140px] flex gap-1">
              <input
                type={showKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder={serverProviderInfo?.configured ? '(server key)' : placeholder}
                className="flex-1 text-[11px] border border-slate-200 rounded-lg px-2 py-1 font-mono min-w-0"
              />
              <button
                type="button"
                onClick={() => setShowKey((v) => !v)}
                className="text-[10px] px-2 rounded border border-slate-200 text-slate-500"
              >
                {showKey ? 'hide' : 'show'}
              </button>
              <button
                type="button"
                onClick={saveKey}
                className="text-[10px] px-2 rounded border border-slate-200 text-slate-500"
              >
                save
              </button>
            </div>
            <span className="flex items-center gap-1 text-[10px] text-slate-500">
              <ProviderDot configured={Boolean(serverProviderInfo?.configured)} />
              env key
            </span>
          </div>

          <div className="flex gap-2 items-start">
            <button
              type="button"
              onClick={streaming ? () => setStreaming(false) : handleGenerate}
              disabled={!streaming && (!keyOk || brief.trim().length < 12)}
              className={`px-3 py-2 rounded-lg text-xs font-semibold shrink-0 ${
                streaming
                  ? 'bg-red-500 text-white'
                  : 'bg-teal-600 hover:bg-teal-500 disabled:opacity-40 text-white'
              }`}
            >
              {streaming ? 'Stop' : 'Generate'}
            </button>
          </div>

          {(buffer || error) && (
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] font-semibold text-slate-400 uppercase">
                  {error ? 'Error' : streaming ? 'Streaming' : 'Result'}
                </span>
                {done && !streaming && (
                  <span className="text-[10px] text-emerald-600 font-medium">ready to apply</span>
                )}
              </div>
              {error ? (
                <div className="text-[11px] text-red-700 bg-red-50 border border-red-200 rounded-lg px-2 py-2 whitespace-pre-wrap break-all">
                  {error}
                </div>
              ) : (
                <pre
                  ref={outputRef}
                  className="text-[10px] font-mono bg-slate-950 text-cyan-200 rounded-lg px-2 py-2 max-h-40 overflow-auto whitespace-pre-wrap"
                >
                  {buffer}
                  {streaming && <span className="animate-pulse text-teal-400">▍</span>}
                </pre>
              )}
              {done && !error && (
                <div className="flex gap-2 mt-2">
                  <button
                    type="button"
                    onClick={() => void handleApply()}
                    className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-emerald-600 text-white text-xs font-semibold"
                  >
                    <Check size={12} /> Apply deck
                  </button>
                  <button
                    type="button"
                    onClick={handleDiscard}
                    className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-200 text-slate-700 text-xs font-semibold"
                  >
                    <X size={12} /> Discard
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
