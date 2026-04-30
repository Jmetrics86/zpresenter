import type { Slide } from '../../types'
import type { ThemeColors } from '../../theme'
import { resolveIconChar } from '../../theme'

interface Props {
  slide: Slide
  colors: ThemeColors
  iconMap: Record<string, string>
}

/**
 * Pull-quote card — Slidev/Spectacle "quote" layout equivalent.
 *
 * Left vertical accent bar mirrors the visual weight of the PPTX quote slide.
 * Optional title_icon shown as a large glyph above the quote text.
 */
export default function QuoteCard({ slide, colors, iconMap }: Props) {
  const text = slide.quote ?? slide.title ?? ''
  const iconChar = resolveIconChar(slide.title_icon, iconMap)

  return (
    <div className="h-full w-full bg-white flex items-center px-[7%] gap-6">
      {/* Left accent bar — mirrors the visual weight of python-pptx quote slide */}
      <div
        className="w-1.5 self-stretch my-[7%] rounded-full shrink-0"
        style={{ background: colors.accent }}
      />

      <div className="flex-1 flex flex-col justify-center">
        {iconChar && (
          <span className="text-[2rem] mb-3 leading-none">{iconChar}</span>
        )}
        <blockquote
          className="text-[1.55rem] italic font-medium text-slate-800 leading-relaxed"
        >
          &ldquo;{text}&rdquo;
        </blockquote>
        {slide.attribution && (
          <p
            className="mt-6 text-right text-[1rem] font-semibold tracking-wide"
            style={{ color: colors.muted }}
          >
            &mdash;&nbsp;{slide.attribution}
          </p>
        )}
      </div>
    </div>
  )
}
