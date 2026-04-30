import { useState, useEffect, useCallback } from 'react'
import type { Deck, Finding, Slide } from './types'
import { validateDeck, exportPptx, listExamples, loadExample, fetchIcons } from './api'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import SlideViewer from './components/SlideViewer'
import OverviewModal from './components/OverviewModal'
import AIPanel from './components/AIPanel'

export default function App() {
  // ── Core deck state ────────────────────────────────────────────────────
  const [deck, setDeck] = useState<Deck | null>(null)
  const [currentIdx, setCurrentIdx] = useState(0)
  const [jsonText, setJsonText] = useState('')
  const [findings, setFindings] = useState<Finding[]>([])
  const [errors, setErrors] = useState('')
  const [loading, setLoading] = useState(false)
  const [exportLoading, setExportLoading] = useState(false)

  // ── UI state ───────────────────────────────────────────────────────────
  const [examples, setExamples] = useState<string[]>([])
  const [iconMap, setIconMap] = useState<Record<string, string>>({})
  const [presentMode, setPresentMode] = useState(false)
  const [overviewMode, setOverviewMode] = useState(false)
  const [aiPanelOpen, setAiPanelOpen] = useState(false)
  const [activeTab, setActiveTab] = useState<'load' | 'slides'>('load')

  // ── AI undo (one-level per slide; cleared when slide changes) ──────────
  const [aiUndo, setAiUndo] = useState<{ idx: number; slide: Slide } | null>(null)

  // Bootstrap
  useEffect(() => {
    listExamples().then(setExamples).catch(() => {})
    fetchIcons()
      .then((icons) => setIconMap(Object.fromEntries(icons.map((ic) => [ic.id, ic.char]))))
      .catch(() => {})
  }, [])

  // Prevent body scroll in overlays
  useEffect(() => {
    document.body.style.overflow = presentMode || overviewMode ? 'hidden' : ''
    return () => { document.body.style.overflow = '' }
  }, [presentMode, overviewMode])

  // Clear undo when slide changes
  useEffect(() => {
    setAiUndo(null)
  }, [currentIdx])

  // ── Navigation ─────────────────────────────────────────────────────────
  const go = useCallback(
    (dir: 1 | -1) => {
      if (!deck) return
      setCurrentIdx((i) => Math.min(Math.max(0, i + dir), deck.slides.length - 1))
    },
    [deck],
  )

  // ── Deck load / validate ───────────────────────────────────────────────
  const handleValidate = useCallback(async () => {
    if (!jsonText.trim()) return
    setLoading(true)
    setErrors('')
    try {
      const raw: unknown = JSON.parse(jsonText)
      const result = await validateDeck(raw)
      setDeck(result.deck)
      setFindings(result.findings)
      setCurrentIdx(0)
      setActiveTab('slides')
    } catch (e: unknown) {
      setErrors(e instanceof Error ? e.message : String(e))
      setDeck(null)
    } finally {
      setLoading(false)
    }
  }, [jsonText])

  const handleLoadExample = useCallback(async (name: string) => {
    setLoading(true)
    setErrors('')
    try {
      const raw = await loadExample(name)
      setJsonText(JSON.stringify(raw, null, 2))
      const result = await validateDeck(raw)
      setDeck(result.deck)
      setFindings(result.findings)
      setCurrentIdx(0)
      setActiveTab('slides')
    } catch (e: unknown) {
      setErrors(e instanceof Error ? e.message : String(e))
    } finally {
      setLoading(false)
    }
  }, [])

  // ── Export ─────────────────────────────────────────────────────────────
  const handleExport = useCallback(async () => {
    if (!deck) return
    setExportLoading(true)
    try {
      await exportPptx(deck)
    } catch (e: unknown) {
      setErrors(e instanceof Error ? e.message : 'Export failed')
    } finally {
      setExportLoading(false)
    }
  }, [deck])

  // ── AI apply / undo ────────────────────────────────────────────────────
  const handleApplyAI = useCallback(
    (updatedSlide: Slide) => {
      if (!deck) return
      setAiUndo({ idx: currentIdx, slide: deck.slides[currentIdx] })
      const newSlides = [...deck.slides]
      newSlides[currentIdx] = updatedSlide
      setDeck({ ...deck, slides: newSlides })
    },
    [deck, currentIdx],
  )

  const handleUndoAI = useCallback(() => {
    if (!deck || !aiUndo) return
    const newSlides = [...deck.slides]
    newSlides[aiUndo.idx] = aiUndo.slide
    setDeck({ ...deck, slides: newSlides })
    setAiUndo(null)
  }, [deck, aiUndo])

  // ── Keyboard shortcuts (Slidev-compatible) ─────────────────────────────
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (!deck) return
      const tag = (e.target as HTMLElement).tagName
      if (tag === 'TEXTAREA' || tag === 'INPUT' || tag === 'SELECT') return

      switch (e.key) {
        case 'ArrowRight':
        case 'ArrowDown':
        case ' ':
          e.preventDefault()
          go(1)
          break
        case 'ArrowLeft':
        case 'ArrowUp':
          e.preventDefault()
          go(-1)
          break
        case 'Escape':
          if (presentMode) setPresentMode(false)
          else if (overviewMode) setOverviewMode(false)
          else if (aiPanelOpen) setAiPanelOpen(false)
          break
        case 'f':
        case 'F':
          if (!presentMode && !overviewMode) setPresentMode(true)
          break
        case 'o':
        case 'O':
          if (!presentMode) setOverviewMode((v) => !v)
          break
        case 'i':
        case 'I':
          if (!presentMode && !overviewMode) setAiPanelOpen((v) => !v)
          break
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [deck, presentMode, overviewMode, aiPanelOpen, go])

  return (
    <div className="flex flex-col h-screen bg-slate-100 overflow-hidden">
      <Header
        deck={deck}
        onExport={handleExport}
        exportLoading={exportLoading}
        onPresent={() => setPresentMode(true)}
      />

      {/* ── Present mode ─────────────────────────────────────────── */}
      {presentMode && deck && (
        <div
          className="fixed inset-0 z-50 bg-black flex flex-col items-center justify-center"
          onClick={() => setPresentMode(false)}
        >
          <div className="w-full max-w-[90vw]" onClick={(e) => e.stopPropagation()}>
            <SlideViewer
              deck={deck}
              currentIdx={currentIdx}
              onPrev={() => go(-1)}
              onNext={() => go(1)}
              onOpenOverview={() => {}}
              onToggleAI={() => {}}
              aiPanelOpen={false}
              iconMap={iconMap}
              presentMode
            />
          </div>
          <p className="mt-4 text-white/25 text-xs select-none">
            ← → navigate · Esc to exit
          </p>
        </div>
      )}

      {/* ── Overview modal ───────────────────────────────────────── */}
      {overviewMode && deck && (
        <OverviewModal
          deck={deck}
          currentIdx={currentIdx}
          onSelectSlide={(i) => { setCurrentIdx(i); setOverviewMode(false) }}
          onClose={() => setOverviewMode(false)}
        />
      )}

      {/* ── Main layout ──────────────────────────────────────────── */}
      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          activeTab={activeTab}
          onTabChange={setActiveTab}
          deck={deck}
          currentIdx={currentIdx}
          onSelectSlide={setCurrentIdx}
          jsonText={jsonText}
          onJsonChange={setJsonText}
          onValidate={handleValidate}
          loading={loading}
          errors={errors}
          findings={findings}
          examples={examples}
          onLoadExample={handleLoadExample}
        />

        <main className="flex-1 flex flex-col items-center justify-start py-8 px-8 gap-6 overflow-auto bg-slate-100">
          {deck ? (
            <>
              <SlideViewer
                deck={deck}
                currentIdx={currentIdx}
                onPrev={() => go(-1)}
                onNext={() => go(1)}
                onOpenOverview={() => setOverviewMode(true)}
                onToggleAI={() => setAiPanelOpen((v) => !v)}
                aiPanelOpen={aiPanelOpen}
                iconMap={iconMap}
              />

              {/* ── AI Panel (below slide viewer) ───────────────── */}
              {aiPanelOpen && (
                <AIPanel
                  deck={deck}
                  slideIndex={currentIdx}
                  onApply={handleApplyAI}
                  onUndo={aiUndo ? handleUndoAI : null}
                  canUndo={aiUndo !== null && aiUndo.idx === currentIdx}
                />
              )}
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center w-full">
              <div className="text-center select-none">
                <div className="text-7xl mb-5">🎴</div>
                <h2 className="text-2xl font-bold text-slate-600 mb-2">No deck loaded</h2>
                <p className="text-slate-400 text-sm max-w-xs mx-auto leading-relaxed">
                  Paste JSON or pick an example in the sidebar, then click{' '}
                  <strong>Load Deck</strong>.
                </p>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
