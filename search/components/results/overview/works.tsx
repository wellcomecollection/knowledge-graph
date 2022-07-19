import { FC } from 'react'
import OverviewResultsBlock from '.'
import { Work } from '../../../types/work'
import WorksResults from '../works'

type Props = {
  totalResults: number
  queryParams: any
  results: Work[]
  heading?: string
}
const WorkResultsOverview: FC<Props> = ({
  totalResults,
  queryParams,
  results,
  heading,
}) => {
  return (
    <OverviewResultsBlock
      heading={heading ? heading : 'Works'}
      index="works"
      totalResults={totalResults}
      queryParams={queryParams}
    >
      <WorksResults results={results} />
    </OverviewResultsBlock>
  )
}

export default WorkResultsOverview
