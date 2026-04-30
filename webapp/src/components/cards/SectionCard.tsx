import type { Slide } from '../../types'
import type { ThemeColors } from '../../theme'
import { resolveIconChar } from '../../theme'

interface Props {
  slide: Slide
  colors: ThemeColors
  iconMap: Record<string, string>
}

/**
 * Section/chapter break card.
 *
 * Visual treatment inspired by Slidev section layout:
 * - When `title_color_hex` is set the card gets a light tinted background so
 *   chapter breaks feel visually distinct from content slides (web only; the
 *   PPTX builder stamps the accent band separately).
 * - White background fallback when no color is specified.
 */
export default function SectionCard({ slide, colors, iconMap }: Props) {
  const iconChar = resolveIconChar(slide.title_icon, iconMap)

  const customHex = slide.title_color_hex
    ? `#${slide.title_color_hex}`
    : null

  // Tinted background: 8% opacity of the title/accent color → subtle but clear
  const bgStyle = customHex
    ? {
        background: `linear-gradient(135deg, ${customHex}14 0%, ${customHex}08 100%)`,
        borderTop: `4px solid ${customHex}`,
      }
    : { borderTop: `4px solid ${colors.accent}` }

  const titleStyle = { color: customHex ?? colors.primary }
  const accentStyle = { background: customHex ?? colors.accent }

  return (
    <div
      className="h-full w-full bg-white flex flex-col items-center justify-center text-center px-[12%]"
      style={bgStyle}
    >
      {iconChar && (
        <span className="text-[2.2rem] mb-3 leading-none">{iconChar}</span>
      )}
      <h2
        className="text-[2.4rem] font-bold leading-tight tracking-tight"
        style={titleStyle}
      >
        {slide.title ?? ''}
      </h2>
      {/* Accent stub + hairline — matches python-pptx stamp_section_slide_band */}
      <div className="mt-4 h-1.5 w-24 rounded-full" style={accentStyle} />
      <div className="mt-1.5 h-px w-[65%] bg-slate-200" />
    </div>
  )
}
