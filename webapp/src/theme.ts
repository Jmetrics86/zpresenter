import type { DeckTheme } from './types'

export interface ThemeColors {
  accent: string
  primary: string
  muted: string
}

export function themeColors(theme?: DeckTheme | null): ThemeColors {
  return {
    accent: theme?.accent_hex ? `#${theme.accent_hex}` : '#2563EB',
    primary: theme?.primary_hex ? `#${theme.primary_hex}` : '#1E3A5F',
    muted: theme?.muted_hex ? `#${theme.muted_hex}` : '#64748B',
  }
}

export function resolveIconChar(
  iconId: string | null | undefined,
  iconMap: Record<string, string>,
): string {
  if (!iconId) return ''
  return iconMap[iconId] ?? ''
}

export function titleColor(slide: { title_color_hex?: string | null }): string {
  return slide.title_color_hex ? `#${slide.title_color_hex}` : '#1F2937'
}

export const CHART_COLORS = [
  '#2563EB',
  '#059669',
  '#D97706',
  '#DC2626',
  '#7C3AED',
  '#0891B2',
  '#BE185D',
]
