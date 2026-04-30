import { memo } from 'react'
import type { Deck, Finding, Slide } from '../types'
import { themeColors, titleColor, CHART_COLORS } from '../theme'

interface Props {
  activeTab: 'load' | 'slides'
  onTabChange: (tab: 'load' | 'slides') => void
  deck: Deck | null
  currentIdx: number
  onSelectSlide: (idx: number) => void
  jsonText: string
  onJsonChange: (text: string) => void
  onValidate: () => void
  loading: boolean
  errors: string
  findings: Finding[]
  examples: string[]
  onLoadExample: (name: string) => void
}

/**
 * Layout-aware mini preview for the thumbnail strip.
 *
 * Uses only SVG + plain HTML — zero recharts — so even 30-slide decks with
 * charts are fast. Each card approximates the visual rhythm of its layout type.
 */
const SlideThumbnail = memo(function SlideThumbnail({
  slide,
  deck,
}: {
  slide: Slide
  deck: Deck
}) {
  const colors = themeColors(deck.theme)
  const tc = titleColor(slide)
  const title = slide.title ?? slide.quote ?? ''
  const hasCustomColor = !!slide.title_color_hex
  const accentColor = hasCustomColor ? tc : colors.accent

  // Chart slides: SVG sparkline
  if (slide.layout === 'chart_bar' || slide.layout === 'chart_line') {
    const values = slide.chart_series?.[0]?.values ?? [0.4, 0.6, 0.5, 0.8, 0.7]
    const max = Math.max(...values, 1)
    const isLine = slide.layout === 'chart_line'
    const W = 88
    const chartH = 26
    const barW = Math.max(2, (W - 8) / values.length - 1.5)
    const pts = values
      .map((v, i) => {
        const x = 4 + i * (barW + 1.5) + barW / 2
        const y = chartH - 2 - (v / max) * (chartH - 4)
        return `${x.toFixed(1)},${y.toFixed(1)}`
      })
      .join(' ')

    return (
      <div
        className="h-full w-full bg-white flex flex-col overflow-hidden"
        style={{ borderTop: `2px solid ${accentColor}` }}
      >
        <p className="px-1.5 pt-1 text-[6px] font-bold truncate" style={{ color: tc }}>{title}</p>
        <div className="flex-1 px-1 pb-1 min-h-0">
          <svg viewBox={`0 0 ${W} ${chartH}`} className="w-full h-full">
            {isLine ? (
              <polyline points={pts} fill="none" stroke={CHART_COLORS[0]} strokeWidth="1.5" strokeLinejoin="round" />
            ) : (
              values.map((v, i) => {
                const x = 4 + i * (barW + 1.5)
                const h = Math.max(2, (v / max) * (chartH - 4))
                return (
                  <rect key={i} x={x} y={chartH - 2 - h} width={barW} height={h} rx="0.5" fill={CHART_COLORS[0]} opacity="0.75" />
                )
              })
            )}
          </svg>
        </div>
      </div>
    )
  }

  // Section
  if (slide.layout === 'section') {
    const bg = hasCustomColor ? `${tc}12` : 'white'
    return (
      <div
        className="h-full w-full flex flex-col items-center justify-center text-center px-1 overflow-hidden"
        style={{ background: bg, borderTop: `2px solid ${accentColor}` }}
      >
        <p className="text-[6.5px] font-bold leading-tight line-clamp-2" style={{ color: tc }}>{title}</p>
        <div className="mt-0.5 h-0.5 w-5 rounded-full" style={{ background: accentColor }} />
      </div>
    )
  }

  // Title / opening
  if (slide.layout === 'title') {
    return (
      <div
        className="h-full w-full bg-white flex flex-col overflow-hidden"
        style={{ borderTop: `2px solid ${accentColor}` }}
      >
        <div className="flex-1 flex flex-col items-center justify-center text-center px-1">
          <p className="text-[6.5px] font-bold leading-tight line-clamp-2" style={{ color: tc }}>{title}</p>
          {slide.subtitle && (
            <p className="text-[5px] mt-0.5 leading-tight line-clamp-1 opacity-70" style={{ color: colors.muted }}>
              {slide.subtitle}
            </p>
          )}
        </div>
        <div className="mx-1.5 mb-1 h-px bg-slate-200" />
      </div>
    )
  }

  // Quote
  if (slide.layout === 'quote') {
    return (
      <div className="h-full w-full bg-white flex items-center px-1 gap-1 overflow-hidden">
        <div className="w-0.5 self-stretch my-1.5 rounded-full shrink-0" style={{ background: accentColor }} />
        <p className="text-[5.5px] italic leading-tight line-clamp-4 text-slate-700">
          &ldquo;{title}&rdquo;
        </p>
      </div>
    )
  }

  // Two-column
  if (slide.layout === 'two_column') {
    const L = (slide.bullets_left ?? []).slice(0, 4)
    const R = (slide.bullets_right ?? []).slice(0, 4)
    return (
      <div
        className="h-full w-full bg-white flex flex-col px-1.5 py-1 overflow-hidden"
        style={{ borderTop: `2px solid ${accentColor}` }}
      >
        <p className="text-[6.5px] font-bold truncate shrink-0" style={{ color: tc }}>{title}</p>
        <div className="flex-1 flex gap-0.5 mt-0.5 min-h-0 overflow-hidden">
          <div className="flex-1 space-y-px overflow-hidden">
            {L.map((b, i) => <p key={i} className="text-[4px] text-slate-600 truncate">▸ {b}</p>)}
          </div>
          <div className="w-px bg-slate-200 shrink-0" />
          <div className="flex-1 space-y-px overflow-hidden">
            {R.map((b, i) => <p key={i} className="text-[4px] text-slate-600 truncate">▸ {b}</p>)}
          </div>
        </div>
      </div>
    )
  }

  // title_content (default)
  const bullets = (slide.bullets ?? []).slice(0, 5)
  return (
    <div
      className="h-full w-full bg-white flex flex-col px-1.5 py-1 overflow-hidden"
      style={{ borderTop: `2px solid ${accentColor}` }}
    >
      <p className="text-[6.5px] font-bold truncate shrink-0" style={{ color: tc }}>{title}</p>
      <div className="flex items-center mt-0.5 mb-0.5 shrink-0">
        <div className="h-px w-3 rounded-full" style={{ background: accentColor }} />
        <div className="flex-1 h-px bg-slate-200 ml-0.5" />
      </div>
      <div className="flex-1 space-y-px overflow-hidden">
        {bullets.map((b, i) => <p key={i} className="text-[4px] text-slate-600 truncate">▸ {b}</p>)}
      </div>
    </div>
  )
})

function FindingBadge({ f }: { f: Finding }) {
  const cls =
    f.severity === 'error'
      ? 'bg-red-50 text-red-700 border-red-200'
      : f.severity === 'warn'
        ? 'bg-amber-50 text-amber-700 border-amber-200'
        : 'bg-blue-50 text-blue-700 border-blue-200'
  return (
    <div className={`text-[10px] px-2 py-1 rounded border ${cls} leading-snug`}>
      {f.slide_index != null && <span className="font-bold">#{f.slide_index + 1}&nbsp;</span>}
      {f.message}
    </div>
  )
}

export default function Sidebar({
  activeTab,
  onTabChange,
  deck,
  currentIdx,
  onSelectSlide,
  jsonText,
  onJsonChange,
  onValidate,
  loading,
  errors,
  findings,
  examples,
  onLoadExample,
}: Props) {
  const errCount = findings.filter((f) => f.severity === 'error').length
  const warnCount = findings.filter((f) => f.severity === 'warn').length
  const infoCount = findings.length - errCount - warnCount

  return (
    <aside className="w-72 bg-white border-r border-slate-200 flex flex-col shrink-0">
      {/* Tab bar */}
      <div className="flex border-b border-slate-200 shrink-0">
        {(['load', 'slides'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => onTabChange(tab)}
            className={`flex-1 py-2.5 text-xs font-semibold uppercase tracking-wider transition-colors border-b-2 -mb-px ${
              activeTab === tab
                ? 'text-blue-600 border-blue-600'
                : 'text-slate-400 border-transparent hover:text-slate-600'
            }`}
          >
            {tab === 'load'
              ? 'Load'
              : `Slides${deck ? ` (${deck.slides.length})` : ''}`}
          </button>
        ))}
      </div>

      {/* ── Load tab ─────────────────────────────────────────────────── */}
      {activeTab === 'load' && (
        <div className="flex-1 overflow-y-auto flex flex-col p-3 gap-3">
          {examples.length > 0 && (
            <div>
              <label className="block text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                Examples
              </label>
              <select
                className="w-full text-xs border border-slate-200 rounded-lg px-2 py-2 bg-white text-slate-700 focus:outline-none focus:ring-1 focus:ring-blue-300 cursor-pointer"
                defaultValue=""
                onChange={(e) => {
                  if (e.target.value) onLoadExample(e.target.value)
                  e.target.value = ''
                }}
              >
                <option value="">Pick an example…</option>
                {examples.map((ex) => (
                  <option key={ex} value={ex}>{ex}</option>
                ))}
              </select>
            </div>
          )}

          <div className="flex flex-col flex-1">
            <label className="block text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
              Deck JSON
            </label>
            <textarea
              value={jsonText}
              onChange={(e) => onJsonChange(e.target.value)}
              placeholder={'{\n  "title": "My deck",\n  "slides": [...]\n}'}
              className="flex-1 min-h-[180px] text-[11px] font-mono border border-slate-200 rounded-lg px-2.5 py-2 resize-none focus:outline-none focus:ring-1 focus:ring-blue-300 text-slate-700 placeholder:text-slate-300 leading-relaxed"
              spellCheck={false}
            />
          </div>

          <button
            onClick={onValidate}
            disabled={loading || !jsonText.trim()}
            className="w-full py-2 rounded-lg bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-semibold transition-colors"
          >
            {loading ? 'Loading…' : 'Load Deck'}
          </button>

          {errors && (
            <div className="text-[10px] text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2 font-mono whitespace-pre-wrap break-all">
              {errors}
            </div>
          )}

          {findings.length > 0 && (
            <div className="space-y-1.5">
              <p className="text-[10px] font-semibold text-slate-500">
                {errCount > 0 && (
                  <span className="text-red-600">{errCount} error{errCount > 1 ? 's' : ''}&nbsp;</span>
                )}
                {warnCount > 0 && (
                  <span className="text-amber-600">{warnCount} warning{warnCount > 1 ? 's' : ''}&nbsp;</span>
                )}
                {infoCount > 0 && <span className="text-blue-600">{infoCount} info</span>}
              </p>
              {findings.slice(0, 6).map((f, i) => (
                <FindingBadge key={i} f={f} />
              ))}
              {findings.length > 6 && (
                <p className="text-[10px] text-slate-400">+{findings.length - 6} more findings</p>
              )}
            </div>
          )}
        </div>
      )}

      {/* ── Slides tab ───────────────────────────────────────────────── */}
      {activeTab === 'slides' && (
        <div className="flex-1 overflow-y-auto py-2 px-2">
          {deck ? (
            <div className="space-y-1">
              {deck.slides.map((slide, i) => {
                const active = currentIdx === i
                return (
                  <button
                    key={i}
                    onClick={() => onSelectSlide(i)}
                    className={`w-full flex items-center gap-2.5 px-2 py-1.5 rounded-lg text-left transition-colors ${
                      active ? 'bg-blue-50 ring-1 ring-blue-200' : 'hover:bg-slate-50'
                    }`}
                  >
                    <span className="text-[10px] font-medium text-slate-400 w-5 text-right shrink-0">
                      {i + 1}
                    </span>
                    {/* Thumbnail — 88×49.5 (16:9), layout-aware, no recharts */}
                    <div
                      className={`rounded-md overflow-hidden shrink-0 border ${
                        active ? 'border-blue-300' : 'border-slate-200'
                      }`}
                      style={{ width: 88, height: 49.5 }}
                    >
                      <SlideThumbnail slide={slide} deck={deck} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-[11px] font-semibold text-slate-700 truncate leading-tight">
                        {slide.title ?? slide.quote ?? '(untitled)'}
                      </p>
                      <p className="text-[10px] text-slate-400 mt-0.5">{slide.layout}</p>
                    </div>
                  </button>
                )
              })}
            </div>
          ) : (
            <div className="flex items-center justify-center h-24 text-slate-400 text-xs">
              Load a deck first
            </div>
          )}
        </div>
      )}
    </aside>
  )
}
