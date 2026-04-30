import { X } from 'lucide-react'
import type { Deck, Slide } from '../types'
import { themeColors, titleColor, CHART_COLORS } from '../theme'

interface Props {
  deck: Deck
  currentIdx: number
  onSelectSlide: (idx: number) => void
  onClose: () => void
}

/** Layout-aware mini card for the overview grid — no recharts dependency. */
function MiniPreview({
  slide,
  deck,
}: {
  slide: Slide
  deck: Deck
}) {
  const colors = themeColors(deck.theme)
  const tc = titleColor(slide)

  const hasCustomColor = !!slide.title_color_hex
  const borderTopColor = hasCustomColor ? tc : colors.accent

  const titleText = slide.title ?? slide.quote ?? ''

  // Chart sparkline — simple SVG bars/polyline (no recharts, no external deps)
  if (slide.layout === 'chart_bar' || slide.layout === 'chart_line') {
    const series = slide.chart_series ?? []
    const values = series[0]?.values ?? []
    const cats = slide.chart_categories ?? []
    const max = Math.max(...values, 1)
    const W = 200
    const H = 60
    const barW = values.length > 0 ? (W - 8) / values.length - 2 : 20
    const isLine = slide.layout === 'chart_line'

    const points = values
      .map((v, i) => {
        const x = 4 + i * (barW + 2) + barW / 2
        const y = H - 4 - ((v / max) * (H - 10))
        return `${x},${y}`
      })
      .join(' ')

    return (
      <div className="h-full w-full bg-white flex flex-col" style={{ borderTop: `3px solid ${colors.accent}` }}>
        <div className="px-2 pt-1.5 pb-0.5 shrink-0">
          <p className="text-[7px] font-bold truncate" style={{ color: tc }}>{titleText}</p>
          {slide.subtitle && (
            <p className="text-[5.5px] truncate" style={{ color: colors.muted }}>{slide.subtitle}</p>
          )}
        </div>
        <div className="flex-1 px-2 pb-1.5 min-h-0">
          <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-full">
            {isLine ? (
              <>
                <polyline
                  points={points}
                  fill="none"
                  stroke={CHART_COLORS[0]}
                  strokeWidth="2"
                  strokeLinejoin="round"
                />
                {values.map((v, i) => {
                  const x = 4 + i * (barW + 2) + barW / 2
                  const y = H - 4 - ((v / max) * (H - 10))
                  return <circle key={i} cx={x} cy={y} r="3" fill={CHART_COLORS[0]} />
                })}
              </>
            ) : (
              values.map((v, i) => {
                const x = 4 + i * (barW + 2)
                const h = (v / max) * (H - 10)
                const y = H - 4 - h
                return (
                  <rect
                    key={i}
                    x={x}
                    y={y}
                    width={barW}
                    height={h}
                    rx="1"
                    fill={CHART_COLORS[0]}
                    opacity="0.8"
                  />
                )
              })
            )}
          </svg>
          {cats.length > 0 && (
            <div className="flex justify-between mt-px">
              {cats.slice(0, Math.min(cats.length, 6)).map((c, i) => (
                <span key={i} className="text-[4px]" style={{ color: colors.muted }}>{c}</span>
              ))}
            </div>
          )}
        </div>
      </div>
    )
  }

  // Section
  if (slide.layout === 'section') {
    const sectionBg = hasCustomColor ? `${tc}12` : 'white'
    return (
      <div
        className="h-full w-full flex flex-col items-center justify-center text-center px-2"
        style={{ background: sectionBg, borderTop: `3px solid ${borderTopColor}` }}
      >
        <p className="text-[8px] font-bold leading-tight" style={{ color: tc }}>{titleText}</p>
        <div className="mt-1 h-0.5 w-8 rounded-full" style={{ background: borderTopColor }} />
      </div>
    )
  }

  // Title / opening
  if (slide.layout === 'title') {
    return (
      <div
        className="h-full w-full bg-white flex flex-col"
        style={{ borderTop: `3px solid ${colors.accent}` }}
      >
        <div className="flex-1 flex flex-col items-center justify-center text-center px-2">
          <p className="text-[8px] font-bold leading-tight" style={{ color: tc }}>{titleText}</p>
          {slide.subtitle && (
            <p className="text-[5.5px] mt-0.5 leading-tight" style={{ color: colors.muted }}>
              {slide.subtitle}
            </p>
          )}
        </div>
        <div className="mx-2 mb-1 h-px bg-slate-200" />
      </div>
    )
  }

  // Quote
  if (slide.layout === 'quote') {
    return (
      <div className="h-full w-full bg-white flex items-center px-2 gap-1.5">
        <div className="w-0.5 self-stretch my-2 rounded-full shrink-0" style={{ background: colors.accent }} />
        <p
          className="text-[7px] italic leading-tight line-clamp-4"
          style={{ color: '#1F2937' }}
        >
          &ldquo;{titleText}&rdquo;
        </p>
      </div>
    )
  }

  // Two-column
  if (slide.layout === 'two_column') {
    const leftBullets = slide.bullets_left ?? []
    const rightBullets = slide.bullets_right ?? []
    return (
      <div
        className="h-full w-full bg-white flex flex-col px-2 py-1.5"
        style={{ borderTop: `3px solid ${colors.accent}` }}
      >
        <p className="text-[7px] font-bold truncate shrink-0" style={{ color: tc }}>{titleText}</p>
        <div className="flex-1 flex gap-1 mt-1 min-h-0">
          <div className="flex-1 space-y-0.5 overflow-hidden">
            {leftBullets.slice(0, 5).map((b, i) => (
              <p key={i} className="text-[4.5px] text-slate-600 truncate">▸ {b}</p>
            ))}
          </div>
          <div className="w-px bg-slate-200 shrink-0" />
          <div className="flex-1 space-y-0.5 overflow-hidden">
            {rightBullets.slice(0, 5).map((b, i) => (
              <p key={i} className="text-[4.5px] text-slate-600 truncate">▸ {b}</p>
            ))}
          </div>
        </div>
      </div>
    )
  }

  // title_content (default)
  const bullets = slide.bullets ?? []
  return (
    <div
      className="h-full w-full bg-white flex flex-col px-2 py-1.5"
      style={{ borderTop: `3px solid ${colors.accent}` }}
    >
      <p className="text-[7px] font-bold truncate shrink-0" style={{ color: tc }}>{titleText}</p>
      <div className="flex items-center mt-0.5 mb-1 shrink-0">
        <div className="h-0.5 w-4 rounded-full" style={{ background: colors.accent }} />
        <div className="flex-1 h-px bg-slate-200 ml-0.5" />
      </div>
      <div className="flex-1 space-y-0.5 overflow-hidden">
        {bullets.slice(0, 6).map((b, i) => (
          <p key={i} className="text-[4.5px] text-slate-600 truncate">▸ {b}</p>
        ))}
      </div>
    </div>
  )
}

/**
 * Overview grid — Slidev's `O` key equivalent.
 *
 * Shows all slides as clickable thumbnails. Active slide is highlighted.
 * Layout-aware: each card renders an accurate mini-preview (no recharts).
 */
export default function OverviewModal({ deck, currentIdx, onSelectSlide, onClose }: Props) {
  return (
    <div
      className="fixed inset-0 z-50 bg-slate-950/95 overflow-auto p-8 animate-overview-in"
      onClick={onClose}
    >
      {/* Close hint */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-white/70 text-sm font-semibold tracking-wide uppercase">
          {deck.title} &mdash; {deck.slides.length} slides
        </h2>
        <button
          onClick={onClose}
          className="p-2 rounded-lg bg-white/10 hover:bg-white/20 text-white/60 hover:text-white transition-colors"
          aria-label="Close overview"
        >
          <X size={16} />
        </button>
      </div>

      {/* Grid */}
      <div
        className="grid gap-4"
        style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))' }}
        onClick={(e) => e.stopPropagation()}
      >
        {deck.slides.map((slide, i) => {
          const isActive = i === currentIdx
          return (
            <button
              key={i}
              onClick={() => { onSelectSlide(i); onClose() }}
              className={`group text-left focus:outline-none ${
                isActive ? 'ring-2 ring-blue-400 ring-offset-2 ring-offset-slate-950 rounded-lg' : ''
              }`}
            >
              {/* Thumbnail */}
              <div
                className={`w-full aspect-video rounded-lg overflow-hidden border transition-all duration-150 ${
                  isActive
                    ? 'border-blue-400 shadow-lg shadow-blue-500/20'
                    : 'border-white/10 group-hover:border-white/30 group-hover:shadow-md group-hover:shadow-white/5'
                }`}
              >
                <MiniPreview slide={slide} deck={deck} />
              </div>

              {/* Label */}
              <div className="mt-1.5 px-0.5">
                <div className="flex items-center gap-1.5">
                  <span className="text-[10px] font-semibold text-white/40 tabular-nums w-5 text-right shrink-0">
                    {i + 1}
                  </span>
                  <p className="text-[11px] font-medium text-white/70 truncate group-hover:text-white/90 transition-colors">
                    {slide.title ?? slide.quote ?? '(untitled)'}
                  </p>
                </div>
                <p className="text-[10px] text-white/30 ml-6.5 pl-0.5">{slide.layout}</p>
              </div>
            </button>
          )
        })}
      </div>

      {/* Keyboard hint */}
      <p className="mt-8 text-center text-[11px] text-white/25 select-none">
        Click or press <kbd className="font-mono bg-white/10 px-1.5 py-0.5 rounded">O</kbd> /{' '}
        <kbd className="font-mono bg-white/10 px-1.5 py-0.5 rounded">Esc</kbd> to close
      </p>
    </div>
  )
}
