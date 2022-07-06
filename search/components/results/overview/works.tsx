import { FC } from 'react'
import OverviewResultsBlock from '.'
import { Work } from '../../../types/work'
import WorksResults from '../works'

type Props = {
  totalResults: number
  queryParams: any
  results: Work[]
}
const WorkResultsOverview: FC<Props> = ({
  totalResults,
  queryParams,
  results,
}) => {
  return (
    <OverviewResultsBlock
      name="Works"
      totalResults={totalResults}
      queryParams={queryParams}
    >
      <WorksResults results={results} />
    </OverviewResultsBlock>
  )
}

export default WorkResultsOverview
