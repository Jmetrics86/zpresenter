import type { Deck, Slide } from '../types'
import { themeColors } from '../theme'
import TitleCard from './cards/TitleCard'
import SectionCard from './cards/SectionCard'
import ContentCard from './cards/ContentCard'
import TwoColumnCard from './cards/TwoColumnCard'
import QuoteCard from './cards/QuoteCard'
import ChartCard from './cards/ChartCard'

interface Props {
  slide: Slide
  deck: Deck
  iconMap: Record<string, string>
}

export default function SlideCard({ slide, deck, iconMap }: Props) {
  const colors = themeColors(deck.theme)
  const props = { slide, colors, iconMap }

  switch (slide.layout) {
    case 'title':
      return <TitleCard {...props} />
    case 'section':
      return <SectionCard {...props} />
    case 'title_content':
      return <ContentCard {...props} />
    case 'two_column':
      return <TwoColumnCard {...props} />
    case 'quote':
      return <QuoteCard {...props} />
    case 'chart_bar':
    case 'chart_line':
      return <ChartCard slide={slide} colors={colors} />
    default:
      return <ContentCard {...props} />
  }
}
