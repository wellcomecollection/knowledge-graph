import { FC } from 'react'
import OverviewResultsBlock from '.'
import { WhatsOn } from '../../../types/whats-on'
import { WhatsOnResult } from '../whats-on'

type Props = {
  totalResults: number
  queryParams: any
  results: WhatsOn[]
}
const WhatsOnResultsOverview: FC<Props> = ({
  totalResults,
  queryParams,
  results,
}) => {
  return (
    <OverviewResultsBlock
      name="What's On"
      totalResults={totalResults}
      queryParams={queryParams}
    >
      <ul className="grid h-auto grid-cols-3 gap-3 pt-4">
        {results.map((whatsOn) => {
          return <WhatsOnResult whatsOn={whatsOn} key={whatsOn.title} />
        })}
      </ul>{' '}
    </OverviewResultsBlock>
  )
}

export default WhatsOnResultsOverview
