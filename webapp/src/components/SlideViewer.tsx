import { ChevronLeft, ChevronRight, Grid, Sparkles } from 'lucide-react'
import type { Deck } from '../types'
import { themeColors } from '../theme'
import SlideCard from './SlideCard'

interface Props {
  deck: Deck
  currentIdx: number
  onPrev: () => void
  onNext: () => void
  onOpenOverview: () => void
  onToggleAI: () => void
  aiPanelOpen: boolean
  iconMap: Record<string, string>
  presentMode?: boolean
}

/**
 * Slide viewer with:
 * - Fade-in transition (Slidev-style, via key-remount + Tailwind animation)
 * - Progress bar (thin coloured rail, accent-coloured, Slidev-style)
 * - Keyboard shortcut hint strip
 * - Speaker notes panel (hidden in present mode)
 * - AI Improve toggle button
 */
export default function SlideViewer({
  deck,
  currentIdx,
  onPrev,
  onNext,
  onOpenOverview,
  onToggleAI,
  aiPanelOpen,
  iconMap,
  presentMode = false,
}: Props) {
  const slide = deck.slides[currentIdx]
  const isFirst = currentIdx === 0
  const isLast = currentIdx === deck.slides.length - 1
  const colors = themeColors(deck.theme)
  const pct = ((currentIdx + 1) / deck.slides.length) * 100

  return (
    <div
      className={`flex flex-col items-center gap-3 ${
        presentMode ? 'w-full h-full justify-center' : 'w-full max-w-4xl'
      }`}
    >
      {/* ── Slide card ─────────────────────────────────────────────── */}
      <div
        key={currentIdx}
        className="w-full aspect-video rounded-2xl shadow-2xl overflow-hidden ring-1 ring-black/5 animate-fade-in"
      >
        <SlideCard slide={slide} deck={deck} iconMap={iconMap} />
      </div>

      {/* ── Progress bar ───────────────────────────────────────────── */}
      <div className="w-full">
        <div className="h-0.5 w-full bg-slate-200 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-300 ease-out"
            style={{ width: `${pct}%`, background: colors.accent }}
          />
        </div>
      </div>

      {/* ── Navigation controls ────────────────────────────────────── */}
      <div className="flex items-center gap-3">
        <button
          onClick={onPrev}
          disabled={isFirst}
          className={`p-2.5 rounded-xl shadow-sm hover:shadow-md disabled:opacity-30 disabled:cursor-not-allowed transition-all ${
            presentMode
              ? 'bg-white/10 text-white hover:bg-white/20'
              : 'bg-white text-slate-600 hover:bg-slate-50'
          }`}
          aria-label="Previous slide"
        >
          <ChevronLeft size={20} />
        </button>

        <span
          className={`text-sm font-semibold tabular-nums select-none min-w-[100px] text-center ${
            presentMode ? 'text-white/70' : 'text-slate-500'
          }`}
        >
          {currentIdx + 1} / {deck.slides.length}
          <span
            className={`ml-2 text-[11px] font-normal ${
              presentMode ? 'text-white/40' : 'text-slate-400'
            }`}
          >
            {slide.layout}
          </span>
        </span>

        <button
          onClick={onNext}
          disabled={isLast}
          className={`p-2.5 rounded-xl shadow-sm hover:shadow-md disabled:opacity-30 disabled:cursor-not-allowed transition-all ${
            presentMode
              ? 'bg-white/10 text-white hover:bg-white/20'
              : 'bg-white text-slate-600 hover:bg-slate-50'
          }`}
          aria-label="Next slide"
        >
          <ChevronRight size={20} />
        </button>

        {!presentMode && (
          <>
            <button
              onClick={onOpenOverview}
              className="p-2.5 rounded-xl bg-white text-slate-500 shadow-sm hover:shadow-md hover:bg-slate-50 transition-all"
              title="Overview (O)"
            >
              <Grid size={18} />
            </button>

            {/* ✨ AI Improve toggle */}
            <button
              onClick={onToggleAI}
              className={`p-2.5 rounded-xl shadow-sm hover:shadow-md transition-all ${
                aiPanelOpen
                  ? 'bg-violet-600 text-white hover:bg-violet-500 ring-2 ring-violet-400 ring-offset-1'
                  : 'bg-white text-violet-500 hover:bg-violet-50'
              }`}
              title="AI Improve (I)"
              aria-label="Toggle AI improvement panel"
            >
              <Sparkles size={18} />
            </button>
          </>
        )}
      </div>

      {/* ── Keyboard shortcuts hint ─────────────────────────────────── */}
      {!presentMode && (
        <p className="text-[10px] text-slate-400 select-none tracking-wide">
          ← → navigate &nbsp;·&nbsp;
          <kbd className="font-mono bg-slate-100 px-1 rounded">F</kbd> present &nbsp;·&nbsp;
          <kbd className="font-mono bg-slate-100 px-1 rounded">O</kbd> overview &nbsp;·&nbsp;
          <kbd className="font-mono bg-slate-100 px-1 rounded">I</kbd> AI improve
        </p>
      )}

      {/* ── Speaker notes ───────────────────────────────────────────── */}
      {!presentMode && slide.notes && (
        <div className="w-full bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 max-w-4xl animate-slide-up">
          <p className="text-sm text-amber-800">
            <span className="font-semibold">Notes:&nbsp;</span>
            {slide.notes}
          </p>
        </div>
      )}
    </div>
  )
}
