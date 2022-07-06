import { FC } from 'react'
import OverviewResultsBlock from '.'
import StoriesResults from '../stories'
import { Story } from '../../../types/story'

type Props = {
  totalResults: number
  queryParams: any
  results: Story[]
}
const StoryResultsOverview: FC<Props> = ({
  totalResults,
  queryParams,
  results,
}) => {
  return (
    <OverviewResultsBlock
      name="Stories"
      totalResults={totalResults}
      queryParams={queryParams}
    >
      <StoriesResults results={results} />
    </OverviewResultsBlock>
  )
}

export default StoryResultsOverview
