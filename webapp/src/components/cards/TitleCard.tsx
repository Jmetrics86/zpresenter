import type { Slide } from '../../types'
import type { ThemeColors } from '../../theme'
import { resolveIconChar, titleColor } from '../../theme'

interface Props {
  slide: Slide
  colors: ThemeColors
  iconMap: Record<string, string>
}

/**
 * Opening/cover card — Spectacle/Slidev "cover" layout equivalent.
 *
 * Structure: accent top stripe → large centered title → optional subtitle → bottom hairline.
 * Title colour: respects `slide.title_color_hex`, falls back to body charcoal.
 */
export default function TitleCard({ slide, colors, iconMap }: Props) {
  const tc = titleColor(slide)
  const iconChar = resolveIconChar(slide.title_icon, iconMap)

  return (
    <div className="relative h-full w-full bg-white flex flex-col">
      {/* Top accent band — web-canvas variant; PPTX places a hairline at the footer instead */}
      <div className="h-2 shrink-0" style={{ background: colors.accent }} />

      {/* Vertically centered content area */}
      <div className="flex-1 flex flex-col items-center justify-center px-[8%] text-center">
        {iconChar && (
          <span className="text-[2.8rem] mb-3 leading-none">{iconChar}</span>
        )}
        <h1
          className="text-[2.8rem] font-bold leading-tight tracking-tight"
          style={{ color: tc }}
        >
          {slide.title ?? ''}
        </h1>
        {slide.subtitle && (
          <p
            className="mt-4 text-[1.2rem] font-normal leading-relaxed max-w-[80%]"
            style={{ color: colors.muted }}
          >
            {slide.subtitle}
          </p>
        )}
      </div>

      {/* Footer hairline — mirrors python-pptx stamp_title_slide_footer_rule */}
      <div className="mx-[5%] mb-5 h-px bg-slate-200 shrink-0" />
    </div>
  )
}
