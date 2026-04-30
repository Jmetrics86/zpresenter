import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { Slide } from '../../types'
import type { ThemeColors } from '../../theme'
import { CHART_COLORS, titleColor } from '../../theme'

interface Props {
  slide: Slide
  colors: ThemeColors
}

/**
 * Bar / line chart card — Slidev "chart" layout equivalent.
 *
 * Uses Recharts' ResponsiveContainer so the chart fills whatever height remains
 * after the header band. Series colours cycle through CHART_COLORS (first colour
 * can be overridden by deck accent_hex via CHART_COLORS[0] if desired).
 *
 * Title colour respects `slide.title_color_hex`.
 */
export default function ChartCard({ slide, colors }: Props) {
  const categories = slide.chart_categories ?? []
  const series = slide.chart_series ?? []
  const tc = titleColor(slide)

  const data = categories.map((cat, i) => ({
    name: cat,
    ...Object.fromEntries(series.map((s) => [s.name, s.values[i] ?? 0])),
  }))

  const isLine = slide.layout === 'chart_line'
  const tickStyle = { fontSize: 11, fill: '#64748B' }

  return (
    <div className="h-full w-full bg-white flex flex-col px-[5.5%] py-[4%]">
      {/* Header */}
      <div className="shrink-0">
        <h2
          className="text-[1.65rem] font-bold tracking-tight leading-tight"
          style={{ color: tc }}
        >
          {slide.title ?? ''}
        </h2>
        {slide.subtitle && (
          <p className="text-[0.88rem] mt-0.5" style={{ color: colors.muted }}>
            {slide.subtitle}
          </p>
        )}
        {/* Accent stub + hairline — mirrors stamp_content_header_band */}
        <div className="flex items-center mt-2">
          <div
            className="h-1 w-14 rounded-full shrink-0"
            style={{ background: colors.accent }}
          />
          <div className="flex-1 h-px bg-slate-200 ml-2" />
        </div>
      </div>

      {/* Chart area — fills remaining height */}
      <div className="flex-1 mt-3 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          {isLine ? (
            <LineChart data={data} margin={{ top: 4, right: 24, bottom: 0, left: -8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
              <XAxis dataKey="name" tick={tickStyle} />
              <YAxis tick={tickStyle} />
              <Tooltip contentStyle={{ fontSize: 12, borderRadius: 8 }} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              {series.map((s, si) => (
                <Line
                  key={s.name}
                  type="monotone"
                  dataKey={s.name}
                  stroke={CHART_COLORS[si % CHART_COLORS.length]}
                  strokeWidth={2.5}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
              ))}
            </LineChart>
          ) : (
            <BarChart data={data} margin={{ top: 4, right: 24, bottom: 0, left: -8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
              <XAxis dataKey="name" tick={tickStyle} />
              <YAxis tick={tickStyle} />
              <Tooltip contentStyle={{ fontSize: 12, borderRadius: 8 }} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              {series.map((s, si) => (
                <Bar
                  key={s.name}
                  dataKey={s.name}
                  fill={CHART_COLORS[si % CHART_COLORS.length]}
                  radius={[4, 4, 0, 0]}
                />
              ))}
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  )
}
