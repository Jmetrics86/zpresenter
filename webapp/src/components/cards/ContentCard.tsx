import type { Slide } from '../../types'
import type { ThemeColors } from '../../theme'
import { resolveIconChar, titleColor } from '../../theme'

interface Props {
  slide: Slide
  colors: ThemeColors
  iconMap: Record<string, string>
}

/**
 * Title + bullets card — Slidev/Spectacle "default" layout equivalent.
 *
 * Header band: accent stub (short) + full-width hairline, matching
 * `stamp_content_header_band` in `slide_design.py`.
 * Bullets: accent-coloured icon/arrow marker, slate body text.
 */
export default function ContentCard({ slide, colors, iconMap }: Props) {
  const bullets = slide.bullets ?? []
  const bulletIcons = slide.bullet_icons ?? []
  const titleIconChar = resolveIconChar(slide.title_icon, iconMap)
  const tc = titleColor(slide)

  return (
    <div className="h-full w-full bg-white flex flex-col px-[5.5%] py-[4%]">
      {/* Header */}
      <div className="shrink-0">
        <div className="flex items-center gap-2.5">
          {titleIconChar && (
            <span className="text-[1.6rem] leading-none">{titleIconChar}</span>
          )}
          <h2
            className="text-[1.65rem] font-bold tracking-tight leading-tight"
            style={{ color: tc }}
          >
            {slide.title ?? ''}
          </h2>
        </div>
        {/* Accent stub + hairline — mirrors stamp_content_header_band */}
        <div className="flex items-center mt-2">
          <div
            className="h-1 w-14 rounded-full shrink-0"
            style={{ background: colors.accent }}
          />
          <div className="flex-1 h-px bg-slate-200 ml-2" />
        </div>
      </div>

      {/* Bullet list */}
      <ul className="mt-4 flex-1 flex flex-col justify-start space-y-2.5 overflow-hidden min-h-0">
        {bullets.map((bullet, i) => {
          const iconChar = resolveIconChar(bulletIcons[i], iconMap)
          return (
            <li key={i} className="flex items-start gap-3">
              <span
                className="shrink-0 mt-0.5 text-[1rem] font-bold leading-snug"
                style={{ color: colors.accent }}
              >
                {iconChar || '▸'}
              </span>
              <span className="text-[0.95rem] text-slate-700 leading-snug">{bullet}</span>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
