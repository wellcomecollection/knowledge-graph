import ImageResults from './images'
import OverviewResultsBlock from './overview'

export const formatDate = (date: Date): string => {
  return new Date(date).toLocaleDateString('en-GB', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
