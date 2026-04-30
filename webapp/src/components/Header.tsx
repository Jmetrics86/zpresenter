import { Download, Maximize2 } from 'lucide-react'
import type { Deck } from '../types'

interface Props {
  deck: Deck | null
  onExport: () => void
  exportLoading: boolean
  onPresent: () => void
}

export default function Header({ deck, onExport, exportLoading, onPresent }: Props) {
  return (
    <header className="h-14 bg-slate-900 flex items-center px-5 gap-4 shrink-0">
      {/* Brand */}
      <div className="flex items-center gap-2 min-w-0">
        <span className="text-white font-bold text-lg tracking-tight select-none">🎴</span>
        <span className="text-white font-bold text-base tracking-tight select-none">zpresenter</span>
        {deck && (
          <>
            <span className="text-slate-600 select-none">/</span>
            <span className="text-slate-300 text-sm font-medium truncate max-w-xs">
              {deck.title}
            </span>
            {deck.author && (
              <span className="text-slate-500 text-xs hidden md:inline truncate">
                &nbsp;·&nbsp;{deck.author}
              </span>
            )}
          </>
        )}
      </div>

      <div className="flex-1" />

      {/* Actions */}
      {deck && (
        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={onPresent}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-white text-sm font-medium transition-colors"
            title="Present (keyboard: F)"
          >
            <Maximize2 size={14} />
            <span className="hidden sm:inline">Present</span>
          </button>
          <button
            onClick={onExport}
            disabled={exportLoading}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 disabled:opacity-60 disabled:cursor-wait text-white text-sm font-medium transition-colors"
          >
            <Download size={14} />
            <span>{exportLoading ? 'Exporting…' : 'Export PPTX'}</span>
          </button>
        </div>
      )}
    </header>
  )
}
