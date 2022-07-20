import { FC } from 'react'
import OverviewResultsBlock from '.'
import StoriesResults from '../stories'
import { Story } from '../../../types/story'

type Props = {
  totalResults: number
  queryParams?: {
    searchTerms?: string
    subject?: string
    person?: string
  }
  results: Story[]
  heading?: string
}
const StoryResultsOverview: FC<Props> = ({
  totalResults,
  queryParams,
  results,
  heading,
}) => {
  return (
    <OverviewResultsBlock
      totalResults={totalResults}
      queryParams={queryParams}
      heading={heading ? heading : 'Stories'}
      index="stories"
    >
      <StoriesResults results={results} />
    </OverviewResultsBlock>
  )
}

export default StoryResultsOverview
