import type { Slide } from '../../types'
import type { ThemeColors } from '../../theme'
import { resolveIconChar, titleColor } from '../../theme'

interface Props {
  slide: Slide
  colors: ThemeColors
  iconMap: Record<string, string>
}

function BulletList({
  bullets,
  icons,
  colors,
  iconMap,
}: {
  bullets: string[]
  icons: (string | null)[]
  colors: ThemeColors
  iconMap: Record<string, string>
}) {
  return (
    <ul className="space-y-2">
      {bullets.map((b, i) => {
        const iconChar = resolveIconChar(icons[i], iconMap)
        return (
          <li key={i} className="flex items-start gap-2.5">
            <span
              className="shrink-0 mt-0.5 text-[0.9rem] font-bold leading-snug"
              style={{ color: colors.accent }}
            >
              {iconChar || '▸'}
            </span>
            <span className="text-[0.85rem] text-slate-700 leading-snug">{b}</span>
          </li>
        )
      })}
    </ul>
  )
}

/**
 * Two-column comparison card — Slidev/Spectacle "two-cols" layout equivalent.
 *
 * Vertical divider mirrors `add_vertical_rule` in `slide_design.py`.
 * Title colour respects `slide.title_color_hex`.
 */
export default function TwoColumnCard({ slide, colors, iconMap }: Props) {
  const titleIconChar = resolveIconChar(slide.title_icon, iconMap)
  const tc = titleColor(slide)

  return (
    <div className="h-full w-full bg-white flex flex-col px-[5.5%] py-[4%]">
      {/* Header */}
      <div className="shrink-0">
        <div className="flex items-center gap-2.5">
          {titleIconChar && (
            <span className="text-[1.5rem] leading-none">{titleIconChar}</span>
          )}
          <h2
            className="text-[1.65rem] font-bold tracking-tight leading-tight"
            style={{ color: tc }}
          >
            {slide.title ?? ''}
          </h2>
        </div>
        <div className="flex items-center mt-2">
          <div
            className="h-1 w-14 rounded-full shrink-0"
            style={{ background: colors.accent }}
          />
          <div className="flex-1 h-px bg-slate-200 ml-2" />
        </div>
      </div>

      {/* Two columns with vertical divider */}
      <div className="flex-1 flex mt-4 gap-4 min-h-0 overflow-hidden">
        <div className="flex-1 overflow-hidden">
          <BulletList
            bullets={slide.bullets_left ?? []}
            icons={slide.bullets_left_icons ?? []}
            colors={colors}
            iconMap={iconMap}
          />
        </div>
        {/* Vertical rule — mirrors add_vertical_rule */}
        <div className="w-px bg-slate-200 self-stretch shrink-0" />
        <div className="flex-1 overflow-hidden">
          <BulletList
            bullets={slide.bullets_right ?? []}
            icons={slide.bullets_right_icons ?? []}
            colors={colors}
            iconMap={iconMap}
          />
        </div>
      </div>
    </div>
  )
}
