export interface DeckTheme {
  primary_hex?: string | null
  accent_hex?: string | null
  muted_hex?: string | null
}

export interface ChartSeries {
  name: string
  values: number[]
}

export interface SlideImage {
  src: string
  placement: string
  caption?: string | null
  context?: string | null
}

export type LayoutKind =
  | 'title'
  | 'title_content'
  | 'section'
  | 'quote'
  | 'chart_bar'
  | 'chart_line'
  | 'two_column'

export type LayoutIntent =
  | 'opening'
  | 'chapter_break'
  | 'narrative'
  | 'comparison'
  | 'metrics_bar'
  | 'metrics_trend'
  | 'pull_quote'
  | 'visual_emphasis'

export interface Slide {
  layout: LayoutKind
  layout_intent?: LayoutIntent | null
  title?: string | null
  subtitle?: string | null
  bullets?: string[] | null
  bullets_left?: string[] | null
  bullets_right?: string[] | null
  quote?: string | null
  attribution?: string | null
  chart_categories?: string[] | null
  chart_series?: ChartSeries[] | null
  notes?: string | null
  title_color_hex?: string | null
  title_icon?: string | null
  bullet_icons?: (string | null)[] | null
  bullets_left_icons?: (string | null)[] | null
  bullets_right_icons?: (string | null)[] | null
  images?: SlideImage[] | null
}

export interface Deck {
  title: string
  subtitle?: string | null
  author?: string | null
  theme?: DeckTheme | null
  audience?: {
    technical_level?: string
    attention_span?: string
  }
  slides: Slide[]
}

export interface Finding {
  severity: 'error' | 'warn' | 'info'
  slide_index?: number | null
  message: string
  suggestion?: string | null
}

export interface ValidateResult {
  deck: Deck
  findings: Finding[]
  summary: { errors: number; warnings: number; info: number }
}

// ── AI improvement ────────────────────────────────────────────────────────

export type AIProvider = 'anthropic' | 'openai' | 'gemini'

export interface ImproveRequest {
  deck: Deck
  slideIndex: number
  instructions: string
  provider: AIProvider
  model: string
  apiKey: string
}

export interface ImproveEvent {
  type: 'delta' | 'done' | 'error'
  text?: string     // delta chunk
  buffer?: string   // full accumulated text (done event)
  message?: string  // error description
}

export interface ProviderInfo {
  label: string
  models: string[]
  env_var: string
  configured: boolean
}

export interface ModelsResponse {
  providers: Record<AIProvider, ProviderInfo>
}
